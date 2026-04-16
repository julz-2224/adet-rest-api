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
            print("Data:", data.get("data"))
        print("-----------------------\n")
    except ValueError:
        print("\nError: Server did not return valid JSON.")
        print("Raw response:", response.text)


def generate_api():
    print("\n=== API KEY GENERATION ===")
    payload = {}
    try:
        response = requests.post(f"{BASE_URL}?action=generate_api", json=payload, timeout=10)
        print_response(response)
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API server.")
    except requests.exceptions.Timeout:
        print("\nError: Request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"\nUnexpected error: {e}")


def execute_ai():
    print("\n=== AI EXECUTION===")
    api_key = input("Enter API key: ").strip()
    month = input("Enter month: ").strip()
    raw = input("Is raw?(Y/n): ").strip()

    if raw.lower() == "n":
        raw = False
    else:
        raw = True

    payload = {
        "api_key": api_key,
        "month": int(month),
        "raw": raw
    }

    print(payload)
    try:
        response = requests.post(f"{BASE_URL}?action=execute_ai", json=payload, timeout=10)
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
        print("1. API key generation")
        print("2. Execute AI")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            generate_api()
        elif choice == "2":
            execute_ai()
        elif choice == "3":
            print("Exiting auth/execute client.")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()