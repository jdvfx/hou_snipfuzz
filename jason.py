import json
import os
# from os import execve




snippet_id = 12
snippet_name = "smoke"
description = "sparse clustered smoke trail"
tags = ["pyro","smoke","cluster","sparse"]





#
# def read_json(json_file:str) -> None:
#     data = []
#     try:
#         with open(json_file, "r") as read_file:
#             data = json.load(read_file)
#     except Exception:
#         return
#     print(data)
#     
# data = read_json(json_file)
# print(type(data))



def write_to_json(*,json_file:str,snippet_data:dict)-> None:
    data = {"data":[]}
    try:
        with open(json_file, "r") as read_file:
            data = json.load(read_file)
    except Exception:
        pass

    with open(json_file, "w") as write_file:
        data["data"].append(snippet_data)
        json.dump(data, write_file,indent=4)

def get_hscript() -> str:
    return "my_hscript"

def get_latest_id(*,json_file:str) -> int:
    try:
        with open(json_file,"r") as file:
            data = json.load(file)
            last_id = data["data"][-1]["snippet_id"]
            return last_id+1
    except Exception:
        return 0

def get_snippet_data(*,snippet_id:int=0) -> dict:
    snippet_data = {
        "snippet_id":snippet_id,
        "snippet_name":snippet_name,
        "description":description,
        "tags":tags
    }
    return snippet_data

    
def write_hscript(*,snippets_location:str, hscript:str, snippet_id:int) -> None:
    if not os.path.exists(snippets_location):
        os.makedirs(snippets_location)
    file_name = f"{snippets_location}/hs_snippet_{snippet_id}"
    with open(file_name,"w") as file:
        file.write(hscript)

def get_config()->dict:
    with open("config.json","r") as file:
        data = json.load(file)
        return data

""" get config """
config = get_config()
snippets_location = config["location"]
snippets_db = f"{snippets_location}/{config['snippets_db']}"

""" write snippet and store details in json """
hscript = get_hscript()
latest_id = get_latest_id(json_file=snippets_db)
write_hscript(snippets_location=snippets_location,hscript=hscript,snippet_id=latest_id)
# user input via GUI
snippet_data = get_snippet_data(snippet_id=latest_id)
write_to_json(json_file=snippets_db,snippet_data=snippet_data)




"""
with selected nodes
get hscript code
get latest snippet ID in jsonDB file



"""


