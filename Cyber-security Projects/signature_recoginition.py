"""
Simple Fingerprint Matcher
- Load JPG fingerprint images
- Extract basic features
- Compare and show similarity
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import numpy as np
from PIL import Image, ImageTk
import cv2

class SimpleFingerprintMatcher:
    def __init__(self, master):
        self.master = master
        master.title("Fingerprint Matcher")
        master.geometry("600x500")

        # Image storage
        self.current_img = None
        self.img1 = None
        self.img2 = None
        
        self.setup_gui()

    def setup_gui(self):
        # Image display
        self.canvas = tk.Canvas(self.master, width=300, height=300, bg='lightgray')
        self.canvas.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(self.master)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Load Image", command=self.load_image, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Set as Image 1", command=lambda: self.set_image(1), width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Set as Image 2", command=lambda: self.set_image(2), width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Compare", command=self.compare, width=12).pack(side=tk.LEFT, padx=5)

        # Status
        self.status = tk.Label(self.master, text="Load two fingerprint images to compare")
        self.status.pack(pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            img = Image.open(file_path).convert('L').resize((300, 300))
            self.current_img = np.array(img)
            self.display_image(img)
            self.status.config(text=f"Loaded: {os.path.basename(file_path)}")

    def display_image(self, img):
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(150, 150, image=self.photo)

    def set_image(self, num):
        if self.current_img is not None:
            if num == 1:
                self.img1 = self.current_img.copy()
                self.status.config(text="Image 1 set")
            else:
                self.img2 = self.current_img.copy()
                self.status.config(text="Image 2 set")

    def extract_features(self, img):
        """Simple feature extraction"""
        features = {}
        features['mean'] = np.mean(img)
        features['std'] = np.std(img)
        
        # Simple edge detection
        edges = cv2.Canny(img, 50, 150)
        features['edge_density'] = np.sum(edges > 0) / edges.size
        
        # Texture - simple variance
        features['texture'] = np.var(img)
        
        return features

    def compare(self):
        if self.img1 is None or self.img2 is None:
            messagebox.showwarning("Error", "Please load and set both images first")
            return

        features1 = self.extract_features(self.img1)
        features2 = self.extract_features(self.img2)

        # Simple similarity calculation
        similarity = 0
        for key in features1:
            diff = abs(features1[key] - features2[key])
            max_val = max(abs(features1[key]), abs(features2[key]))
            if max_val > 0:
                similarity += (1 - diff/max_val) / len(features1)

        similarity = max(0, min(1, similarity))
        
        result = f"Similarity: {similarity*100:.1f}%\n"
        if similarity > 0.7:
            result += "✅ Likely Match"
        elif similarity > 0.4:
            result += "⚠️ Possible Match"
        else:
            result += "❌ Different"

        messagebox.showinfo("Comparison Result", result)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleFingerprintMatcher(root)
    root.mainloop()