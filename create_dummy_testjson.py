import json
import random



n = [
    "sphere",
    "pyro setup",
    "smoke trail",
    "sand explosion",
    "cloth tearing",
    "test snippet",
    "sand dunes",
    "sop occlusion",
    "resample time",
    "hide some nodes",
    "magic portal",
    "lightning bolts",
    "sand portal",
    "water splash large scale",
    "ocean remesh",
    "water foam solver",
    "bubble sim",
    "point clustering",
    "tree rigging"
    ]

d = [
    "moutain model",
    "sop cleanup",
    "sparks effect",
    "smoke trails setup",
    "sparks with motion blur",
    "cloth tearing setup",
    "color nodes",
    "vex code cleanup"
    "simple point cluster",
    "retime animation",
    "create pre and post roll",
    "extrapolate into collision",
    "smoke upres solver",
    "reduce polygons",
    "convert volume to points",
    "extract transforms",
    "reload transform",
    "instancing setup"
    "crowds setup",
    "simple rigging setup"
    ]

t = [
    "origin",
    "noise",
    "bake",
    "crash",
    "vector",
    "point",
    "boxes",
    "clustering",
    "vortex",
    "acceleration",
    "vex",
    "python",
    "xform",
    "trans",
    "position",
    "quaternion",
    "rotation",
    "disc",
    "bounding",
    "separate",
    "groups",
    "rename",
    "voxel",
    "velocity",
    "debug",
    "contact",
    "detangle",
    "rest",
    "cleanup"
    "sops",
    "dops",
    "geometry",
    "culling",
    "filter",
    "vdb",
    "particles",
    "bounds",
    "delete",
    "simulation",
    "clip",
    "retopo",
    "remesh",
    "volume",
    "dissipation",
    "proxy",
    "clean",
    "camera",
    "frustum",
    "timeoffset",
    "rasterize",
    "fluid",
    "mesh",
    "emission",
    "light",
    "export",
    "decimate",
    "xform",
    "intersection",
    "sdf",
    "project",
    "carve",
    "motionblur"
]

json_file = "test.json"

data = {"data": []}

for i in range(16):
    print(f">>>> {i}")
    n_ = random.choice(n)
    n.remove(n_)
    d_ = random.choice(d)
    d.remove(d_)
    tags = []
    for j in range(3):
        t_ = random.choice(t)
        t.remove(t_)
        tags.append(t_)



    snippet_data = {
        "snippet_id": i,
        "snippet_name": n_,
        "description": d_,
        "tags": tags
    }
    data["data"].append(snippet_data)

with open(json_file, "w") as write_file:
    json.dump(data, write_file, indent=4)
