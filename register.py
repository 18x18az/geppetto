import requests

def register(server, serverPort, uuid):
    url = 'http://' + server + ':' + str(serverPort) + '/api/displays/' + uuid + '/register'
    requests.post(url)