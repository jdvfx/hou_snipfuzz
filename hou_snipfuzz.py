# Python 3.10 / Houdini 20.0

import json
import pathlib
import os
from enum import Enum
import hou

from PySide2 import QtCore,QtWidgets
import difflib
from typing import List,Tuple

class SearchType(Enum):
    TAG = 0
    NAME = 1
    DESCRIPTION = 2





class HouSnipFuzz:

    def __init__(self):

        config = self.get_config()
        self.snippets_location = config["location"]
        self.snippets_db_file = f"{self.snippets_location}/{config['snippets_db']}"
        self.node_name = None

        print(">>" , self.snippets_location , self.snippets_db_file)

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
        return self.selected_nodes_to_hscript()

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
        
        snippet_name = self.node_name
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
        
        parent = pathlib.Path(__file__).parent.resolve()
        with open(f"{parent}/config.json","r") as file:
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

    #############################################################

    def solversop_to_subnet(self,solver) -> None:
        """
        convert solver_SOP node into custom_subnet node
        """
        subnet = solver.parent().createNode("subnet")
        subnet.setPosition(solver.position())
        
        CUSTOM_COLOR = hou.Color((2,0.1,0.5))
        subnet.setColor(CUSTOM_COLOR)
        
        # d/s are the 2 nodes inside solver SOP levels
        # d: dopnet / s:SOP solver
        hou.copyNodesTo(solver.node("d/s").children(),subnet)
        
        for idx, input in enumerate(solver.inputs()):
            subnet.setInput(idx,input)
        for idx, output in enumerate(solver.outputs()):
            output.setInput(0,subnet)

        solver_name = solver.name()
        solver.destroy()
        subnet.setName(solver_name)

    # -------------------------------------------------------------------

    def subnet_to_solversop(self,subnet) -> None:
        """
        convert custom_subnet node into solver_SOP node
        """
        solver = subnet.parent().createNode("solver")
        solver.setPosition(subnet.position())
        
        for solver_child in solver.node("d/s").children():
            solver_child.destroy()
            
        hou.copyNodesTo(subnet.children(),solver.node("d/s"))

        for idx, input in enumerate(subnet.inputs()):
            solver.setInput(idx,input)  
        for idx, output in enumerate(subnet.outputs()):
            output.setInput(0,solver)

        subnet_name = subnet.name()
        subnet.destroy()
        solver.setName(subnet_name)

    # -------------------------------------------------------------------

    def solversops_to_subnets(self) -> None:
        for solversop in hou.nodeType("Sop/solver").instances():
            self.solversop_to_subnet(solversop)

    # -------------------------------------------------------------------

    def subnets_to_solversops(self) -> None:
        CUSTOM_COLOR = hou.Color((2,0.1,0.5))
        for subnet in hou.nodeType("Sop/subnet").instances():
            if subnet.color()==CUSTOM_COLOR:
                self.subnet_to_solversop(subnet)

    # -------------------------------------------------------------------

    def selected_nodes_to_hscript(self) -> str:
        selected_nodes = hou.selectedNodes()
        if len(selected_nodes)==0:
            return ""
        selected_node = selected_nodes[0]
        parent = selected_node.parent()
        self.node_name = selected_node.name()
        subnet = parent.collapseIntoSubnet(selected_nodes,subnet_name="TEMP_subnet")
        
        hscript_command='opscript -rbV '+subnet.path()
        opscript_result = hou.hscript(hscript_command)
        
        pos = subnet.position()
        subnet.setPosition(pos)
        subnet.extractAndDelete()
        
        return opscript_result[0]

    # -------------------------------------------------------------------









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



class SnipFuzz(QtWidgets.QWidget):

    def __init__(self, wrangle, file:str):

        self.wrangle = wrangle
        QtWidgets.QWidget.__init__(self)

        self.resize(600,400)

        self.input_char_list:List[str] = []
        self.snippet_index:int = 0
        self.file:str = file
        self.snippets:List[str] = self.get_snippet_list()
        #
        self.textfield = QtWidgets.QLineEdit()
        self.textfield.textChanged.connect(self.textchanged)
        #
        self.text = QtWidgets.QLabel("-")
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.text)
        layout.addWidget(self.textfield)
        self.setLayout(layout)
        
    # ----------------------------------------------------------
    def keyPressEvent(self, e):
            if e.key() == QtCore.Qt.Key_Up:
                self.snippet_index +=1
            elif e.key() == QtCore.Qt.Key_Down:
                self.snippet_index -=1
            # Validate search result with Ctrl key
            elif e.key() == QtCore.Qt.Key_Control:
                self.wrangle.parm("snippet").set(self.text.text())
                self.close()
                
            self.update_text(self.textfield.displayText())

    # ----------------------------------------------------------
    def update_text(self,text):
        results:List[Tuple[float,str]] = self.search(text)
        if len(results)>0:
            self.snippet_index:int = min(max(0,self.snippet_index),len(results)-1)
            current_snippet = results[self.snippet_index][1]
            self.text.setText(current_snippet)

    def textchanged(self,text):
        self.update_text(text)

    # ----------------------------------------------------------
    """ split file by separators containing dashes """
    def get_snippet_list(self) -> List[str]:
        with open(self.file,"r") as file:
            lines = file.read().splitlines()
        snippets:list[str] = []
        snip_lines:str = ""
        for line in lines:
            if "-----" not in line:
                snip_lines += f"{line}\n"
            else:
                snippets.append(snip_lines)
                snip_lines = ""
        if len(snip_lines)>0:
            snippets.append(snip_lines)
        return snippets

    # ----------------------------------------------------------
    """ fuzzy search in snippet lines, return list of snippets """
    def search(self,search_string) -> List[Tuple[float,str]]:
        search_results = []
        for snippet in self.snippets:
            # if the search string is literally inside the snippet, prioritize it 
            if search_string in snippet:
                ratio = 2.0
                result:Tuple[float,str] = (ratio,snippet)
                search_results.append(result)
            else:
                alpha = re.sub('[^a-za-z]+', ' ', snippet) # alpha only
                words_ = alpha.split(' ')
                words_ = [x for x in words_ if x != ''] # remove empty elements
                words = list(set(words_)) # remove duplicates

                # basic fuzzy search with difflib
                for word in words:
                    ratio:float = difflib.SequenceMatcher(None,search_string,word).ratio()
                    if ratio>0.8:
                        result:Tuple[float,str] = (ratio,snippet)
                        search_results.append(result)
                        break
        #
        search_results.sort(reverse=True)
        return search_results


