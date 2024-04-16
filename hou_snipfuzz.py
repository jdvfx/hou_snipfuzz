import json
import os
from enum import Enum

class SearchType(Enum):
    TAG = 0
    NAME = 1
    DESCRIPTION = 2

class HouSnipFuzz:

    def __init__(self):

        config = self.get_config()
        self.snippets_location = config["location"]
        self.snippets_db_file = f"{self.snippets_location}/{config['snippets_db']}"

    def write_to_json(self,*,json_file:str,snippet_data:dict)-> None:

        data = {"data":[]}
        try:
            with open(json_file, "r") as read_file:
                data = json.load(read_file)
        except Exception:
            pass

        with open(json_file, "w") as write_file:
            data["data"].append(snippet_data)
            json.dump(data, write_file,indent=4)

    def get_hscript(self) -> str:
        return "my_hscript"

    def get_latest_id(self,*,json_file:str) -> int:
        data = self.load_db_file(snippets_db_file=json_file)
        if data is None:
            return 0
        else:
            last_id = data["data"][-1]["snippet_id"]
            return last_id+1

    def load_db_file(self,*,snippets_db_file:str) -> dict | None:
        try:
            with open(snippets_db_file,"r") as file:
                return json.load(file)
        except Exception:
            return None

    def get_snippet_data(self,*,snippet_id:int=0) -> dict:
        
        snippet_name = "smoke"
        description = "sparse clustered smoke trail"
        tags = ["pyro","smoke","cluster","sparse"]
        
        snippet_data = {
            "snippet_id":snippet_id,
            "snippet_name":snippet_name,
            "description":description,
            "tags":tags
        }
        return snippet_data

        
    def write_hscript(self,*,snippets_location:str, hscript:str, snippet_id:int) -> None:

        if not os.path.exists(snippets_location):
            os.makedirs(snippets_location)
        file_name = f"{snippets_location}/hs_snippet_{snippet_id}"
        with open(file_name,"w") as file:
            file.write(hscript)

    def get_config(self)->dict:
        with open("config.json","r") as file:
            return json.load(file)

    def save_hscript(self) -> None:

        hscript = self.get_hscript()
        self.latest_id = self.get_latest_id(json_file=self.snippets_db_file)

        self.write_hscript(
            snippets_location   = self.snippets_location,
            hscript             = hscript,
            snippet_id          = self.latest_id
        )
        snippet_data = self.get_snippet_data(snippet_id=self.latest_id)
        self.write_to_json(
            json_file       = self.snippets_db_file,
            snippet_data    = snippet_data
        )


    def search_snippets(self,*,search_string:str,search_type:SearchType):

        data = self.load_db_file(snippets_db_file=self.snippets_db_file)
        if data is None:
            return None
        matches = []
        
        for snippet in data["data"]:
            match search_type:

                case SearchType.TAG:
                    for tag in snippet["tags"]:
                        if search_string in tag:
                            matches.append(snippet["snippet_id"])

                case SearchType.NAME:
                    if search_string in snippet["name"]:
                        matches.append(snippet["snippet_id"])

                case SearchType.DESCRIPTION:
                    if search_string in snippet["description"]:
                        matches.append(snippet["snippet_id"])

        return matches







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



# """ get config """
# config = get_config()
# snippets_location = config["location"]
# snippets_db = f"{snippets_location}/{config['snippets_db']}"
#
# """ write snippet and store details in json """
# hscript = get_hscript()
# latest_id = get_latest_id(json_file=snippets_db)
# write_hscript(snippets_location=snippets_location,hscript=hscript,snippet_id=latest_id)
# # user input via GUI
# snippet_data = get_snippet_data(snippet_id=latest_id)
# write_to_json(json_file=snippets_db,snippet_data=snippet_data)




# """
# with selected nodes
# get hscript code
# get latest snippet ID in jsonDB file
#
# """





