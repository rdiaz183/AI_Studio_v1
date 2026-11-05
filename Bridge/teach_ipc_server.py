import http.server
import socketserver
import json

PORT = 9877

class TeachIPC(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "ONLINE",
            "system": "Teach Engine v1 Native",
            "port": PORT,
            "role": "Curriculum Generation & Real-Time Technical Mentorship"
        }).encode("utf-8"))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "TEACH_ACK", "payload": data.decode("utf-8")}).encode("utf-8"))

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), TeachIPC) as httpd:
        print(f"[✓] Teach IPC listening on http://127.0.0.1:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down Teach IPC daemon.")