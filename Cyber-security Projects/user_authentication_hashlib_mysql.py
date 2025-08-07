import mysql.connector
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#connect with SQL DATABASE
conn = mysql.connector.connect(
    host="localhost",
    user="collegewala",
    password="********",     
    database="user_authentication_hashlib_mysql"        
)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id VARCHAR(255) PRIMARY KEY,
        password_hash VARCHAR(255) NOT NULL
    )
''')

def add_user(user_id, password):
    password_hash = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (user_id, password_hash) VALUES (%s, %s)", (user_id, password_hash))
        conn.commit()
        print(f" User '{user_id}' registered successfully.")
    except mysql.connector.errors.IntegrityError:
        print(f" User-ID '{user_id}' already exists.")


def authenticate(user_id, password):
    cursor.execute("SELECT password_hash FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()

    if result:
        if hash_password(password) == result[0]:
            print(" Authentication successful.")
        else:
            print(" Invalid password.")
    else:
        print(" User-ID not found.")


print("1. Register\n2. Login")
choice = input("Enter your choice (1 or 2): ")

if choice == '1':
    uid = input("Enter new User-ID: ")
    pwd = input("Enter new Password: ")
    add_user(uid, pwd)

elif choice == '2':
    uid = input("Enter User-ID: ")
    pwd = input("Enter Password: ")
    authenticate(uid, pwd)

else:
    print(" Invalid choice.")

# Close DB connection properly 
cursor.close()
conn.close()

