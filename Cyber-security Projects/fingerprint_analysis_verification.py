import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import mysql.connector
import numpy as np
from skimage.morphology import skeletonize


# ----------------- Database Setup -----------------
def connect_db():
    try:
        cnx = mysql.connector.connect(
            host="localhost",
            user="root",        # <-- Change to your MySQL username
            password="042905",  # <-- Change to your MySQL password
            database="fingerprints_db"  # <-- Change to your DB name
        )
        return cnx
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None


# ----------------- Minutiae Extraction -----------------
def extract_minutiae(processed_img):
    binary = processed_img == 0   # binary conversion
    skeleton = skeletonize(binary)  # thin ridges

    minutiae_end = []
    minutiae_bif = []

    rows, cols = skeleton.shape
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if skeleton[i, j]:
                neighbors = [
                    skeleton[i-1, j-1], skeleton[i-1, j], skeleton[i-1, j+1],
                    skeleton[i, j-1],                   skeleton[i, j+1],
                    skeleton[i+1, j-1], skeleton[i+1, j], skeleton[i+1, j+1]
                ]
                crossing_number = np.sum(neighbors)

                if crossing_number == 1:   # Ridge ending
                    minutiae_end.append((i, j))
                elif crossing_number > 2:  # Bifurcation
                    minutiae_bif.append((i, j))

    return minutiae_end, minutiae_bif, skeleton


def draw_minutiae(processed_img, minutiae_end, minutiae_bif):
    img_color = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2BGR)

    # Ridge endings (red)
    for (y, x) in minutiae_end:
        cv2.circle(img_color, (x, y), 3, (0, 0, 255), -1)

    # Bifurcations (green)
    for (y, x) in minutiae_bif:
        cv2.circle(img_color, (x, y), 3, (0, 255, 0), -1)

    return img_color


# ----------------- GUI App Class -----------------
class FingerprintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fingerprint System (Enroll + Verify)")
        self.root.geometry("700x550")

        self.image_path = None

        # Student Name
        tk.Label(root, text="Student Name (for enrollment):", font=("Arial", 12)).pack(pady=5)
        self.name_entry = tk.Entry(root, font=("Arial", 12), width=40)
        self.name_entry.pack(pady=5)

        # Canvas for image preview
        self.canvas = tk.Canvas(root, width=400, height=300, bg="lightgray")
        self.canvas.pack(pady=10)
        self.canvas.create_text(200, 150, text="No Image Selected", fill="black", font=("Arial", 14))

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Select Image", command=self.select_image).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Enroll Fingerprint", command=self.process_and_save).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Verify Fingerprint", command=self.verify_fingerprint).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Exit", command=root.quit).grid(row=0, column=3, padx=5)

        # Status Label
        self.status_label = tk.Label(root, text="", fg="green", font=("Arial", 11))
        self.status_label.pack(pady=5)

    # -------- Select fingerprint image --------
    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:
            self.image_path = file_path
            self.display_image(file_path)
            self.status_label.config(text="Image Loaded", fg="blue")

    # -------- Display image on canvas --------
    def display_image(self, path):
        img = Image.open(path)
        img.thumbnail((400, 300))
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(200, 150, image=self.tk_img)

    # -------- Fingerprint preprocessing --------
    def process_fingerprint(self, img_path):
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.GaussianBlur(img, (3, 3), 0)
        _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        return thresh

    # -------- Save to DB --------
    def save_to_db(self, name, image_bytes):
        cnx = connect_db()
        if cnx is None:
            return

        try:
            cursor = cnx.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    fingerprint LONGBLOB
                )
            """)
            cursor.execute("INSERT INTO students (name, fingerprint) VALUES (%s, %s)", (name, image_bytes))
            cnx.commit()
            cursor.close()
            cnx.close()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Error: {err}")
            return False

    # -------- Enroll Fingerprint --------
    def process_and_save(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter student name")
            return
        if not self.image_path:
            messagebox.showwarning("Input Error", "Please select a fingerprint image")
            return

        # Process fingerprint
        processed = self.process_fingerprint(self.image_path)

        # Extract minutiae
        minutiae_end, minutiae_bif, skeleton = extract_minutiae(processed)

        # Draw minutiae
        img_with_minutiae = draw_minutiae(processed, minutiae_end, minutiae_bif)

        # Show image in GUI
        img_rgb = cv2.cvtColor(img_with_minutiae, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil.thumbnail((400, 300))
        self.tk_img = ImageTk.PhotoImage(img_pil)
        self.canvas.create_image(200, 150, image=self.tk_img)

        # Show numbers
        msg = f"Ridge Endings: {len(minutiae_end)}, Bifurcations: {len(minutiae_bif)}"
        self.status_label.config(text=msg, fg="purple")
        messagebox.showinfo("Minutiae Points", msg)

        # Save fingerprint image to DB
        success, encoded_img = cv2.imencode('.png', processed)
        if success:
            img_bytes = encoded_img.tobytes()
            if self.save_to_db(name, img_bytes):
                self.status_label.config(text=f"Saved: {name} | {msg}", fg="green")
                messagebox.showinfo("Success", f"Fingerprint saved with {msg}")

    # -------- Compare Minutiae Sets --------
    def compare_minutiae(self, set1, set2, tolerance=10):
        matches = 0
        for (y1, x1) in set1:
            for (y2, x2) in set2:
                if abs(x1 - x2) <= tolerance and abs(y1 - y2) <= tolerance:
                    matches += 1
                    break
        total_points = max(len(set1), len(set2))
        return matches / total_points if total_points > 0 else 0

    # -------- Verify Fingerprint --------
    def verify_fingerprint(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if not file_path:
            return

        # Preprocess input fingerprint
        processed_input = self.process_fingerprint(file_path)
        minutiae_end_in, minutiae_bif_in, _ = extract_minutiae(processed_input)
        input_points = set(minutiae_end_in + minutiae_bif_in)

        # Fetch all fingerprints from DB
        cnx = connect_db()
        if cnx is None:
            return
        cursor = cnx.cursor()
        cursor.execute("SELECT name, fingerprint FROM students")
        records = cursor.fetchall()
        cursor.close()
        cnx.close()

        best_match = None
        best_score = 0

        for name, blob in records:
            # Decode DB image
            nparr = np.frombuffer(blob, np.uint8)
            db_img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

            # Extract minutiae from DB fingerprint
            minutiae_end_db, minutiae_bif_db, _ = extract_minutiae(db_img)
            db_points = set(minutiae_end_db + minutiae_bif_db)

            # Compare
            score = self.compare_minutiae(input_points, db_points)
            if score > best_score:
                best_score = score
                best_match = (name, db_img)

        if best_match and best_score > 0.6:  # 60% threshold
            name, matched_img = best_match

            # Show matched fingerprint
            img_rgb = cv2.cvtColor(matched_img, cv2.COLOR_GRAY2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_pil.thumbnail((400, 300))
            self.tk_img = ImageTk.PhotoImage(img_pil)
            self.canvas.create_image(200, 150, image=self.tk_img)

            msg = f"Match Found: {name} (Score: {best_score:.2f})"
            self.status_label.config(text=msg, fg="green")
            messagebox.showinfo("Verification Result", msg)
        else:
            messagebox.showwarning("Verification Failed", "No matching fingerprint found.")
            self.status_label.config(text="No Match Found", fg="red")


# ----------------- Run App -----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = FingerprintApp(root)
    root.mainloop()
