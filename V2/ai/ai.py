import socket
import random
import json

# Mock version of AI 

def main():
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_socket.bind(('localhost', 1234))
    s_socket.listen(5)

    print("Server is online and listening on port 1234...")
    while True:
        c_socket, address = s_socket.accept()
        print(f"Connected to {address}")
        response = {}
        while True:
            j_data = {}
            #:< you networking, TCP 1024 bytes buffer. might convert to http or other protocols.
            # might break if data is too large, need more code.
            data = c_socket.recv(1024).decode() 
            if not data:
                break
            print(f"Client: {data}")
            try:
                j_data = json.loads(data)
                print("JSON parse successful!")
            except json.JSONDecodeError:
                print(f"Error: {data}")
            cmd = j_data.get("cmd", "").lower()

            if cmd == "shutdown":
                response["response_code"] = 10
                response["response_message"] = "Server shutting down. Bye!!!"
                c_socket.send((json.dumps(response) + "\n").encode())
                print("Server shutting down...")
                c_socket.close()
                s_socket.close()
                return
            elif cmd == "ping":
                response["response_code"] = 0
                response["response_message"] = "pong!"
                c_socket.send((json.dumps(response) + "\n").encode())
            elif cmd == "run":
                if "month" not in j_data or "raw" not in j_data:
                    response["response_code"] = 1
                    response["response_message"] = "Error: parameters not fulfilled!"
                    c_socket.send((json.dumps(response) + "\n").encode())
                    break

                if j_data["raw"] == True:
                    s_data = [random.randint(1, 100) for _ in range(j_data["month"])]
                    response["response_message"] = "Raw data transmission success!"
                    
                else:
                    s_data = [i + 1 for i in range(j_data["month"])]
                    response["response_message"] = "Data transmission success!"
                response["response_code"] = 0
                response["data"] = s_data  
                c_socket.send((json.dumps(response) + "\n").encode())

            else:
                response["response_code"] = 4
                response["response_message"] = "Error: Unknown command!"
                c_socket.send((json.dumps(response) + "\n").encode())
            #print(f"R: {data}")
        c_socket.close()
        print("Client disconnected")

if __name__ == "__main__":
    main()