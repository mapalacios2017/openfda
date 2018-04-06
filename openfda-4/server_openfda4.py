import http.server
import socketserver

PORT = 8005

# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):

        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()
        if self.path == "/":
            with open("search.html") as f:
                message = f.read()
                self.wfile.write(bytes(message, "utf8"))

        elif "search" in self.path:
            params = self.path.split("?")[1]
            drug = params.split("&")[0].split("=")[1]
            limit = params.split("&")[0].split("=")[1]
            self.wfile.write(bytes(drug + " " + limit, "utf8"))


        return

Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()

