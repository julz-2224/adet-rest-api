import os
import re
from getpass import getpass

try:
    import requests
except ImportError:
    print("The 'requests' package is not installed.")
    print("Please install it by running: pip install -r client/requirements.txt")
    exit()
    
    
BASE_URL = os.getenv("ADET_API_BASE_URL", "http://localhost/adet-rest-api/server/service.php")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MIN_PASSWORD_LENGTH = 8


def print_response(response):
    try:
        data = response.json()
        print("\n--- SERVER RESPONSE ---")
        print(f"HTTP Status: {response.status_code}")
        print(f"Status: {data.get('status')}")
        print(f"Message: {data.get('message')}")
        if data.get("data") is not None:
            print("Data:", data.get("data"))
        if response.status_code >= 400:
            print("Note: The server reported an HTTP error.")
        print("-----------------------\n")
    except ValueError:
        print("\nError: Server did not return valid JSON.")
        print("Raw response:", response.text)


def prompt_non_empty(field_name):
    while True:
        value = input(f"Enter {field_name}: ").strip()
        if value:
            return value
        print(f"{field_name.capitalize()} cannot be empty.")


def prompt_email():
    while True:
        email = input("Enter email: ").strip()
        if not email:
            print("Email cannot be empty.")
            continue
        if not EMAIL_PATTERN.match(email):
            print("Please enter a valid email address.")
            continue
        return email


def prompt_password(confirm=False):
    while True:
        password = getpass("Enter password: ").strip()
        if not password:
            print("Password cannot be empty.")
            continue
        if len(password) < MIN_PASSWORD_LENGTH:
            print(f"Password must be at least {MIN_PASSWORD_LENGTH} characters.")
            continue
        if confirm:
            confirm_password = getpass("Confirm password: ").strip()
            if password != confirm_password:
                print("Passwords do not match. Please try again.")
                continue
        return password


def send_auth_request(action, payload):
    try:
        response = requests.post(f"{BASE_URL}?action={action}", json=payload, timeout=10)
        print_response(response)
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API server.")
    except requests.exceptions.Timeout:
        print("\nError: Request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"\nUnexpected error: {e}")


def register():
    print("\n=== USER REGISTRATION ===")
    username = prompt_non_empty("username")
    email = prompt_email()
    password = prompt_password(confirm=True)

    payload = {
        "username": username,
        "email": email,
        "password": password
    }

    send_auth_request("register", payload)


def login():
    print("\n=== USER LOGIN ===")
    email = prompt_email()
    password = prompt_password()

    payload = {
        "email": email,
        "password": password
    }

    send_auth_request("login", payload)


def main():
    while True:
        print("=== AUTH CLIENT ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Exiting auth client.")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()