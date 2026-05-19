import  socket
def start_server(): 
    # socket.AF_INET= IP addresses family    socket.SOCK_STREAM= protocol that keeps connecction until one of them breaks or conn error 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind(('127.0.0.1', 8080))
    
    server_socket.listen(5)
    print("Server is live and listening on http://127.0.0.1:8080 ...")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        
        try:
            raw_request = client_socket.recv(1024).decode('utf-8')
            if not raw_request:
                continue
                
            print("\n--- RECEIVED RAW HTTP REQUEST ---")
            print(raw_request)
            print("---------------------------------\n")


            request_lines = raw_request.split("\r\n")
            first_line = request_lines[0]
            parts = first_line.split(" ")
            
            method = parts[0] if len(parts) > 0 else "GET"
            path = parts[1] if len(parts) > 1 else "/"
            
            if path == "/" or path == "/index.html":
                body = "<html><body><h1>Success</h1></body></html>"
                status = "HTTP/1.1 200 OK"
            else:
                body = "<html><body><h1>Error Not Found</h1></body></html>"
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
            print(f" Error processing request: {e}")
            
        finally:
            client_socket.close()
            print("Connection closed. Waiting for next client")

if __name__ == "__main__":
    start_server()