import http.server
import socketserver

# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8002


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self_path = self.path
        self_path = self_path.replace("\r", "").split("\n")
        request_line = self_path[0]
        request = request_line.split(" ")
		print(request)
        #req_cmd = request[0]
        #path = request[1]
        if path == "/":
            message = "index.html"
        if path == "/new":
            message = "new.html"
        else:
            message = "error.html"
        with open(filename, "r") as f:
            message = f.read()
        self.wfile.write(bytes(message, "utf8"))
        print("File served!")
        print(self.path)
        return


# Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
        pass

httpd.server_close()
print("")
print("Server stopped!")


# https://github.com/joshmaker/simple-python-webserver/blob/master/server.py
