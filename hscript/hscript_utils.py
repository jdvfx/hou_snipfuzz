import hou

class Hscript:
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

