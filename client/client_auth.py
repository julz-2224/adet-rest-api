try:
    import requests
except ImportError:
    print("The 'requests' package is not installed.")
    print("Please install it by running: pip install -r client/requirements.txt")
    exit()
    
    
BASE_URL = "http://localhost/user-api"


def print_response(response):
    try:
        data = response.json()
        print("\n--- SERVER RESPONSE ---")
        print(f"HTTP Status: {response.status_code}")
        print(f"Status: {data.get('status')}")
        print(f"Message: {data.get('message')}")
        if data.get("data") is not None:
            print("Data:", data.get("data"))
        print("-----------------------\n")
    except ValueError:
        print("\nError: Server did not return valid JSON.")
        print("Raw response:", response.text)


def register():
    print("\n=== USER REGISTRATION ===")
    username = input("Enter username: ").strip()
    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()

    payload = {
        "username": username,
        "email": email,
        "password": password
    }

    try:
        response = requests.post(f"{BASE_URL}/register", json=payload, timeout=10)
        print_response(response)
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API server.")
    except requests.exceptions.Timeout:
        print("\nError: Request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"\nUnexpected error: {e}")


def login():
    print("\n=== USER LOGIN ===")
    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()

    payload = {
        "email": email,
        "password": password
    }

    try:
        response = requests.post(f"{BASE_URL}/login", json=payload, timeout=10)
        print_response(response)
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API server.")
    except requests.exceptions.Timeout:
        print("\nError: Request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"\nUnexpected error: {e}")


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