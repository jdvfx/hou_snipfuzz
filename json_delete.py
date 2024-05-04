import json

with open("test.json","r") as j:

    data= json.load(j)

    id_to_delete = 10
    data.pop(str(id_to_delete))

    with open("test.json","w") as write_file:
        json.dump(data,write_file,indent=4)

