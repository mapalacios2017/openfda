import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)

repo = repos['results']

print("The drug id is", repo[0]['openfda']['spl_id'])
print("The drug purpose is", repo[0]['purpose'])
print("The manufacturer name is", repo[0]['openfda']['manufacturer_name'])