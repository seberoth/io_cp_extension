import bpy
import os
from ..main.common import *
from ..data_types import *
from ..ExtensionHelper import ExtensionHelper

class MeshDecalParallax:

    def __init__(self):
        self.BasePath = bpy.context.preferences.addons["io_cp_extension"].preferences.depot_path
        self.image_format = "png"


    def create(self, eh: ExtensionHelper, Mat):
        CurMat = Mat.node_tree
        CurMat.nodes['Principled BSDF'].inputs['Specular'].default_value = 0
#Diffuse
        mixRGB = CurMat.nodes.new("ShaderNodeMixRGB")
        mixRGB.location = (-500,500)
        mixRGB.hide = True
        mixRGB.blend_type = 'MULTIPLY'
        mixRGB.inputs[0].default_value = 1
        CurMat.links.new(mixRGB.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Base Color'])

        mulNode = CurMat.nodes.new("ShaderNodeMath")
        mulNode.operation = 'MULTIPLY'
        mulNode.location = (-500,450)

        diffuse_alpha = eh.get_scalar("DiffuseAlpha")
        if diffuse_alpha is not None:
            mulNode.inputs[0].default_value = diffuse_alpha.scalar
        else:
            mulNode.inputs[0].default_value = 1

        dTexMapping = CurMat.nodes.new("ShaderNodeMapping")
        dTexMapping.label = "UVMapping"
        dTexMapping.location = (-1000,300)

        diffuse_texture = eh.get_texture("DiffuseTexture")
        if diffuse_texture is not None:
            dImgNode = CreateShaderNodeTexImage(CurMat, diffuse_texture, -800, 500, "DiffuseTexture")
            CurMat.links.new(dTexMapping.outputs[0],dImgNode.inputs[0])
            CurMat.links.new(dImgNode.outputs[0],mixRGB.inputs[2])
            CurMat.links.new(dImgNode.outputs[1],mulNode.inputs[1])

        uv_offset_x = eh.get_scalar("UVOffsetX")
        if uv_offset_x is not None:
            dTexMapping.inputs[1].default_value[0] = uv_offset_x.scalar

        uv_offset_y = eh.get_scalar("UVOffsetY")
        if uv_offset_y is not None:
            dTexMapping.inputs[1].default_value[1] = uv_offset_y.scalar

        uv_rotation = eh.get_scalar("UVRotation")
        if uv_rotation is not None:
            dTexMapping.inputs[2].default_value[0] = uv_rotation.scalar
            dTexMapping.inputs[2].default_value[1] = uv_rotation.scalar

        uv_scale_x = eh.get_scalar("UVScaleX")
        if uv_scale_x is not None:
            dTexMapping.inputs[3].default_value[0] = uv_scale_x.scalar

        uv_scale_y = eh.get_scalar("UVScaleY")
        if uv_scale_y is not None:
            dTexMapping.inputs[3].default_value[1] = uv_scale_y.scalar

        UVNode = CurMat.nodes.new("ShaderNodeTexCoord")
        UVNode.location = (-1200,300)
        CurMat.links.new(UVNode.outputs[2],dTexMapping.inputs[0])

        CurMat.links.new(mulNode.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Alpha'])

        diffuse_color = eh.get_color("DiffuseColor")
        if diffuse_color is not None:
            dColor = CreateShaderNodeRGB(CurMat, diffuse_color, -700, 550, "DiffuseColor")
            CurMat.links.new(dColor.outputs[0],mixRGB.inputs[1])

        normal_texture = eh.get_texture("NormalTexture")
        if normal_texture is not None:
            nMap = CreateShaderNodeNormalMap(CurMat, normal_texture, -200, -250, "NormalTexture")
            CurMat.links.new(nMap.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Normal'])

        normal_alpha = eh.get_scalar("NormalAlpha")
        if normal_alpha is not None:
            norAlphaVal = CreateShaderNodeValue(CurMat, normal_alpha.scalar, -1200, -450, "NormalAlpha")

        normal_alphaTex = eh.get_texture("NormalAlphaTex", True)
        if normal_alphaTex is not None:
            nAImgNode = CreateShaderNodeTexImage(CurMat, normal_alphaTex, -1200, -500, "NormalAlphaTex")

        mulNode1 = CurMat.nodes.new("ShaderNodeMath")

        roughness_scale = eh.get_scalar("RoughnessScale")
        if roughness_scale is not None:
            mulNode1.inputs[0].default_value = roughness_scale.scalar
        else:
            mulNode1.inputs[0].default_value = 1

        mulNode1.operation = 'MULTIPLY'
        mulNode1.location = (-500,-100)
        CurMat.links.new(mulNode1.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Roughness'])

        roughness_texture = eh.get_texture("RoughnessTexture", True)
        if roughness_texture is not None:
            rImgNode = CreateShaderNodeTexImage(CurMat, roughness_texture, -800, 100, "RoughnessTexture")
            CurMat.links.new(rImgNode.outputs[0],mulNode1.inputs[1])


        mulNode2 = CurMat.nodes.new("ShaderNodeMath")

        metalness_scale = eh.get_scalar("MetalnessScale")
        if metalness_scale is not None:
            mulNode2.inputs[0].default_value = metalness_scale.scalar
        else:
            mulNode2.inputs[0].default_value = 1

        mulNode2.operation = 'MULTIPLY'
        mulNode2.location = (-500,200)
        CurMat.links.new(mulNode2.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Metallic'])

        metalness_texture = eh.get_texture("MetalnessTexture", True)
        if metalness_texture is not None:
            mImgNode = CreateShaderNodeTexImage(CurMat, metalness_texture, -800, 200, "MetalnessTexture")
            CurMat.links.new(mImgNode.outputs[0],mulNode2.inputs[1])
'''     
        if "SecondaryMask"in Data:
            print('SecondaryMask detected', Data['SecondaryMask'])
            
        if "SecondaryMaskUVScale"in Data:
            print('SecondaryMaskUVScale detected - ', Data['SecondaryMaskUVScale'])
            
        if "SecondaryMaskInfluence"in Data:
            print('SecondaryMaskInfluence detected', Data['SecondaryMaskInfluence'])
            
        if "UseNormalAlphaTex"in Data:
            print('UseNormalAlphaTex detected', Data['UseNormalAlphaTex'])
        if "NormalsBlendingMode"in Data:
            print('NormalsBlendingMode detected', Data['NormalsBlendingMode'])
        
        if "AlphaMaskContrast"in Data:
            print('NormalsBlendingMode detected', Data['NormalsBlendingMode'])

        if "RoughnessMetalnessAlpha"in Data:
            print('RoughnessMetalnessAlpha detected', Data['NormalsBlendingMode'])

        if "DepthThreshold"in Data:
            print('DepthThreshold detected', Data['DepthThreshold'])

        if "HeightTexture"in Data:
            print('HeightTexture detected', Data['HeightTexture'])
        if "HeightStrength"in Data:
            print('HeightStrength detected', Data['HeightStrength'])
'''