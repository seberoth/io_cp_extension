import bpy
import os
from ..main.common import *
from ..ExtensionHelper import ExtensionHelper

class MeshDecalGradientMapReColor:

    def __init__(self):
        self.BasePath = bpy.context.preferences.addons["io_cp_extension"].preferences.depot_path
        self.image_format = "png"

    def create(self, eh: ExtensionHelper, Mat):
        Mat.blend_method = 'HASHED'
        Mat.shadow_method = 'HASHED'

        CurMat = Mat.node_tree

        mask_texture = eh.get_texture("MaskTexture")
        if mask_texture is not None:
            aImgNode =  CreateShaderNodeTexImage(CurMat, mask_texture, -300, -100, "MaskTexture")
            CurMat.links.new(aImgNode.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Alpha'])


        CurMat.nodes['Principled BSDF'].inputs['Specular'].default_value = 0

        normal_texture = eh.get_texture("NormalTexture")
        if normal_texture is not None:
            nMap = CreateShaderNodeNormalMap(CurMat, normal_texture, -800, -250, "NormalTexture")
            CurMat.links.new(nMap.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Normal'])

        diffuse_texture = eh.get_texture("DiffuseTexture")
        if diffuse_texture is not None:
            dImgNode = CreateShaderNodeTexImage(CurMat, diffuse_texture, -600, 250, "DiffuseTexture")

        gradient_map = eh.get_texture("GradientMap")
        if gradient_map is not None:
            gImgNode = CreateShaderNodeTexImage(CurMat, gradient_map, -300, 250, "GradientMap")

        CurMat.links.new(dImgNode.outputs[0],gImgNode.inputs[0])
        CurMat.links.new(gImgNode.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Base Color'])