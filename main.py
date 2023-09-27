from getUuid import get_uuid
from connect import get_server
from register import register

server = get_server()

ident = get_uuid()

register(server, ident)

print(server)
print(ident)
