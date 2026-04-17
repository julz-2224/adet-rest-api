import socket
import random
import json

## fix: 1024 buffer limit size corrupting data exchange, now can exchange data beyond 1024 bytes
def safe_send(sock, obj):
    # newline framing, uses newline for sending response. much safer 
    try:
        data = (json.dumps(obj) + "\n").encode("utf-8")
        sock.sendall(data)
    except Exception as e:
        print(f"Send error: {e}")


def handle_client(c_socket):
    buffer = ""
    while True:
        try:
            chunk = c_socket.recv(1024)
        except ConnectionResetError:
            print("Client forcefully disconnected")
            break
        except OSError:
            print("Socket error")
            break

        if not chunk:
            print("Client closed connection")
            break

        buffer += chunk.decode("utf-8")

        while "\n" in buffer:
            # separate message from leftovers(buffer)
            message, buffer = buffer.split("\n", 1)
            message = message.strip()
            # for debugging
            # print("RAW MESSAGE:", repr(message))
            if not message:
                continue # skip 
            try:
                j_data = json.loads(message)
            except json.JSONDecodeError:
                print(f"Invalid JSON: {message}")
                continue
            # for debugging
            print("JSON parse successful!")

            try:
                cmd = j_data.get("cmd", "").lower()

                # default response (prevents missing-send bugs)
                response = {
                    "response_code": 0,
                    "response_message": "ok"
                }
                # remote shutdown
                if cmd == "shutdown":
                    response = {
                        "response_code": 2,
                        "response_message": "Server shutting down. Bye!!!"
                    }
                    safe_send(c_socket, response)
                    return "shutdown"
                # for debugging
                elif cmd == "ping":
                    response = {
                        "response_code": 0,
                        "response_message": "pong!"
                    }

                elif cmd == "run":
                    # parse data to ensure type safety
                    try:
                        month = int(j_data.get("month", 0))
                        raw = bool(j_data.get("raw", False))
                    except Exception:
                        response = {
                            "response_code": 1,
                            "response_message": "Invalid parameter types"
                        }
                        safe_send(c_socket, response)
                        continue
                    
                    # check whether payload is valid
                    if month <= 0:
                        response = {
                            "response_code": 1,
                            "response_message": "Month must be > 0"
                        }
                    # otherwise do the thing
                    else:
                        if raw:
                            s_data = [random.randint(1, 100) for _ in range(month)]
                            msg = "Raw data transmission success!"
                        else:
                            s_data = list(range(1, month + 1))
                            msg = "Data transmission success!"

                        response = {
                            "response_code": 0,
                            "response_message": msg,
                            "data": s_data
                        }
                else:
                    response = {
                        "response_code": 4,
                        "response_message": "Error: Unknown command!"
                    }

                safe_send(c_socket, response)

            except Exception as e:
                # send errors to client
                error_response = {
                    "response_code": 3,
                    "response_message": f"Server error: {str(e)}"
                }
                safe_send(c_socket, error_response)

    return None


def main():
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_socket.bind(("localhost", 1234)) # change port accordingly, do the same for others
    s_socket.listen(5)

    print("Server is online and listening on port 1234...")

    while True:
        c_socket, address = s_socket.accept()
        print(f"Connected to {address}")

        try:
            result = handle_client(c_socket)
            if result == "shutdown":
                break
        except Exception as e:
            print(f"Error: {e}")
        finally:
            c_socket.close()
            print("Client disconnected")

    s_socket.close()
    print("Server shut down")

if __name__ == "__main__":
    main()