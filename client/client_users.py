try:
    import requests
except ImportError:
    print("The 'requests' package is not installed.")
    print("Please install it by running: pip install -r client/requirements.txt")
    exit()
    
    
BASE_URL = "http://localhost/adet-rest-api/server/service.php"


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
        print("-----------------------\n")
    except ValueError:
        print("\nError: Server did not return valid JSON.")
        print("Raw response:", response.text)


def get_all_users():
    try:
        response = requests.get(f"{BASE_URL}?action=users", timeout=10)
        print_response(response)
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API server.")
    except requests.exceptions.Timeout:
        print("\nError: Request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"\nUnexpected error: {e}")


def get_user_by_id():
    user_id = input("Enter user ID: ").strip()

    try:
        response = requests.get(f"{BASE_URL}?action=user&id={user_id}", timeout=10)
        print_response(response)
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API server.")
    except requests.exceptions.Timeout:
        print("\nError: Request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"\nUnexpected error: {e}")


def update_user():
    user_id = input("Enter user ID to update: ").strip()
    username = input("Enter new username: ").strip()
    email = input("Enter new email: ").strip()

    payload = {
        "username": username,
        "email": email
    }

    try:
        response = requests.put(f"{BASE_URL}?action=update_user&id={user_id}", json=payload, timeout=10)
        print_response(response)
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API server.")
    except requests.exceptions.Timeout:
        print("\nError: Request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"\nUnexpected error: {e}")


def delete_user():
    user_id = input("Enter user ID to delete: ").strip()

    try:
        response = requests.delete(f"{BASE_URL}?action=delete_user&id={user_id}", timeout=10)
        print_response(response)
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API server.")
    except requests.exceptions.Timeout:
        print("\nError: Request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"\nUnexpected error: {e}")


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