# exploration/dns_lookup.py
import socket
import time

domains = [
    "example.com",
    "google.com",
    "github.com",
    "localhost",
]

for domain in domains:
    start = time.perf_counter()
    
    try:
        # getaddrinfo gibt alle Adressen zurück (IPv4 + IPv6)
        results = socket.getaddrinfo(domain, 80)
        elapsed_ms = (time.perf_counter() - start) * 1000
        
        # Nur IPv4 Adressen (AF_INET)
        ipv4 = [r[4][0] for r in results if r[0] == socket.AF_INET]
        
        print(f"{domain:<20} → {ipv4[0]:<18} ({elapsed_ms:.2f} ms)")
    
    except socket.gaierror as e:
        print(f"{domain:<20} → FEHLER: {e}")