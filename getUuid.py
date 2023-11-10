import uuid

def get_stored_uuid():
    try:
        with open('/home/admin/geppetto/uuid.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None
    
def store_uuid(uuid):
    with open('/home/admin/geppetto/uuid.txt', 'w') as f:
        f.write(uuid)

def generate_uuid():
    raw = str(uuid.uuid4())
    processed = raw.replace('-', '')
    return processed

def get_uuid():
    ident = get_stored_uuid()
    if ident is None:
        print('creating new uuid')
        ident = generate_uuid()
        store_uuid(ident)
    return ident
