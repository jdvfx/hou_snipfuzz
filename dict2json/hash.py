import hashlib
import json


# create stable hash from any object
def create_hash(thing) -> str: 
    h= hashlib.md5(json.dumps(thing).encode('utf-8')).digest()
    return h.hex()

def test():
    j = {
        "name":"BOB",
        "type":"Bald",
        "age":83
    }

    h = create_hash(j)
    print(h)


