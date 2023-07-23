import bpy
import os
from ..main.common import *
from ..ExtensionHelper import ExtensionHelper

class MetalBase:

    def __init__(self):
        self.BasePath = bpy.context.preferences.addons["io_cp_extension"].preferences.depot_path
        self.image_format = "png"

    def create(self, eh: ExtensionHelper, Mat):
        CurMat = Mat.node_tree


        CurMat.nodes['Principled BSDF'].inputs['Specular'].default_value = 0

        mixRGB = CurMat.nodes.new("ShaderNodeMixRGB")
        mixRGB.location = (-200,200)
        mixRGB.hide = True
        mixRGB.blend_type = 'MULTIPLY'
        mixRGB.inputs[0].default_value = 1
        CurMat.links.new(mixRGB.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Base Color'])

        base_color = eh.get_texture("BaseColor")
        if base_color is not None:
            bColNode = CreateShaderNodeTexImage(CurMat, base_color, -800, -450, "BaseColor")
            CurMat.links.new(bColNode.outputs[0],mixRGB.inputs[2])
            CurMat.links.new(bColNode.outputs[1],CurMat.nodes['Principled BSDF'].inputs['Alpha'])

        base_color_scale = eh.get_vector("BaseColorScale")
        if base_color_scale is not None:
            dColScale = CreateShaderNodeRGB(CurMat, base_color_scale, -700, 500, "BaseColorScale")
            CurMat.links.new(dColScale.outputs[0],mixRGB.inputs[1])


        alpha_threshold = eh.get_scalar("AlphaThreshold")
        if alpha_threshold is not None:
            aThreshold = CreateShaderNodeValue(CurMat, alpha_threshold.scalar, -1000, 0, "AlphaThreshold")

        normal = eh.get_texture("Normal")
        if normal is not None:
            nMap = CreateShaderNodeNormalMap(CurMat, normal, -200, -300, "Normal")
            CurMat.links.new(nMap.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Normal'])

        mulNode = CurMat.nodes.new("ShaderNodeMixRGB")
        mulNode.inputs[0].default_value = 1
        mulNode.blend_type = 'MULTIPLY'
        mulNode.location = (-450,100)

        emissive_color = eh.get_color("EmissiveColor")
        if emissive_color is not None:
            emColor = CreateShaderNodeRGB(CurMat, emissive_color, -800, -200, "EmissiveColor")
            CurMat.links.new(emColor.outputs[0],mulNode.inputs[1])

        emissive = eh.get_texture("Emissive")
        if emissive is not None:
            emTexNode = CreateShaderNodeTexImage(CurMat, emissive, -800, 100, "Emissive")
            CurMat.links.new(emTexNode.outputs[0],mulNode.inputs[2])

        CurMat.links.new(mulNode.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Emission'])

        emissive_ev = eh.get_scalar("EmissiveEV")
        if emissive_ev is not None:
            CurMat.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = emissive_ev.scalar