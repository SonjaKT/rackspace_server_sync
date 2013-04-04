import requests
import json

version = 1
username = "eleddy"
api_key = "NO API KEY BC IT'S GITHUB"

name_key = {"auth":{"RAX-KSKEY:apiKeyCredentials":{"username":username, "apiKey":api_key}}}
headers = {"Content-Type": "application/json"}

r = requests.post("https://identity.api.rackspacecloud.com/v2.0/tokens", data=json.dumps(name_key), headers=headers)

token_id = r.json()["access"]["token"]["id"]
tenant_id = r.json()["access"]["token"]["tenant"]["id"]

if version == 1:
	servers_api = "https://servers.api.rackspacecloud.com/v1.0/{0}/servers/detail".format(tenant_id)
else:
	servers_api = "https://dfw.servers.api.rackspacecloud.com/v2/{0}/servers/detail".format(tenant_id)

s = requests.get(servers_api, headers = {"X-Auth-Token": token_id})
server_list = []

for dict in s.json()["servers"]:
	server_list.append("{1} {0}".format(dict["name"], dict["addresses"]["public"][0]))

with open("/etc/hosts","ab") as ho:
	for server in server_list:
		ho.write("\n"+server)
