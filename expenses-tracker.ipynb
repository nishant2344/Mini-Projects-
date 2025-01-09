
import sqlite3
import bcrypt
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime

# Database setup
DB_FILE = "expense_tracker.db"

def init_db():
    """Initialize the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

# User authentication
def register():
    """Register a new user."""
    username = input("Enter a username: ")
    password = input("Enter a password: ").encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    conn.close()

def login():
    """Login an existing user."""
    username = input("Enter your username: ")
    password = input("Enter your password: ").encode('utf-8')
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password, user[1]):
        print("Login successful!")
        return user[0]
    else:
        print("Invalid username or password.")
        return None

# Expense management
def add_expense(user_id):
    """Add a new expense."""
    date = input("Enter the date (YYYY-MM-DD): ")
    category = input("Enter the category (e.g., Food, Rent): ")
    amount = float(input("Enter the amount: "))
    notes = input("Enter any notes (optional): ")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (user_id, date, category, amount, notes) 
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, date, category, amount, notes))
    conn.commit()
    conn.close()
    print("Expense added successfully!")

def view_expenses(user_id):
    """View all expenses."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT date, category, amount, notes FROM expenses WHERE user_id = ?", (user_id,))
    expenses = cursor.fetchall()
    conn.close()
    if expenses:
        print("\nYour Expenses:")
        for expense in expenses:
            print(f"Date: {expense[0]}, Category: {expense[1]}, Amount: {expense[2]}, Notes: {expense[3]}")
    else:
        print("No expenses found.")

def delete_expense(user_id):
    """Delete an expense."""
    view_expenses(user_id)
    expense_id = int(input("Enter the ID of the expense to delete: "))
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (expense_id, user_id))
    conn.commit()
    conn.close()
    print("Expense deleted successfully!")

# Data visualization
def visualize_expenses(user_id):
    """Visualize expenses."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE user_id = ? GROUP BY category", (user_id,))
    data = cursor.fetchall()
    conn.close()
    if data:
        categories, amounts = zip(*data)
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title("Expenses by Category")
        plt.show()
    else:
        print("No expenses to visualize.")

# Export and import
def export_expenses(user_id):
    """Export expenses to a CSV file."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT date, category, amount, notes FROM expenses WHERE user_id = ?", (user_id,))
    expenses = cursor.fetchall()
    conn.close()
    if expenses:
        filename = f"expenses_{user_id}.csv"
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Notes"])
            writer.writerows(expenses)
        print(f"Expenses exported to {filename}.")
    else:
        print("No expenses to export.")

def import_expenses(user_id):
    """Import expenses from a CSV file."""
    filename = input("Enter the CSV file path: ")
    if os.path.exists(filename):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        with open(filename, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                cursor.execute("""
                    INSERT INTO expenses (user_id, date, category, amount, notes) 
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, row[0], row[1], float(row[2]), row[3]))
        conn.commit()
        conn.close()
        print("Expenses imported successfully!")
    else:
        print("File not found.")

# Main menu
def main():
    init_db()
    user_id = None
    while not user_id:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            register()
        elif choice == "2":
            user_id = login()
        elif choice == "3":
            print("Goodbye!")
            exit()
        else:
            print("Invalid option.")

    while True:
        print("\n1. Add Expense\n2. View Expenses\n3. Delete Expense\n4. Visualize Expenses")
        print("5. Export Expenses\n6. Import Expenses\n7. Logout")
        choice = input("Choose an option: ")
        if choice == "1":
            add_expense(user_id)
        elif choice == "2":
            view_expenses(user_id)
        elif choice == "3":
            delete_expense(user_id)
        elif choice == "4":
            visualize_expenses(user_id)
        elif choice == "5":
            export_expenses(user_id)
        elif choice == "6":
            import_expenses(user_id)
        elif choice == "7":
            print("Logged out.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
