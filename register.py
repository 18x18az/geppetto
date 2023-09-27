import requests

def register(server, uuid):
    url = 'http://' + server + '/api/displays/' + uuid + '/register'
    r = requests.post(url)