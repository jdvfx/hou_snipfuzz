# create hscript from selection
hs_file = "hscript_file"
c='opscript -rbV '+s.path()+' > '+hs_file
hou.hscript(c)


# convert all SolverSOP nodes  
for i in hou.nodeType("Sop/solver").instances():
  solverSop2Subnet(i)


for i in hou.nodeType("Sop/subnet").instances():
  print i.color()
  if i.color()==hou.Color((1,0.1,0.5)):
    subnet2SolverSop(i)


# convert solverSOP into subnet
def solverSop2Subnet(solver):
  subnet = solver.parent().createNode("subnet")
  subnet.setPosition(solver.position())
  subnet.setColor(hou.Color((1,0.1,0.5)))
  hou.copyNodesTo(solver.node("d/s").children(),subnet)
   
  for i, input in enumerate(solver.inputs()):
    subnet.setInput(i,input)
  out = solver.outputs()[0]
  out.setInput(0,subnet)
  n=solver.name()
  solver.destroy()
  subnet.setName(n)

# convert back subnet into solverSOP
def subnet2SolverSop(subnet):
  solver = subnet.parent().createNode("solver")
  solver.setPosition(subnet.position())
  for i in solver.node("d/s").children():
    i.destroy()
  hou.copyNodesTo(subnet.children(),solver.node("d/s"))

  for i, input in enumerate(subnet.inputs()):
    solver.setInput(i,input)
  out = subnet.outputs()[0]
  out.setInput(0,solver)
  n=subnet.name()
  subnet.destroy()
  solver.setName(n)
