# exploration/http_server.py
import socket


def parse_request(raw: bytes) -> dict:
    """
    Zerlegt einen rohen HTTP-Request in seine Teile.
    Gibt ein Dictionary zurück.
    """
    text = raw.decode("utf-8", errors="replace")

    # Header und Body trennen (getrennt durch \r\n\r\n)
    if "\r\n\r\n" in text:
        header_section, body = text.split("\r\n\r\n", 1)
    else:
        header_section, body = text, ""

    # Zeilen trennen
    lines = header_section.split("\r\n")

    # Erste Zeile: "GET /pfad HTTP/1.1"
    first_line = lines[0]
    parts = first_line.split(" ")
    method = parts[0]           # GET, POST, etc.
    path = parts[1]             # /pfad
    version = parts[2]          # HTTP/1.1

    # Header parsen: "Host: example.com" → {"Host": "example.com"}
    headers = {}
    for line in lines[1:]:
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key] = value

    return {
        "method": method,
        "path": path,
        "version": version,
        "headers": headers,
        "body": body,
    }


def make_response(status_code: int, status_text: str, body: str, content_type: str = "text/plain") -> bytes:
    """
    Baut eine korrekte HTTP-Antwort als Bytes zusammen.
    """
    body_bytes = body.encode("utf-8")
    response = (
        f"HTTP/1.1 {status_code} {status_text}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        f"\r\n"
    )
    return response.encode("utf-8") + body_bytes


def handle_request(request: dict) -> bytes:
    """
    Routing: Welcher Pfad bekommt welche Antwort?
    """
    method = request["method"]
    path = request["path"]

    print(f"  Methode : {method}")
    print(f"  Pfad    : {path}")
    print(f"  Headers : {request['headers']}")

    if path == "/":
        return make_response(200, "OK", "Willkommen bei Nexus!")

    elif path == "/health":
        return make_response(200, "OK", "OK")

    elif path == "/echo" and method == "POST":
        body = request["body"]
        return make_response(200, "OK", f"Du hast gesendet: {body}")

    else:
        return make_response(404, "Not Found", f"Pfad nicht gefunden: {path}")


# --- Server ---

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("127.0.0.1", 9000))
server_socket.listen(5)

print("HTTP Server läuft auf http://127.0.0.1:9000")
print("Stoppen mit CTRL+C\n")

# Mehrere Anfragen hintereinander verarbeiten
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Anfrage von {client_address}:")

    raw = client_socket.recv(4096)
    request = parse_request(raw)
    response = handle_request(request)

    client_socket.send(response)
    client_socket.close()
    print()