try:
    import os
    import re
    import requests
except ImportError:
    print("Some packages is not installed.")
    print("Please install it by running: pip install -r client/requirements.txt")
    exit()
    
    
BASE_URL = os.getenv("ADET_API_BASE_URL", "http://localhost/adet-rest-api/server/service.php")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def print_response(response):
    try:
        data = response.json()
        print("\n--- SERVER RESPONSE ---")
        print(f"HTTP Status: {response.status_code}")
        print(f"Status: {data.get('status')}")
        print(f"Message: {data.get('message')}")

        if data.get("data") is not None:
            print("Data:")
            if isinstance(data["data"], list):
                for item in data["data"]:
                    print(item)
            else:
                print(data["data"])
        if response.status_code >= 400:
            print("Note: The server reported an HTTP error.")
        print("-----------------------\n")
    except ValueError:
        print("\nError: Server did not return valid JSON.")
        print("Raw response:", response.text)


def prompt_user_id(prompt_text):
    while True:
        user_id = input(prompt_text).strip()
        if not user_id:
            print("User ID cannot be empty.")
            continue
        if not user_id.isdigit() or int(user_id) <= 0:
            print("User ID must be a positive number.")
            continue
        return user_id


def prompt_non_empty(prompt_text, field_label):
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print(f"{field_label} cannot be empty.")


def prompt_email(prompt_text="Enter new email: "):
    while True:
        email = input(prompt_text).strip()
        if not email:
            print("Email cannot be empty.")
            continue
        if not EMAIL_PATTERN.match(email):
            print("Please enter a valid email address.")
            continue
        return email


def confirm_action(prompt_text):
    confirmation = input(prompt_text).strip().lower()
    return confirmation in {"y", "yes"}


def send_user_request(method, action, params=None, payload=None):
    request_params = {"action": action}
    if params:
        request_params.update(params)

    try:
        response = requests.request(
            method=method,
            url=BASE_URL,
            params=request_params,
            json=payload,
            timeout=10,
        )
        print_response(response)
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API server.")
    except requests.exceptions.Timeout:
        print("\nError: Request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"\nUnexpected error: {e}")


def get_all_users():
    send_user_request("GET", "users")


def get_user_by_id():
    user_id = prompt_user_id("Enter user ID: ")
    send_user_request("GET", "user", params={"id": user_id})


def update_user():
    user_id = prompt_user_id("Enter user ID to update: ")
    username = prompt_non_empty("Enter new username: ", "Username")
    email = prompt_email("Enter new email: ")

    payload = {
        "username": username,
        "email": email
    }

    send_user_request("PUT", "update_user", params={"id": user_id}, payload=payload)


def delete_user():
    user_id = prompt_user_id("Enter user ID to delete: ")
    if not confirm_action(f"Are you sure you want to delete user ID {user_id}? (y/N): "):
        print("Delete action canceled.")
        return

    send_user_request("DELETE", "delete_user", params={"id": user_id})


def main():
    while True:
        print("=== USER MANAGEMENT CLIENT ===")
        print("1. Get all users")
        print("2. Get user by ID")
        print("3. Update user")
        print("4. Delete user")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            get_all_users()
        elif choice == "2":
            get_user_by_id()
        elif choice == "3":
            update_user()
        elif choice == "4":
            delete_user()
        elif choice == "5":
            print("Exiting user management client.")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()