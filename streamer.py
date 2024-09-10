import socket
import os

# Configura l'indirizzo e la porta del server
UDP_IP = "0.0.0.0"  # Accetta connessioni da qualsiasi indirizzo
UDP_PORT = 5005

# Crea il socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Server UDP in ascolto su {UDP_IP}:{UDP_PORT}")

# File JPG da inviare
file_path = "image.jpg"

while True:
    # Aspetta una richiesta dal client
    data, addr = sock.recvfrom(1024)  # 1024 è la dimensione del buffer
    print(f"Richiesta ricevuta da {addr}")
    
    if data == b"GET_IMAGE":
        # Se la richiesta è corretta, invia il file JPG
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                jpg_data = f.read()
                sock.sendto(jpg_data, addr)  # Invia i dati JPG al client
                print("File inviato!")
        else:
            print("File non trovato!")
