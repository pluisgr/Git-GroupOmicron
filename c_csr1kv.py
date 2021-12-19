import json
import requests
requests.packages.urllib3.disable_warnings()
ipr = '10.10.0.254'
urlb = 'https://' + ipr
headers_router = {
    "Accept": "application/yang-data+json",
     "Content-type":"application/yang-data+json"
}
basicauth_router = ("admin", "cisco")


yangConfig = {
    "ietf-interfaces:interface": {
        "name": "Loopback8",
        "description": "Loopback 8",
        "type": "iana-if-type:softwareLoopback", "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                { "ip": "10.10.1.8",
                "netmask": "255.255.0.0"
                }
            ]
        },
        "ietf-ip:ipv6": {}
    }
}
print('**Router CSR1kv**')
print('  Creando Loopback 8')
url_router = urlb + '/restconf/data/ietf-interfaces:interfaces/interface=Loopback8'
resp_router = requests.put(url_router, data=json.dumps(yangConfig), auth=basicauth_router, headers=headers_router, verify=False)
if(resp_router.status_code >= 200 and resp_router.status_code <= 299):
    print('    Status code: {}'.format(resp_router.status_code))
else:
    print('    Error. Status Code: {} \nError message: {}'.format(resp.status_code,resp.json()))
    exit(1)
print('  ---------Detalle de Loopback 8:')
url_router = urlb + '/restconf/data/ietf-interfaces:interfaces/interface=Loopback8'
resp_router = requests.get(url_router, auth=basicauth_router, headers=headers_router, verify=False)
print(json.dumps(resp_router.json(), indent=4))

#url_router = urlb + '/restconf/data/ietf-routing:routing-state/routing-instance=default/ribs/rib=ipv4-default/routes/route=0.0.0.0%2F0'
#url_router = urlb + '/restconf/data/ietf-routing:routing-state/routing-instance=default/ribs:rib=ipv4-default'
url_router = urlb + '/restconf/data/ietf-routing:routing-state'
resp_router = requests.request('GET',url_router, auth=basicauth_router, headers=headers_router, verify=False)
print('  ----------Tabla de enrutamiento:')
print('    Status code', resp_router.status_code)
print(resp_router, resp_router.text)
