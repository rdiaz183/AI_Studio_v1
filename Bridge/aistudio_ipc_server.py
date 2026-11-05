import http.server
import socketserver
import json

PORT = 9876

class AIStudioIPC(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "ONLINE",
            "system": "AI_Studio v1 Native",
            "port": PORT,
            "workspace": r"C:\Users\rdiaz\Documents\Unreal Projects\AI_Studio_Workspace"
        }).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"received": True, "payload": post_data.decode("utf-8")}).encode("utf-8"))

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), AIStudioIPC) as httpd:
        print(f"[✓] AI_Studio IPC listening on http://127.0.0.1:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down AI_Studio IPC daemon.")