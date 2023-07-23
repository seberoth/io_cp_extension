import bpy
from pprint import pprint
from io_scene_gltf2.io.com.gltf2_io import TextureInfo
from io_scene_gltf2.io.com.gltf2_io_extensions import Extension
from io_scene_gltf2.blender.imp.gltf2_blender_image import BlenderImage

import sys

imports = [
    "io_cp_extension.data_types",
    "io_cp_extension.ExtensionHelper",
    "io_cp_extension.main.common",
    "io_cp_extension.material_types.hair",
    "io_cp_extension.material_types.meshdecal",
    "io_cp_extension.material_types.meshdecalgradientmaprecolor",
    "io_cp_extension.material_types.meshdecalparallax",
    "io_cp_extension.material_types.metalbase",
    "io_cp_extension.material_types.multilayered",
    "io_cp_extension.material_types.skin"
]

for imp in imports:
    if imp in sys.modules:
        del sys.modules[imp]

from .ExtensionHelper import ExtensionHelper
from .material_types.hair import Hair
from .material_types.meshdecal import MeshDecal
from .material_types.meshdecalgradientmaprecolor import MeshDecalGradientMapReColor
from .material_types.meshdecalparallax import MeshDecalParallax
from .material_types.metalbase import MetalBase
from .material_types.multilayered import Multilayered
from .material_types.skin import Skin

bl_info = {
    "name": "Cyberpunk 2077 Material Test",
    "category": "Generic",
    "version": (1, 0, 0),
    "blender": (3, 1, 0),
    "location": "File > Import > glTF 2.0",
    "description": "Cyberpunk 2077 Material Test"
}

# glTF extensions are named following a convention with known prefixes.
# See: https://github.com/KhronosGroup/glTF/tree/main/extensions#about-gltf-extensions
# also: https://github.com/KhronosGroup/glTF/blob/main/extensions/Prefixes.md
glTF_extension_name = "CP_MaterialInstance"


class GLTF_CP_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = "io_cp_extension"

    depot_path: bpy.props.StringProperty(
        subtype="DIR_PATH",
        default="",
        description="Location of Depot"
    )


    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "depot_path", text="Location of Depot")


class glTF2ImportUserExtension:

    def __init__(self):
        self.extensions = [Extension(name=glTF_extension_name, extension={}, required=False)]

    def gather_import_gltf_before_hook(self, gltf):
        print("Import started")

    def gather_import_material_after_hook(self, gltf_material, vertex_color, blender_mat, gltf):
        if hasattr(gltf_material.extensions, glTF_extension_name) == False:
            pass

        blender_mat.use_nodes = True

        eh = ExtensionHelper(gltf, gltf_material.extensions[glTF_extension_name])

        match eh.get_template():
            case "engine\\materials\\multilayered.mt":
                multilayered = Multilayered()
                multilayered.create(eh, blender_mat)

            # Test
            case "base\\materials\\cloth_mov_multilayered.mt":
                multilayered = Multilayered()
                multilayered.create(eh, blender_mat)

            case "base\\materials\\mesh_decal_gradientmap_recolor.mt":
                meshDecalGradientMapReColor = MeshDecalGradientMapReColor()
                meshDecalGradientMapReColor.create(eh, blender_mat)

            case "base\\materials\\hair.mt":
                hair = Hair()
                hair.create(eh, blender_mat)

            case "engine\\materials\\metal_base.remt" | "engine\\materials\\metal_base_proxy.mt":
                metalBase = MetalBase()
                metalBase.create(eh, blender_mat)
            
            case "base\\materials\\mesh_decal_parallax.mt" | "base\\materials\\parallaxscreen.mt" :
                meshDecalParallax = MeshDecalParallax()
                meshDecalParallax.create(eh, blender_mat)

            case "base\\materials\\skin.mt":
                skin = Skin()
                skin.create(eh, blender_mat)

            case "base\\materials\\mesh_decal.mt":
                meshDecal = MeshDecal()
                meshDecal.create(eh, blender_mat)

            case _:
                print(eh.get_template())
            
        blender_mat.blend_method='HASHED'


def register():
    bpy.utils.register_class(GLTF_CP_AddonPreferences)


def unregister():
    bpy.utils.unregister_class(GLTF_CP_AddonPreferences)