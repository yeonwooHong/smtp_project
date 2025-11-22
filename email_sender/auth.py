from email_sender.user import User
from email_sender.colors import Colors

# Global session variable
current_user = None


def register():
    print("\n--- Register ---")
    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()

    # Check if user exists
    if User.objects.filter(email=email).exists():
        print(f"{Colors.RED}User already exists.{Colors.END}")
        return None

    user = User(email=email)
    user.set_password(password)
    user.save()
    print(f"{Colors.GREEN}User registered successfully.{Colors.END}")

    return "registered"


def login():
    global current_user

    print("\n--- Login ---")
    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        print(f"{Colors.RED}User not found.{Colors.END}")
        return

    if user.check_password(password):
        current_user = user
        print(f"{Colors.GREEN}Welcome, {user.email}!{Colors.END}")
        return "logged_in"
    else:
        print(f"{Colors.RED}Incorrect password.{Colors.END}")


def logout():
    global current_user
    current_user = None
    print(f"{Colors.YELLOW}You have been logged out.{Colors.END}")
    return "logged_out"