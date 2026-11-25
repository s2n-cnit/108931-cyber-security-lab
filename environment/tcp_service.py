"""Harmless TCP reachability fixture, not an SSH or application server."""
import socketserver, sys
class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.sendall(b'LAB TCP reachability fixture\n')
class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True
if __name__ == '__main__':
    with Server(('0.0.0.0',int(sys.argv[1])), Handler) as server:
        server.serve_forever()
