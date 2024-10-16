from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/cam0':
            # Imposta il percorso del file JPG da servire
            file_path = 'path/to/your/image.jpg'

            try:
                # Apri il file in modalità binaria
                with open(file_path, 'rb') as file:
                    # Leggi il contenuto del file
                    file_content = file.read()

                    # Imposta l'intestazione di risposta
                    self.send_response(200)
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', len(file_content))
                    self.end_headers()

                    # Invia il contenuto del file
                    self.wfile.write(file_content)

            except FileNotFoundError:
                # Gestione dell'errore se il file non viene trovato
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'File not found')
        else:
            # Gestione per le richieste non corrispondenti a /cam0
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Endpoint not found')

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server in esecuzione sulla porta {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    # Esegui il server HTTP sulla porta 8000
    run(port=8000)
