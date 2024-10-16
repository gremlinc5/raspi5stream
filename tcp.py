import socket

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()

        print(f"Server in ascolto su {host}:{port}")

        while True:
            # Accetta una nuova connessione
            client_socket, address = server_socket.accept()
            print(f"Connessione accettata da {address}")

            with client_socket:
                # Ricevi il messaggio dal client
                data = client_socket.recv(1024)
                if data:
                    message = data.decode('utf-8')
                    print(f"Messaggio ricevuto: {message}")
                    
                    # Invia un echo della risposta
                    response = f"Echo: {message}"
                    client_socket.sendall(response.encode('utf-8'))

if __name__ == "__main__":
    start_server('localhost', 12345)
