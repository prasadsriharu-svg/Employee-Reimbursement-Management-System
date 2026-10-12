from getpass import getpass
from database import create_user, get_user_by_username

username = input("Enter Admin username: ").strip()

if not username:
    print("Username cannot be empty.")

elif get_user_by_username(username):
    print("Username already exists.")

else:
    password = getpass("Enter Admin password: ")

    if len(password) < 8:
        print("Password must contain at least 8 characters.")
    else:
        create_user(
            employee_name="System Administrator",
            username=username,
            password=password,
            role="Admin"
        )

        print("Admin user created successfully!")