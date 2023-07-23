import sys
import bpy
from io_scene_gltf2.blender.imp.gltf2_blender_image import BlenderImage
from .data_types import *

class ExtensionHelper():

    def __init__(self, gltf, data):
        self.__gltf = gltf
        self.__data = data
        self.__depot_path = bpy.context.preferences.addons["io_cp_extension"].preferences.depot_path

    def get_template(self):
        return self.__data["Template"]
    
    def __get_value(self, key: str, type: str):
        if key not in self.__data:
            print("Parameter " + key + " not found!")
            return None
        
        if self.__data[key]["$type"] != type:
            print("Parameter " + key + " is not a " + type + "! (" + self.__data[key]["$type"] + ")")
            return None
        
        return self.__data[key]["$value"]

    def get_color(self, key: str) -> Color:
        value = self.__get_value(key, "Color")
        if value is not None:
            return Color(value)
        return None

    def get_scalar(self, key: str) -> Scalar:
        value = self.__get_value(key, "Scalar")
        if value is not None:
            return Scalar(value)
        return None
    
    def get_vector(self, key: str) -> Vector:
        value = self.__get_value(key, "Vector")
        if value is not None:
            return Vector(value)
        return None

    def get_path(self, key: str):
        if "pathName" in self.__data[key]["$value"]:
            return self.__data[key]["$value"]["pathName"]
        return None
    
    def get_texture(self, key: str, is_normal: bool = False):
        if key not in self.__data:
            print("Parameter " + key + " not found!")
            return None
        
        if self.__data[key]["$type"] != "Texture":
            print("Parameter " + key + " is not an texture!")
            return None

        BlenderImage.create(self.__gltf, self.__data[key]['$value']['image'])
        pyimg = self.__gltf.data.images[self.__data[key]['$value']['image']]
        blender_image = bpy.data.images[pyimg.blender_image_name]

        if is_normal:
            blender_image.colorspace_settings.name = 'Non-Color'

        return blender_image