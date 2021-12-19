import requests

"""
Este es el token con duracion de 12 horas: 
'OTk0NzE3MjAtNDVkMi00NGRmLWFlMjMtMDQ2ZDYyN2U2ZGE4OTUwMzNhMzgtMzZk_P0A1_242b07f9-2b66-4cc2-9f6c-81cb45ce0742' 
"""
access_token = input("Digite el Token: ")

# ----------- Creando un Room con el nombre “Devnet-GroupOmicron” ------------------
url = 'https://webexapis.com/v1/rooms'

headers = {

    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}

params={'title': 'Devnet-GroupOmicron'}
res = requests.post(url, headers=headers, json=params)
print(res.json())


# ----- Obteniendo el room_id recien creado del room: “Devnet-GroupOmicron”---------
url = 'https://webexapis.com/v1/rooms'

headers = {
 'Authorization': 'Bearer {}'.format(access_token),
 'Content-Type': 'application/json'
}

params={'max': '100'}
res = requests.get(url, headers=headers, params=params)

datos = res.json() 
room_id  = datos['items'][0]['id']
print(room_id )

"""
Si no funciona el room_id es:
room_id  = 'Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vM2UwYzJjMzAtNjAyZS0xMWVjLTk0N2YtYTk2ZDM4NzVlZTM5'
"""

#  --------- En este Room estan incluidos todos los integrantes del grupo -------------
url = 'https://webexapis.com/v1/memberships'

headers = {
 'Authorization': 'Bearer {}'.format(access_token),
 'Content-Type': 'application/json'
}
params = {  'roomId': room_id, 
            'perosonId':'Y2lzY29zcGFyazovL3VzL1BFT1BMRS81M2QwMDdkYy01MGU2LTRiZWQtYWVmYS05YjdmODc3NGE0ZGM', 
            'personEmail': 'pluisgr@gmail.com',
            'perosonId':'Y2lzY29zcGFyazovL3VzL1BFT1BMRS85MmU1NjEyYi1lMjM5LTRkZTQtYThlYi02MzQzZjQ0NmEyNDE',
            'personEmail': 'lpzd.marcelo.condori@unifranz.edu.bo',
            'perosonId':'Y2lzY29zcGFyazovL3VzL1BFT1BMRS9lZTU2YmEwYS01ODRlLTQ5YmUtYTI0Yi02MDAzZDdhMDMyOTQ',
            'personEmail': 'ferney.amaya@gmail.com'}

res = requests.post(url, headers=headers, json=params)
print(res.json())

# ---------- Se envia un mensaje al Room con la ruta del contenedor en el Docker Hub ------------
message = 'La ruta del contenedor en el Docker Hub es: https://hub.docker.com/repository/docker/ferneyamaya/docker_groupomicron'
url = 'https://webexapis.com/v1/messages'
headers = {
 'Authorization': 'Bearer {}'.format(access_token),
 'Content-Type': 'application/json'
}
params = {'roomId': room_id, 'markdown': message}
res = requests.post(url, headers=headers, json=params)
print(res.json())