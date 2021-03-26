from pyrender import Mesh, Scene, Viewer, Texture, Node, OrthographicCamera
from io import BytesIO
import numpy as np
import trimesh
import requests
from PIL import Image

duck_source = "https://github.com/KhronosGroup/glTF-Sample-Models/raw/master/2.0/Duck/glTF-Binary/Duck.glb"
duck = trimesh.load(BytesIO(requests.get(duck_source).content), file_type='glb')
duckmesh = Mesh.from_trimesh(list(duck.geometry.values())[0])

bg_idx = 0
bg_imgs = [Image.open("./models/background.png"), Image.open("./models/wood_uv.png"), None]
background_texs = [Texture(source=bg_img, source_channels="RGBA") if bg_img else None for bg_img in bg_imgs]
scene = Scene(ambient_light=np.array([0.2, 0.2, 0.2, 1.0]), bg_color=[255, 0, 255], background_texture=background_texs[0])

unit_cube = trimesh.load("./models/unitcube.gltf", file_type='gltf')
unit_cube_mesh = Mesh.from_trimesh(list(unit_cube.geometry.values())[0])
scene.add(duckmesh)
node = Node(name="hud", matrix= np.eye(4), mesh=unit_cube_mesh)
dn = scene.add_hud_node(node)
dn.scale = [0.5,0.5,0.5]
dn.translation = [0,0,-10]


Viewer(scene,
       run_in_thread=False,
       viewport_size=(640, 480))
