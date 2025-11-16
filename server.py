#!/usr/bin/env python3
"""
Tiny static server wrapper that sets conservative headers and is easy on resources.
Usage: python3 server.py 8000
It uses the stdlib http.server and does not spawn worker threads by default.
"""
import http.server
import socketserver
import sys


class LowMemoryHandler(http.server.SimpleHTTPRequestHandler):
    # Minimal headers to avoid heavy caching or extra work.
    def end_headers(self):
        # small, conservative cache for static files
        self.send_header('Cache-Control', 'public, max-age=60')
        super().end_headers()


def run(port=8000):
    Handler = LowMemoryHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving minimal portfolio at http://localhost:{port}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Stopping server")
            httpd.server_close()


if __name__ == '__main__':
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except Exception:
            pass
    run(port)
