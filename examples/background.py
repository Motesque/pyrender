from pyrender import Mesh, Scene, Viewer, Texture
from io import BytesIO
import numpy as np
import trimesh
import requests
from PIL import Image

duck_source = "https://github.com/KhronosGroup/glTF-Sample-Models/raw/master/2.0/Duck/glTF-Binary/Duck.glb"
duck = trimesh.load(BytesIO(requests.get(duck_source).content), file_type='glb')
duckmesh = Mesh.from_trimesh(list(duck.geometry.values())[0])

# create all available backgrounds
bg_idx = 0
bg_imgs = [Image.open("./models/background.png"), Image.open("./models/wood_uv.png"), None]
background_texs = [Texture(source=bg_img, source_channels="RGBA") if bg_img else None for bg_img in bg_imgs]

scene = Scene(ambient_light=np.array([1.0, 1.0, 1.0, 1.0]), bg_color=[255, 0, 255], background_texture=background_texs[0])
scene.add(duckmesh)


def on_background_toggle(vwr):
    global bg_idx
    bg_idx = (bg_idx + 1) % 3
    scene.background_texture = background_texs[bg_idx]


Viewer(scene,
       registered_keys={"b": on_background_toggle},
       run_in_thread=False,
       viewport_size=(640, 480))
