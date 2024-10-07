import os
import json
import random
from enum import Enum
import string
from hash import create_hash

class gender(Enum):
    Male = "Male"
    Female = "Female"

def create_record(unique_name:str , name: str, age: int, gender: gender):
    d = {}

    hash =create_hash(unique_name)
    data = {"hash":hash,"name": name, "age": age, "gender": gender.value}
    d[unique_name] = data
    return d

# ------------------------------------------------------------------
def save_record(json_file: str, records: list[dict], update:bool = True):

    ''' load existing data (READ)'''
    j = {}

    # create file if doesnt exist
    if not os.path.exists(json_file):
        with open(json_file, "a"):
            os.utime(json_file, None)

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

# ------------------------------------------------------------------
def get_record(json_file: str, hash:str) -> None | dict: 

    ''' load existing data (READ)'''
    j = {}
    with open(json_file, "r") as file:
        try:
            j = json.load(file)
        except Exception:
            pass
    return j.get(hash)

# ------------------------------------------------------------------
def create_random_record(gender:gender) -> dict:
    unique_name = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
    name = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    age = random.randint(18,90)
    genders_list = [e.value for e in gender]
    gender = random.choices(genders_list)
    hash =create_hash(unique_name)

    d = {}
    data = {
        "hash":hash,
        "name":name,
        "age":age,
        "gender":gender        
    }
    d[unique_name] = data

    return d

# ------------------------------------------------------------------
def main():

    json_file = f"my_file.json"
    global gender

    records = []
    for i in range(10):
        d = create_random_record(gender=gender)
        records.append(d)

    record = create_record(
        unique_name="Test Name", 
        name="this is a test!", 
        age=23, 
        gender=gender.Female
    )

    records = [record]
    save_record(json_file=json_file, records=records)

    hash = "LBOB"
    record = get_record(json_file=json_file, hash=hash)
    print(record)

main()




