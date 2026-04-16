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


def get_all_api_keys():
    try:
        response = requests.get(f"{BASE_URL}?action=api_keys", timeout=10)
        print_response(response)
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API server.")
    except requests.exceptions.Timeout:
        print("\nError: Request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"\nUnexpected error: {e}")

def delete_api_key():
    key = input("Enter API key to delete: ").strip()
    try:
        response = requests.delete(f"{BASE_URL}?action=delete_api_key&api_key={key}", timeout=10)
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
        print("1. Get all API keys")
        print("2. Delete API key")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            get_all_api_keys()
        elif choice == "2":
            delete_api_key()
        elif choice == "3":
            print("Exiting API key management client.")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()