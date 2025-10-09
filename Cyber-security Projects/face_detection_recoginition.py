import cv2
import os
import numpy as np
import mysql.connector
from mysql.connector import Error, pooling
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
from functools import lru_cache
import threading
from queue import Queue

# ====== MySQL Config with Connection Pooling ======
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "********",
    "database": "face_recog_db",
    "pool_name": "face_recog_pool",
    "pool_size": 5,
    "pool_reset_session": True
}

# Initialize connection pool
try:
    connection_pool = pooling.MySQLConnectionPool(**DB_CONFIG)
except Error as e:
    print(f"Error creating connection pool: {e}")
    connection_pool = None
# ===========================

DATASET_DIR = "dataset"
TRAINER_FILE = "trainer.yml"
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR)

# ====== Cached Face Detector (Singleton) ======
_face_detector = None

def get_face_detector():
    """Reuse face detector instead of creating new instances"""
    global _face_detector
    if _face_detector is None:
        _face_detector = cv2.CascadeClassifier(CASCADE_PATH)
    return _face_detector

# ====== Optimized DB Helpers with Connection Pooling ======
def get_db_connection():
    """Get connection from pool"""
    if connection_pool:
        return connection_pool.get_connection()
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )

def insert_person(name, note=None):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql = "INSERT INTO persons (name, note) VALUES (%s, %s)"
        cur.execute(sql, (name, note))
        conn.commit()
        person_id = cur.lastrowid
        return person_id
    except Error as e:
        print("DB Error:", e)
        return None
    finally:
        if conn:
            cur.close()
            conn.close()

@lru_cache(maxsize=1)
def fetch_all_persons_cached():
    """Cache database results to avoid repeated queries"""
    return fetch_all_persons()

def fetch_all_persons():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, note, created_at FROM persons ORDER BY id")
        rows = cur.fetchall()
        return rows
    except Error as e:
        print("DB fetch error:", e)
        return []
    finally:
        if conn:
            cur.close()
            conn.close()

def delete_person(person_id):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM persons WHERE id = %s", (person_id,))
        conn.commit()
        fetch_all_persons_cached.cache_clear()  # Clear cache
        return True
    except Error as e:
        print("DB delete error:", e)
        return False
    finally:
        if conn:
            cur.close()
            conn.close()

@lru_cache(maxsize=1)
def get_name_map():
    """Cache name mapping to avoid repeated DB queries"""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM persons")
        name_map = {row[0]: row[1] for row in cur.fetchall()}
        return name_map
    except Error as e:
        print("DB error:", e)
        return {}
    finally:
        if conn:
            cur.close()
            conn.close()

# ====== Optimized Image Preprocessing ======
def preprocess_face(face_img):
    """Optimized preprocessing with reduced operations"""
    # Single resize operation
    face_resized = cv2.resize(face_img, (150, 150), interpolation=cv2.INTER_LINEAR)
    # Combined equalization and blur
    face_equalized = cv2.equalizeHist(face_resized)
    # Reduced blur kernel for speed
    face_blurred = cv2.GaussianBlur(face_equalized, (3, 3), 0)
    return face_blurred

# ====== Optimized Training with Batch Processing ======
def get_images_and_labels(dataset_path):
    faces = []
    ids = []
    face_detector = get_face_detector()
    
    print("\n=== Loading Training Data ===")
    
    # Pre-allocate lists with estimated size
    person_dirs = [d for d in sorted(os.listdir(dataset_path)) 
                   if os.path.isdir(os.path.join(dataset_path, d))]
    
    for person_dir in person_dirs:
        person_path = os.path.join(dataset_path, person_dir)
        
        try:
            person_id = int(person_dir.split("_")[0])
        except ValueError:
            print(f"Skipping invalid directory: {person_dir}")
            continue
            
        person_name = "_".join(person_dir.split("_")[1:])
        image_count = 0
        
        # Batch read images
        image_files = sorted(os.listdir(person_path))
        for image_file in image_files:
            img_path = os.path.join(person_path, image_file)
            gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            
            if gray is None:
                continue
            
            face_processed = preprocess_face(gray)
            faces.append(face_processed)
            ids.append(person_id)
            image_count += 1
        
        print(f"  ID {person_id} ({person_name}): Loaded {image_count} images")

    if len(faces) == 0:
        print("ERROR: No valid face images found!")
        return None, None
    
    print(f"\nTotal faces loaded: {len(faces)}")
    print(f"Unique IDs: {len(set(ids))}")
    return faces, ids

