import re

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

def main():
    print("Password Strength Checker")
    print("-------------------------")

    # Get username and password from the user
    username = input("Enter your username: ")

    while True:
        password = input("Enter your password: ")
        weaknesses = check_password_strength(username, password)

        if not weaknesses:
            print("Strong: Your password is strong!")
            break
        else:
            print("Weaknesses:")
            for weakness in weaknesses:
                print(f"- {weakness}")

            choice = input("Do you want to change your password to a stronger one? (yes/no): ").strip().lower()
            if choice == "yes":
                suggested_password = suggest_stronger_password(password)
                print(f"Suggested stronger password: {suggested_password}")

if __name__ == "__main__":
    main()
