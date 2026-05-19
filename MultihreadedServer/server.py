import socket
import threading

# This function is same as the Single threaded server , will be called in every thread
def handle_client(client_socket, client_address):

    print(f" Worker thread started for {client_address}")
    try:
        raw_request = client_socket.recv(1024).decode('utf-8')
        if not raw_request:
            return
            
        request_lines = raw_request.split("\r\n")
        first_line = request_lines[0]
        parts = first_line.split(" ")
        path = parts[1] if len(parts) > 1 else "/"
        
        if path == "/" or path == "/index.html":
            body = "<html><body><h1>Success, Multi-Threaded Server </h1></body></html>"
            status = "HTTP/1.1 200 OK"
        else:
            body = "<html><body><h1>404 Not Found</h1></body></html>"
            status = "HTTP/1.1 404 Not Found"
            
        response = (
            f"{status}\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body.encode('utf-8'))}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{body}"
        )
        
        client_socket.sendall(response.encode('utf-8'))
        
    except Exception as e:
        print(f" Error handling client {client_address}: {e}")
    finally:
        client_socket.close()
        print(f" Worker thread finished for {client_address}")

    


def start_threaded_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(5)
    print("Multi-Threaded Server is live on http://127.0.0.1:8080 ...")
 
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Main thread accepted connection from {client_address}")
        
        client_thread = threading.Thread(
            target=handle_client, 
            args=(client_socket, client_address)
        )
        
        client_thread.start()
        

if __name__ == "__main__":
    start_threaded_server()