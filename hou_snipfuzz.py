# Python 3.10 / Houdini 20.0

import json
import pathlib
import os

# import difflib

import hou
from PySide2 import QtCore, QtWidgets

from typing import List, Tuple
from enum import Enum


class SearchType(Enum):
    TAG = 0
    NAME = 1
    DESCRIPTION = 2


class SnipFuzz(QtWidgets.QWidget):

    def __init__(self):

        QtWidgets.QWidget.__init__(self)

        self.resize(400, 400)

        self.name_text = QtWidgets.QLabel("name")
        self.name_field = QtWidgets.QLineEdit()
        self.desc_text = QtWidgets.QLabel("description")
        self.desc_field = QtWidgets.QLineEdit()
        self.tags_text = QtWidgets.QLabel("tags")
        self.tags_field = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton("Save Snippet")

        layout = QtWidgets.QFormLayout(self)
        layout.addWidget(self.name_text)
        layout.addWidget(self.name_field)
        layout.addWidget(self.desc_text)
        layout.addWidget(self.desc_field)
        layout.addWidget(self.tags_text)
        layout.addWidget(self.tags_field)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.button.pressed.connect(self.buttonpress)

    # -------------------------------------------------------------------
    def buttonpress(self):

        self.name = self.name_field.displayText()
        self.desc = self.desc_field.displayText()
        self.tags = self.tags_field.displayText()
        self.save_hscript()

        self.close()

    # -------------------------------------------------------------------
    def save_hscript(self) -> None:

        config = self.get_config()
        self.snippets_dir = config["dir"]
        self.snippets_db_file = f"{self.snippets_dir}/{config['snippets_db']}"

        hscript = self.get_hscript()
        self.latest_id = self.get_latest_id(json_file=self.snippets_db_file)

        self.write_hscript(
            snippets_dir=self.snippets_dir, hscript=hscript, snippet_id=self.latest_id
        )

        snippet_data = self.get_snippet_data(snippet_id=self.latest_id)
        self.write_to_json(json_file=self.snippets_db_file, snippet_data=snippet_data)

    # -------------------------------------------------------------------
    def get_config(self) -> dict | None:

        parent = pathlib.Path(__file__).parent.resolve()
        with open(f"{parent}/config.json", "r") as file:
            return json.load(file)

    # -------------------------------------------------------------------
    def get_latest_id(self, *, json_file: str) -> int:
        data = self.load_db_file(snippets_db_file=json_file)
        if data is None:
            return 0
        else:
            last_id = data["data"][-1]["snippet_id"]
            return last_id + 1

    # -------------------------------------------------------------------
    def write_to_json(self, *, json_file: str, snippet_data: dict) -> None:

        data = {"data": []}
        try:
            with open(json_file, "r") as read_file:
                data = json.load(read_file)
        except Exception:
            pass

        with open(json_file, "w") as write_file:
            data["data"].append(snippet_data)
            json.dump(data, write_file, indent=4)

    # -------------------------------------------------------------------
    def load_db_file(self, *, snippets_db_file: str) -> dict | None:
        try:
            with open(snippets_db_file, "r") as file:
                return json.load(file)
        except Exception:
            return None

    # -------------------------------------------------------------------
    def get_snippet_data(self, *, snippet_id: int = 0) -> dict:

        snippet_data = {
            "snippet_id": snippet_id,
            "snippet_name": self.name,
            "description": self.desc,
            "tags": self.tags,
        }
        return snippet_data

    # -------------------------------------------------------------------
    def write_hscript(
        self, *, snippets_dir: str, hscript: str, snippet_id: int
    ) -> None:

        if not os.path.exists(snippets_dir):
            os.makedirs(snippets_dir)
        file_name = f"{snippets_dir}/hs_snippet_{snippet_id}"
        with open(file_name, "w") as file:
            file.write(hscript)

    # -------------------------------------------------------------------
    """
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
    """

    """
    Hscript functions

    """

    # -------------------------------------------------------------------
    def get_hscript(self) -> str:

        sel = hou.selectedNodes()
        if len(sel) == 0:
            return ""
        selected_node = sel[0]
        parent = selected_node.parent()
        subnet = parent.collapseIntoSubnet(sel, subnet_name="TEMP_subnet")

        hscript_command = "opscript -rbV " + subnet.path()
        opscript_result = hou.hscript(hscript_command)

        pos = subnet.position()
        subnet.setPosition(pos)
        subnet.extractAndDelete()

        return opscript_result[0]

    # -------------------------------------------------------------------
    def solversops_to_subnets(self) -> None:
        for solversop in hou.nodeType("Sop/solver").instances():
            self.solversop_to_subnet(solversop)

    # -------------------------------------------------------------------
    def subnets_to_solversops(self) -> None:
        CUSTOM_COLOR = hou.Color((2, 0.1, 0.5))
        for subnet in hou.nodeType("Sop/subnet").instances():
            if subnet.color() == CUSTOM_COLOR:
                self.subnet_to_solversop(subnet)

    # -------------------------------------------------------------------
    def solversop_to_subnet(self, solver) -> None:
        """
        convert solver_SOP node into custom_subnet node
        """
        subnet = solver.parent().createNode("subnet")
        subnet.setPosition(solver.position())

        CUSTOM_COLOR = hou.Color((2, 0.1, 0.5))
        subnet.setColor(CUSTOM_COLOR)

        # d/s are the 2 nodes inside solver SOP levels
        # d: dopnet / s:SOP solver
        hou.copyNodesTo(solver.node("d/s").children(), subnet)

        for idx, input in enumerate(solver.inputs()):
            subnet.setInput(idx, input)
        for idx, output in enumerate(solver.outputs()):
            output.setInput(0, subnet)

        solver_name = solver.name()
        solver.destroy()
        subnet.setName(solver_name)

    # -------------------------------------------------------------------
    def subnet_to_solversop(self, subnet) -> None:
        """
        convert custom_subnet node into solver_SOP node
        """
        solver = subnet.parent().createNode("solver")
        solver.setPosition(subnet.position())

        for solver_child in solver.node("d/s").children():
            solver_child.destroy()

        hou.copyNodesTo(subnet.children(), solver.node("d/s"))

        for idx, input in enumerate(subnet.inputs()):
            solver.setInput(idx, input)
        for idx, output in enumerate(subnet.outputs()):
            output.setInput(0, solver)

        subnet_name = subnet.name()
        subnet.destroy()
        solver.setName(subnet_name)
