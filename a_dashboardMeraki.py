import requests
api_key_meraki = "29eb58d73cc5f731afa67fa8e2aac2aa44084949"

def opcion1():
    #encontrando nuestra org id, si existe mostrarla, si no crear la org
    url = "https://api.meraki.com/api/v0/organizations"
    crear=True
    payload = None
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": api_key_meraki
    }

    response = requests.request('GET', url, headers=headers, data = payload)
    print("Respuesta:")
    print(response.status_code)
    #print(response.text.encode('utf8'))
    orgs = response.json()
    for org in orgs:
        if org['name']=='Devnet-GroupOmicron2':
            print("La organizacion ya existe, con ID")
            print(org['id'])
            id = (org['id'])
            crear = False

    if crear==True:
        url = "https://api.meraki.com/api/v0/organizations"
        payload = '''{ 
            "name": "Devnet-GroupOmicron2" 
        }'''
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Cisco-Meraki-API-Key": api_key_meraki
        }
        response = requests.request('POST', url, headers=headers, data = payload)
        print("Creando organizacion...")
        print(response.text.encode('utf8'))
    return
def opcion2():
#encontrando el id
    url = "https://api.meraki.com/api/v0/organizations"
    payload = None
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": api_key_meraki
    }
    response = requests.request('GET', url, headers=headers, data = payload)
    print(response.status_code)
    #print(response.text.encode('utf8'))
    orgs = response.json()
    for org in orgs:
        if org['name']=='Devnet-GroupOmicron2':
            id = (org['id'])

    #formando la url
    try:
        url = "https://api.meraki.com/api/v0/organizations/"+id+"/networks"
        #print (url)
    except:
        print("Se debe crear la organizacion primero")
        
#verificando si existe la network
    payload = None
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": api_key_meraki
    }

    try: 
        response = requests.request('GET', url, headers=headers, data = payload)
    except:
        print("")
    #print(response.text.encode('utf8'))
    networks = response.json()
    for network in networks:
        if network['name']=='Network-Omicron2':
            print(network['id'])
            id = (network['id'])
            borrar=input("La red ya existe, desea borrarla? (s/n)") 
            if borrar=='s':
                url = "https://api.meraki.com/api/v0/networks/"+id
                payload = None
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "X-Cisco-Meraki-API-Key": api_key_meraki
                }
                response = requests.request('DELETE', url, headers=headers, data = payload)
                print(response.status_code)
                #print(response.text.encode('utf8'))
                print("Red borrada")
        
#creando la network
    payload = '''{
        "name": "Network-Omicron2",
        "timeZone": "America/Los_Angeles",
        "tags": " tag1 tag2 ",
        "disableMyMerakiCom": false,
        "type": "appliance switch camera"
    }'''

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": api_key_meraki
    }

    response = requests.request('POST', url, headers=headers, data = payload)
    #print(response.text.encode('utf8'))
    return
def opcion3():
    opcion=input("Introducir el nuevo API KEY:")
    global api_key_meraki
    api_key_meraki=opcion 

while True: 
    print("1 - Crear organizacion, 2 - Crear red, 3 - Ingresar API KEY, 4- Salir")
    opcion=input("Ingrese opcion:") 
    if opcion =='1': 
        opcion1()
    elif opcion == '2': 
        opcion2()
    elif opcion == '3':
        opcion3() 
    elif opcion == '4': 
        break
    else: 
        print ("Escoja una opcion!") 