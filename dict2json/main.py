import json
import random
from enum import Enum
import string

class gender(Enum):
    Male = "Male"
    Female = "Female"

def create_record(hash: str, name: str, age: int, gender: gender):
    d = {}
    data = {"name": name, "age": age, "gender": gender.value}
    d[hash] = data
    return d


def save_record(json_file: str, records: list[dict], update:bool = True):

    ''' load existing data (READ)'''
    j = {}
    with open(json_file, "r") as file:
        try:
            j = json.load(file)
        except Exception:
            pass

    ''' add to existing data (WRITE)'''
    with open(json_file, "w") as file:
        for record in records:
            for key, value in record.items():
                if key in j.keys():
                    if update==True:
                        j[key] = value
                else:
                    j[key] = value

        json.dump(j, file, indent=4, sort_keys=True)

json_file = f"my_file.json"



def create_random_record(gender:gender) -> dict:
    hash = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
    name = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    age = random.randint(18,90)
    genders_list = [e.value for e in gender]
    gender = random.choices(genders_list)

    d = {}
    data = {
        "name":name,
        "age":age,
        "gender":gender        
    }
    d[hash] = data

    return d



records = []
for i in range(10):
    d = create_random_record(gender=gender)
    records.append(d)

record = create_record(
    hash="LBOB", 
    name="Bob", 
    age=23, 
    gender=gender.Male
)
records = [record]

print("?>>",json_file)


save_record(json_file=json_file, records=records)

""" TODO """"""
def get_record(json_file: str, records: list[dict], update:bool = True):

    ''' load existing data (READ)'''
    j = {}
    with open(json_file, "r") as file:
        try:
            j = json.load(file)
        except Exception:
            pass

    ''' add to existing data (WRITE)'''
    with open(json_file, "w") as file:
        for record in records:
            for key, value in record.items():
                if key in j.keys():
                    if update==True:
                        j[key] = value
                else:
                    j[key] = value

        json.dump(j, file, indent=4, sort_keys=True)

json_file = f"my_file.json"
"""

hash = "LBOB"
record = get_record(json_file=json_file, hash=hash)



