# exploration/tcp_server.py
import socket

# 1. Socket erstellen
# AF_INET = IPv4, SOCK_STREAM = TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Adresse wiederverwenden (wichtig beim Neustarten)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 3. An IP + Port binden
server_socket.bind(("127.0.0.1", 9000))

# 4. Auf Verbindungen warten (max. 1 in der Warteschlange)
server_socket.listen(1)

print("Server läuft auf 127.0.0.1:9000")
print("Warte auf Verbindung...\n")

# 5. Verbindung annehmen (blockiert bis jemand verbindet)
client_socket, client_address = server_socket.accept()
print(f"Verbindung von: {client_address}")

# 6. Rohe Bytes lesen
raw_bytes = client_socket.recv(4096)
print(f"\n--- Rohe Bytes (als Text) ---")
print(raw_bytes.decode("utf-8", errors="replace"))
print(f"--- Ende ---\n")
print(f"Anzahl Bytes empfangen: {len(raw_bytes)}")

# 7. Eine minimale HTTP-Antwort zurückschicken
response = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/plain\r\n"
    "Content-Length: 13\r\n"
    "\r\n"
    "Hallo, Nexus!"
)
client_socket.send(response.encode("utf-8"))

# 8. Verbindung schließen
client_socket.close()
server_socket.close()
print("Verbindung geschlossen.")