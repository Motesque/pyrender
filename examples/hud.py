from pyrender import Mesh, Scene, Viewer, Texture, Node, Primitive, MetallicRoughnessMaterial, Material
from io import BytesIO
import numpy as np
import trimesh
import requests
from PIL import Image
from pyrender.constants import GLTF

duck_source = "https://github.com/KhronosGroup/glTF-Sample-Models/raw/master/2.0/Duck/glTF-Binary/Duck.glb"
duck = trimesh.load(BytesIO(requests.get(duck_source).content), file_type='glb')
duckmesh = Mesh.from_trimesh(list(duck.geometry.values())[0])

bg_idx = 0
bg_imgs = [Image.open("./models/background.png"), Image.open("./models/wood_uv.png"), None]
background_texs = [Texture(source=bg_img, source_channels="RGBA") if bg_img else None for bg_img in bg_imgs]
scene = Scene(ambient_light=np.array([0.2, 0.2, 0.2, 1.0]), bg_color=[255, 0, 255], background_texture=background_texs[0])

def create_2d_point_mesh(width, height, pts_2d, point_size_px):
    # create a triangle mesh
    def _rot_mat(angle_rad):
        return np.array([[np.cos(angle_rad), -np.sin(angle_rad)], [np.sin(angle_rad), np.cos(angle_rad)]], dtype=np.float32)

    if isinstance(pts_2d, list):
        pts_2d = np.array(pts_2d, dtype=np.float32)

    vertices = np.zeros((3, 3), dtype=np.float32)
    point_size_ndc = point_size_px/height
    vec = np.array([0, point_size_ndc])
    vertices[0, 0:2] = vec
    vertices[1, 0:2] = _rot_mat(np.radians(120)) @ vec
    vertices[2, 0:2] = _rot_mat(np.radians(-120)) @ vec
    mat = MetallicRoughnessMaterial(doubleSided=True, baseColorFactor=[1.0,0,0,1])

    instances = [np.eye(4) for i in range(pts_2d.shape[0])]
    for i in range(pts_2d.shape[0]):
        instances[i][0, 3] = (2 * pts_2d[i][0] - width) / height
        instances[i][1, 3] = pts_2d[i][1] / height * 2 - 1
        instances[i][2, 3] = -1
    prim = Primitive(positions=vertices,  mode=GLTF.TRIANGLES, material=mat, poses=instances)
    return Mesh(primitives=[prim])

pts_mesh = create_2d_point_mesh(640,480, [[0,0], [320,240], [640,480]], point_size_px=15)

duck_node = scene.add(duckmesh)
dn = scene.add_hud_node(Node(name="hud", mesh=pts_mesh))


Viewer(scene,
       run_in_thread=False,
        viewer_flags={"use_direct_lighting": True},
       viewport_size=(640, 480))
