from pyrender import Mesh, Scene, Viewer
from io import BytesIO
import numpy as np
import trimesh
import requests
import time
duck_source = "https://github.com/KhronosGroup/glTF-Sample-Models/raw/master/2.0/Duck/glTF-Binary/Duck.glb"

duck = trimesh.load(BytesIO(requests.get(duck_source).content), file_type='glb')
duckmesh = Mesh.from_trimesh(list(duck.geometry.values())[0])
scene = Scene(ambient_light=np.array([1.0, 1.0, 1.0, 1.0]))
scene.add(duckmesh)

orig_positions = duckmesh.primitives[0].positions
vwr = Viewer(scene, run_in_thread=True,
                   render_flags={"cull_faces": False, "all_wireframe": False},
                   use_raymond_lighting=True,
                   bg_color=[255, 0, 255])

while vwr.is_active:
    with vwr.render_lock:
        duckmesh.primitives[0].positions = orig_positions + np.random.randn(*orig_positions.shape) * 2
    time.sleep(0.1)