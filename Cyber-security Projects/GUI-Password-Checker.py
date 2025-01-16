import re
import tkinter as tk
from tkinter import messagebox

def check_password_strength(username, password):
    weaknesses = []

    # Check password length
    if len(password) < 8:
        weaknesses.append("Password must be at least 8 characters long.")

    # Check if password contains username
    if username.lower() in password.lower():
        weaknesses.append("Password should not contain the username.")

    # Check for presence of a digit
    if not re.search(r"\d", password):
        weaknesses.append("Password must include at least one digit.")

    # Check for presence of a special character
    if not re.search(r"[@$!%*?&#]", password):
        weaknesses.append("Password must include at least one special character (e.g., @, $, !, %, *, ?, &).")

    # Check for presence of an uppercase letter
    if not re.search(r"[A-Z]", password):
        weaknesses.append("Password must include at least one uppercase letter.")

    # Check for presence of a lowercase letter
    if not re.search(r"[a-z]", password):
        weaknesses.append("Password must include at least one lowercase letter.")

    return weaknesses

def suggest_stronger_password(password):
    # Suggest a stronger password based on the given password
    suggested_password = password

    if len(suggested_password) < 8:
        suggested_password += "A1@abc"

    if not re.search(r"\d", suggested_password):
        suggested_password += "1"

    if not re.search(r"[@$!%*?&#]", suggested_password):
        suggested_password += "@"

    if not re.search(r"[A-Z]", suggested_password):
        suggested_password += "A"

    if not re.search(r"[a-z]", suggested_password):
        suggested_password += "a"

    return suggested_password

def check_password():
    username = username_entry.get()
    password = password_entry.get()
    weaknesses = check_password_strength(username, password)

    if not weaknesses:
        messagebox.showinfo("Password Strength", "Strong: Your password is strong!")
    else:
        messagebox.showwarning("Password Weaknesses", "\n".join(weaknesses))
        if messagebox.askyesno("Suggestion", "Do you want a stronger password suggestion?"):
            suggested_password = suggest_stronger_password(password)
            suggestion_label.config(text=f"Suggested Password: {suggested_password}")

def create_gui():
    global username_entry, password_entry, suggestion_label

    root = tk.Tk()
    root.title("Password Strength Checker")

    tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(root, width=30)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(root, width=30, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(root, text="Check Password", command=check_password).grid(row=2, column=0, columnspan=2, pady=10)

    suggestion_label = tk.Label(root, text="", fg="blue")
    suggestion_label.grid(row=3, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
