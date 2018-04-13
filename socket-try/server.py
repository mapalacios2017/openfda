import http.server
import http.client
import socketserver
import json

socketserver.TCPServer.allow_reuse_address = True

PORT = 8000

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # Code for the active ingredient and company
    def do_GET(self):

        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if self.path == "/":
            with open("openfda.html") as f:
                message = f.read()
                self.wfile.write(bytes(message, "utf8"))

        elif "searchDrug" in self.path:
            params = self.path.split("?")[1]
            drug = params.split("&")[0].split("=")[1]
            limit = params.split("&")[1].split("=")[1]
            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", '/drug/label.json?search=active_ingredient:' + drug + "&limit=" + limit, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            drugs = json.loads(repos_raw)
            total_drugs = ""
            for drug in drugs['results']:
                drugs_info = "<ol>" + "Drug Id: " + drug['id'] + "</ol>"
                total_drugs = total_drugs + drugs_info


            self.wfile.write(bytes(total_drugs, "utf8"))

        elif "searchCompany" in self.path:
            params = self.path.split("?")[1]
            company = params.split("&")[0].split("=")[1]
            limit = params.split("&")[1].split("=")[1]
            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", '/drug/label.json?search=openfda.manufacturer_name:' + company + "&limit=" + limit, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            drugs = json.loads(repos_raw)
            total_drugs = ""
            for drug in drugs['results']:
                drugs_info = "<ol>" + "Drug Id: " + drug['id'] + "</ol>"
                total_drugs = total_drugs + drugs_info


            self.wfile.write(bytes(total_drugs, "utf8"))

        elif "druglist" in self.path:
            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", '/drug/label.json', None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            drugs = json.loads(repos_raw)
            druglist = "<html>" + \
                       "<body>" + \
                       "<ul>"

            for drug in drugs['results']:
                druglist += "<li>" + drug['id']
                if 'active_ingredient' in drug:
                    druglist += " " + drug['active_ingredient']
                druglist += "</li>"
            druglist += "</ul>" + \
                        "</body>" + \
                        "</html>"

            self.wfile.write(bytes(druglist, "utf8"))


Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
# Miguel A. Palacios