import cv2
import os
import numpy as np
import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime

# ====== MySQL Config ======
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "***************",
    "database": "face_recog_db"
}
# ===========================

DATASET_DIR = "dataset"
TRAINER_FILE = "trainer.yml"
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR)

# ====== DB Helpers ======
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def insert_person(name, note=None):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql = "INSERT INTO persons (name, note) VALUES (%s, %s)"
        cur.execute(sql, (name, note))
        conn.commit()
        person_id = cur.lastrowid
        cur.close()
        conn.close()
        return person_id
    except Error as e:
        print("DB Error:", e)
        return None

def fetch_all_persons():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, note, created_at FROM persons ORDER BY id")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Error as e:
        print("DB fetch error:", e)
        return []

# ====== Training ======
def get_images_and_labels(dataset_path):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces = []
    ids = []
    face_detector = cv2.CascadeClassifier(CASCADE_PATH)

    for person_dir in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_dir)
        if not os.path.isdir(person_path):
            continue
        person_id = int(person_dir.split("_")[0])
        for image_file in os.listdir(person_path):
            img_path = os.path.join(person_path, image_file)
            gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if gray is None:
                continue
            faces_detected = face_detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces_detected:
                faces.append(gray[y:y+h, x:x+w])
                ids.append(person_id)

    if len(faces) == 0:
        return None, None
    return faces, ids

def train_model():
    faces, ids = get_images_and_labels(DATASET_DIR)
    if faces is None:
        print("No faces found to train.")
        return False
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(ids))
    recognizer.save(TRAINER_FILE)
    print("Model trained successfully.")
    return True

# ====== Recognition ======
def recognize_faces():
    if not os.path.exists(TRAINER_FILE):
        messagebox.showwarning("No Model", "Please enroll and train first!")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(TRAINER_FILE)
    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM persons")
    name_map = {row[0]: row[1] for row in cur.fetchall()}
    cur.close()
    conn.close()

    cam = cv2.VideoCapture(0)
    messagebox.showinfo("Recognition", "Press Q to stop recognition.")

    while True:
        ret, frame = cam.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            id_, confidence = recognizer.predict(roi_gray)
            if confidence < 80:  # smaller = better match
                name = name_map.get(id_, "Unknown")
                label = f"{name} ({round(confidence, 2)})"
                color = (0, 255, 0)
            else:
                label = "Unknown"
                color = (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

# ====== Enrollment ======
def enroll_person():
    name = simpledialog.askstring("Enroll", "Enter person name:")
    if not name:
        return
    note = simpledialog.askstring("Enroll", "Enter note (optional):")
    person_id = insert_person(name, note)
    if not person_id:
        messagebox.showerror("DB Error", "Failed to save person to DB.")
        return

    face_detector = cv2.CascadeClassifier(CASCADE_PATH)
    cam = cv2.VideoCapture(0)
    messagebox.showinfo("Instructions", "Look at the camera. Press Q to stop capturing.")

    count = 0
    person_dir = os.path.join(DATASET_DIR, f"{person_id}_{name}")
    os.makedirs(person_dir, exist_ok=True)

    while True:
        ret, frame = cam.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            face_img = gray[y:y+h, x:x+w]
            cv2.imwrite(os.path.join(person_dir, f"{count}.jpg"), face_img)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Captured {count}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        cv2.imshow("Enrollment", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif count >= 25:  # capture 25 images per person
            break

    cam.release()
    cv2.destroyAllWindows()

    messagebox.showinfo("Training", "Training model, please wait...")
    train_model()
    messagebox.showinfo("Success", f"{name} enrolled successfully!")

# ====== GUI ======
def view_db():
    rows = fetch_all_persons()
    if not rows:
        messagebox.showinfo("Database", "No persons enrolled.")
        return
    win = tk.Toplevel()
    win.title("Enrolled Persons")
    cols = ("ID", "Name", "Note", "Created At")
    tree = ttk.Treeview(win, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=120)
    for row in rows:
        tree.insert("", "end", values=row)
    tree.pack(fill="both", expand=True)
    ttk.Button(win, text="Close", command=win.destroy).pack(pady=5)

def main():
    root = tk.Tk()
    root.title("Face Recognition - OpenCV LBPH")
    root.geometry("360x200")
    frame = ttk.Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    ttk.Button(frame, text="Enroll Person", command=enroll_person).pack(fill="x", pady=5)
    ttk.Button(frame, text="Start Recognition", command=recognize_faces).pack(fill="x", pady=5)
    ttk.Button(frame, text="View Database", command=view_db).pack(fill="x", pady=5)
    ttk.Button(frame, text="Exit", command=root.destroy).pack(fill="x", pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
