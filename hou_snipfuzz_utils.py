import re

# -------------------------------------------------------------------

def solversop_to_subnet(solver) -> None:
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

def subnet_to_solversop(subnet) -> None:
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

def solversops_to_subnets() -> None:
    for solversop in hou.nodeType("Sop/solver").instances():
       solversop_to_subnet(solversop)

# -------------------------------------------------------------------

def subnets_to_solversops() -> None:
    CUSTOM_COLOR = hou.Color((2,0.1,0.5))
    for subnet in hou.nodeType("Sop/subnet").instances():
        if subnet.color()==CUSTOM_COLOR:
            subnet_to_solversop(subnet)

# -------------------------------------------------------------------

def selected_nodes_to_hscript() -> str:

    selected_nodes = hou.selectedNodes()
    if len(selected_nodes)==0:
        return ""
    parent = selected_nodes[0].parent()
    subnet = parent.collapseIntoSubnet(selected_nodes,subnet_name="TEMP_subnet")
    subnet.node("output0").destroy()
    
    hscript_command='opscript -rbV '+subnet.path()
    opscript_result = hou.hscript(hscript_command)
    
    """
    reduce nodes position offset
    when converting subnet back into nodes
    """
    pos = subnet.position()
    subnet.setPosition((pos[0]-1.65,pos[1]+1.45))
    subnet.extractAndDelete()
    
    return opscript_result[0]

# -------------------------------------------------------------------

def reduce_float_precision(s:str,precision:int) -> str:

    # TODO:
    # use f strings {:.2f} or round()

    """
    trim decimals 
    eg: with precision set to 2:
     -20.149999999999999
     -20.14
    """

    s_ =[]
    floats = r'-*[0-9]+\.[0-9]+'
    validchars = r'^[0-9\-\.]*$'

    for i in s.split(" "):
        if re.match(floats,i) and re.match(validchars,i):
            k = i.split(".")
            k[1] = k[1][:precision]
            s = ".".join(k)
            s = str(float(s))
            s_.append(s)
        else:
            s_.append(i)

    return " ".join(s_)

# -------------------------------------------------------------------

def optimize_hscript(hscript:str) -> str:

    temp = ""
    lines = hscript.splitlines()

    for line in lines:
        precision = 4
        if line.startswith(("opcolor","oplocate")):
            precision = 2
        line = reduce_float_precision(line,precision)

        """ ignore some lines """
        comment = line.startswith("#")
        block_divider = len(line)<2
        wirestyle = "wirestyle" in line
        exprlang = "opexprlanguage -s hscript" in line

        if not (comment or block_divider or wirestyle or exprlang):
            temp+=f"{line}\n"

    return temp

# -------------------------------------------------------------------




