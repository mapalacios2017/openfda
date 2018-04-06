import http.server
import socketserver
import json

socketserver.TCPServer.allow_reuse_address = True

PORT = 8005

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):

        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if self.path == "/":
            with open("search.html") as f:
                message = f.read()
                self.wfile.write(bytes(message, "utf8"))

        elif "search" in self.path:
            params = self.path.split("?")[1]
            drug = params.split("&")[0].split("=")[1]
            self.wfile.write(bytes(drug, "utf8"))

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", '/drug/label.json?search=generic_name:' + self.wfile.write(bytes(drug, "utf8")), None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

        return


Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()

