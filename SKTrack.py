import requests
import json
import re

version = 1
username = "eleddy"
api_key = "PUT IN API KEY HEREE!!!"

name_key = {"auth":{"RAX-KSKEY:apiKeyCredentials":{"username":username, "apiKey":api_key}}}
headers = {"Content-Type": "application/json"}

r = requests.post("https://identity.api.rackspacecloud.com/v2.0/tokens", data=json.dumps(name_key), headers=headers)

token_id = r.json()["access"]["token"]["id"]
tenant_id = r.json()["access"]["token"]["tenant"]["id"]

if version == 1:
	servers_api = "https://servers.api.rackspacecloud.com/v1.0/{0}/servers/detail".format(tenant_id)
else:
	servers_api = "https://dfw.servers.api.rackspacecloud.com/v2.0/{0}/servers/detail".format(tenant_id)

s = requests.get(servers_api, headers = {"X-Auth-Token": token_id})

rack_servers_dict ={}
for dict in s.json()["servers"]:
	rack_servers_dict[dict["addresses"]["public"][0]] = dict["name"]

with open("/etc/hosts","rb") as o_o:
	old_hosts = o_o.readlines()

already_in = [re.search(".+\t",i).group()[:-1] for i in old_hosts if re.search(".\t",i)]

new_additions = list(set(rack_servers_dict.keys())-set(already_in))

with open("/etc/hosts","ab") as hosts:
	for ip_addy in new_additions:
		hosts.write("\n{0}\t{1}".format(ip_addy,rack_servers_dict[ip_addy]))
