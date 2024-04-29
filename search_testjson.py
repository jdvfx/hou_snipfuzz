import json
from enum import Enum

class SearchFields(Enum):
    TAG = "tags",
    NAME = "snippet_name",
    DESCRIPTION = "description",
    ALL = "d"

class SearchType(Enum):
    EXACT = 0,
    FUZZY = 1

search_match ={
    "search_string":str,
    "source_string":str,
    "found_string":str,
    "match_score":float,
}

with open("test.json","r") as f:
    data=json.load(f)

def search(data:list,search_type:SearchFields,search_string:str,ignore_case:bool):

    search_results = []

    if ignore_case:
        search_string = search_string.lower()

    for i in data:

        if search_type == SearchFields.ALL:
            search_keys = i.keys()
        else:
            search_keys = [search_type.value]

        for key in search_keys:
            value = i[key]
            if type(value) is list:
                for item in value:

                    if search_string in item:
                        s = {
                            "matchscore":1.0,
                            "matchto":item,
                            "matchfound":i
                             }

                        search_results.append(s)
            elif type(value) is str:

                if ignore_case:
                    value=value.lower()

                if search_string in value:
                    s = {
                        "matchscore":1.0,
                        "matchto":value,
                        "matchfound":i
                         }

                    search_results.append(s)

    return search_results


data=data["data"]
search_type = SearchFields.ALL
search_string = "cl"

search_results = search(
    data=data,
    search_type=search_type,
    search_string=search_string,
    ignore_case=False
)

print(f"\nsearch type = {search_type}, {len(search_results)} results\n")
for i in search_results:
    print(">",i["matchto"] , i["matchscore"])
    print(i["matchfound"],"\n")

