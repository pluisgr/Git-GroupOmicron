import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#***DNA CENTER
urlb_dna = 'https://sandboxdnac.cisco.com'
User_dna = 'devnetuser'
Pass_dna = 'Cisco123!'
url_dna = urlb_dna + '/dna/system/api/v1/auth/token'
resp_dna = requests.post(url_dna, auth = (User_dna, Pass_dna), verify = False)
print('**DNA CENTER**')
print('  Solicitud de Token:')
print('    Status Code', resp_dna.status_code)
if resp_dna.status_code != 200:
    exit(1)
token_dna = resp_dna.json()['Token']
url_dna = urlb_dna + '/dna/intent/api/v1/network-device'
headers_dna = {
    'Content-Type' : 'application/json',
    'Accept' : 'application/json',
    'X-Auth-Token' : token_dna}
params_dna = ""
print('  Solicitud de Inventario ...')
resp_dna = requests.get(url_dna, headers=headers_dna, params=params_dna, verify = False)
print('    Status Code', resp_dna.status_code)
if resp_dna.status_code != 200:
    exit(1)
inventario = resp_dna.json()['response']
print('  ---------- Inventario ------------')
id = 1
for device in inventario:
    print('    {}. {}'.format(id,device['description']))
    print('       Serial: {}'.format(id, device['serialNumber']))
    print('       IP    : {}'.format(device['managementIpAddress']))
    id += 1