def train_model():
    faces, ids = get_images_and_labels(DATASET_DIR)
    if faces is None or ids is None:
        print("No faces found to train.")
        return False
    
    # Optimized LBPH parameters
    recognizer = cv2.face.LBPHFaceRecognizer_create(
        radius=1,
        neighbors=8,
        grid_x=8,
        grid_y=8,
        threshold=100.0
    )
    
    recognizer.train(faces, np.array(ids))
    recognizer.save(TRAINER_FILE)
    
    # Clear cache after training
    get_name_map.cache_clear()
    
    print(f"\n✓ Model trained successfully with {len(faces)} samples from {len(set(ids))} persons.")
    return True

# ====== Optimized Recognition with Frame Skipping ======
def recognize_faces():
    if not os.path.exists(TRAINER_FILE):
        messagebox.showwarning("No Model", "Please enroll persons and train first!")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create(
        radius=1,
        neighbors=8,
        grid_x=8,
        grid_y=8,
        threshold=100.0
    )
    recognizer.read(TRAINER_FILE)
    face_cascade = get_face_detector()

    # Use cached name map
    name_map = get_name_map()
    print("\nAvailable persons in database:", name_map)

    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cam.set(cv2.CAP_PROP_FPS, 30)
    cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer for lower latency
    
    messagebox.showinfo("Recognition", "Press Q to stop recognition.\n\nTips:\n- Face the camera directly\n- Ensure good lighting\n- Stay at similar distance as enrollment")

    frame_count = 0
    process_every_n_frames = 2  # Process every 2nd frame for better performance
    last_predictions = {}  # Cache predictions
    
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Process only every Nth frame for face detection
        if frame_count % process_every_n_frames == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Optimized detection parameters
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.2,  # Faster than 1.1
                minNeighbors=5,    # Reduced for speed
                minSize=(80, 80),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            # Process detected faces
            for idx, (x, y, w, h) in enumerate(faces):
                roi_gray = gray[y:y+h, x:x+w]
                roi_processed = preprocess_face(roi_gray)
                
                id_, confidence = recognizer.predict(roi_processed)
                
                # Cache prediction
                last_predictions[idx] = (id_, confidence, x, y, w, h)
        
        # Draw using cached predictions
        for idx, pred_data in last_predictions.items():
            if len(pred_data) == 6:
                id_, confidence, x, y, w, h = pred_data
                
                # Determine label and color based on confidence
                if confidence < 60:
                    name = name_map.get(id_, f"Unknown ID {id_}")
                    label = f"{name}"
                    color = (0, 255, 0)
                elif confidence < 85:
                    name = name_map.get(id_, f"Unknown ID {id_}")
                    label = f"{name}?"
                    color = (0, 165, 255)
                else:
                    label = "Unknown"
                    color = (0, 0, 255)
                
                conf_label = f"Conf: {round(confidence, 1)}"
                
                # Draw rectangle and labels
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
                cv2.putText(frame, label, (x+5, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                cv2.putText(frame, conf_label, (x+5, y+h+25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        # Display instructions
        cv2.putText(frame, "Press 'Q' to quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.imshow("Face Recognition System", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

# ====== Optimized Enrollment ======
def enroll_person():
    name = simpledialog.askstring("Enroll", "Enter person name:")
    if not name or name.strip() == "":
        return
    
    name = name.strip()
    note = simpledialog.askstring("Enroll", "Enter note (optional):")
    
    person_id = insert_person(name, note)
    if not person_id:
        messagebox.showerror("DB Error", "Failed to save person to database.")
        return

    face_detector = get_face_detector()
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cam.set(cv2.CAP_PROP_FPS, 30)
    
    messagebox.showinfo("Instructions", 
        f"Enrolling: {name}\n\n"
        "Instructions:\n"
        "- Look directly at camera\n"
        "- Move your head slightly (left, right, up, down)\n"
        "- Keep face well-lit\n"
        "- Maintain distance from camera\n"
        "- Press Q to finish (minimum 20 samples)\n\n"
        "Capturing 50 images...")

    count = 0
    skipped = 0
    person_dir = os.path.join(DATASET_DIR, f"{person_id}_{name}")
    os.makedirs(person_dir, exist_ok=True)

    # Pre-create gray frame buffer
    frame_skip = 2  # Capture every 2nd frame for speed
    frame_num = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            break
        
        frame_num += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Only process every Nth frame
        if frame_num % frame_skip == 0:
            faces = face_detector.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(80, 80)
            )

            if len(faces) == 1:
                (x, y, w, h) = faces[0]
                face_roi = gray[y:y+h, x:x+w]
                face_processed = preprocess_face(face_roi)
                
                count += 1
                filename = os.path.join(person_dir, f"face_{count}.jpg")
                # Use optimized JPEG parameters
                cv2.imwrite(filename, face_processed, [cv2.IMWRITE_JPEG_QUALITY, 95])
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                cv2.putText(frame, f"Captured: {count}/50", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            elif len(faces) > 1:
                skipped += 1
                cv2.putText(frame, "Multiple faces detected! Show only one face.", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "No face detected. Move closer.", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.putText(frame, f"Progress: {count}/50 (Skipped: {skipped})", 
                   (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.imshow(f"Enrolling: {name} - Press Q when done", frame)
        
        key = cv2.waitKey(30) & 0xFF
        if key == ord('q'):
            if count >= 20:
                break
            else:
                messagebox.showwarning("Warning", f"Only {count} images captured. Need at least 20. Continue...")
        elif count >= 50:
            break

    cam.release()
    cv2.destroyAllWindows()

    if count < 20:
        messagebox.showerror("Error", f"Only {count} images captured. Need at least 20 for good accuracy.\nDeleting enrollment...")
        delete_person(person_id)
        import shutil
        shutil.rmtree(person_dir)
        return

    print(f"\n✓ Captured {count} images for {name} (ID: {person_id})")
    messagebox.showinfo("Training", "Training model with all enrolled persons...\nThis may take a moment.")
    
    # Clear caches before training
    get_name_map.cache_clear()
    fetch_all_persons_cached.cache_clear()
    
    if train_model():
        messagebox.showinfo("Success", f"{name} enrolled successfully!\n\nCaptured: {count} face samples\nID: {person_id}")
    else:
        messagebox.showerror("Error", "Training failed! Check console for details.")

# ====== GUI ======
def view_db():
    rows = fetch_all_persons_cached()
    if not rows:
        messagebox.showinfo("Database", "No persons enrolled.")
        return
    
    win = tk.Toplevel()
    win.title("Enrolled Persons")
    win.geometry("700x400")
    
    cols = ("ID", "Name", "Note", "Created At")
    tree = ttk.Treeview(win, columns=cols, show="headings", height=15)
    
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Note", text="Note")
    tree.heading("Created At", text="Created At")
    
    tree.column("ID", width=50)
    tree.column("Name", width=150)
    tree.column("Note", width=200)
    tree.column("Created At", width=180)
    
    for row in rows:
        tree.insert("", "end", values=row)
    
    scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y", pady=10)
    
    ttk.Button(win, text="Close", command=win.destroy).pack(pady=5)

def retrain_model():
    result = messagebox.askyesno("Retrain Model", "This will retrain the model with all enrolled persons.\n\nContinue?")
    if result:
        messagebox.showinfo("Training", "Training in progress...")
        get_name_map.cache_clear()
        fetch_all_persons_cached.cache_clear()
        
        if train_model():
            messagebox.showinfo("Success", "Model retrained successfully!")
        else:
            messagebox.showerror("Error", "Training failed! Check if persons are enrolled.")

def main():
    root = tk.Tk()
    root.title("Advanced Face Recognition System")
    root.geometry("450x280")
    
    frame = ttk.Frame(root, padding=20)
    frame.pack(fill="both", expand=True)

    title = ttk.Label(frame, text="Face Recognition System", 
                     font=("Arial", 16, "bold"))
    title.pack(pady=15)
    
    ttk.Button(frame, text="📷 Enroll New Person", 
              command=enroll_person, width=30).pack(pady=5)
    ttk.Button(frame, text="🔍 Start Recognition", 
              command=recognize_faces, width=30).pack(pady=5)
    ttk.Button(frame, text="📊 View Database", 
              command=view_db, width=30).pack(pady=5)
    ttk.Button(frame, text="🔄 Retrain Model", 
              command=retrain_model, width=30).pack(pady=5)
    ttk.Button(frame, text="❌ Exit", 
              command=root.destroy, width=30).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
