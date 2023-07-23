import bpy
import os
from ..main.common import *
from ..ExtensionHelper import ExtensionHelper

class Skin:

    def __init__(self):
        self.BasePath = bpy.context.preferences.addons["io_cp_extension"].preferences.depot_path
        self.image_format = "png"

    def create(self, eh: ExtensionHelper,Mat):
        CurMat = Mat.node_tree

#SSS/s
        sVcol = CurMat.nodes.new("ShaderNodeVertexColor")
        sVcol.location = (-1400,250)

        sSepRGB = CurMat.nodes.new("ShaderNodeSeparateRGB")
        sSepRGB.location = (-1200,250)

        sMultiply = CurMat.nodes.new("ShaderNodeMath")
        sMultiply.location = (-800,250)
        sMultiply.operation = 'MULTIPLY'
        sMultiply.inputs[1].default_value = (0.05)

        CurMat.links.new(sVcol.outputs[0],sSepRGB.inputs[0])
        CurMat.links.new(sSepRGB.outputs[1],sMultiply.inputs[0])
        CurMat.links.new(sMultiply.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Subsurface'])
        CurMat.nodes['Principled BSDF'].inputs['Subsurface Color'].default_value = (0.8, 0.14908, 0.0825199, 1)
        
#Albedo/a
        mixRGB = CurMat.nodes.new("ShaderNodeMixRGB")
        mixRGB.location = (-200,300)
        mixRGB.hide = True
        mixRGB.blend_type = 'MULTIPLY'

        albedo = eh.get_texture("Albedo")
        if albedo is not None:
            aImgNode = CreateShaderNodeTexImage(CurMat, albedo, -800, 550, "Albedo")
            CurMat.links.new(aImgNode.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Base Color'])
            CurMat.links.new(aImgNode.outputs[0],mixRGB.inputs[1])

        tint_color = eh.get_color("TintColor")
        if tint_color is not None:
            tColor = CreateShaderNodeRGB(CurMat, tint_color, -400, 500, "TintColor")
            CurMat.links.new(tColor.outputs[0],mixRGB.inputs[2])
        
        tint_color_mask = eh.get_texture("TintColorMask", True)
        if tint_color_mask is not None:
            tmaskNode = CreateShaderNodeTexImage(CurMat, tint_color_mask, -500, 550, "TintColorMask")
            CurMat.links.new(tmaskNode.outputs[0],mixRGB.inputs[0])

        CurMat.links.new(mixRGB.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Base Color'])

#ROUGHNES+MASK/rm

        roughness = eh.get_texture("Roughness", True)
        if roughness is not None:
            rImgNode = CreateShaderNodeTexImage(CurMat, roughness, -1600, 50, "Roughness")
        else:
            rImgNode = None

        rmSep = CurMat.nodes.new("ShaderNodeSeparateRGB")
        rmSep.location = (-1300,50)
        rmSep.hide = True
		
        rmSub = CurMat.nodes.new("ShaderNodeMath")
        rmSub.location = (-1100,0)
        rmSub.hide = True
        rmSub.operation = 'SUBTRACT'
        rmSub.inputs[1].default_value = (0.5)

        rmMul = CurMat.nodes.new("ShaderNodeMath")
        rmMul.location = (-900,-100)
        rmMul.hide = True
        rmMul.operation = 'MULTIPLY'
		
#NORMAL/n
        nMDCoordinates = CurMat.nodes.new("ShaderNodeTexCoord")
        nMDCoordinates.hide = True
        nMDCoordinates.location =  (-2000,-850)

        nVecMulAspectA = CurMat.nodes.new("ShaderNodeVectorMath")
        nVecMulAspectA.hide = True
        nVecMulAspectA.location =  (-1800,-1000)
        nVecMulAspectA.operation = "MULTIPLY"
        nVecMulAspectA.inputs[1].default_value = (1, 2, 1)
		
        nVecMulAspectB = CurMat.nodes.new("ShaderNodeVectorMath")
        nVecMulAspectB.hide = True
        nVecMulAspectB.location =  (-1800,-1150)
        nVecMulAspectB.operation = "MULTIPLY"
        nVecMulAspectB.inputs[1].default_value = (1, 2, 1)

        nVecMulA = CurMat.nodes.new("ShaderNodeVectorMath")
        nVecMulA.hide = True
        nVecMulA.location =  (-1600,-850)
        nVecMulA.operation = "MULTIPLY"
		
        nVecMulB = CurMat.nodes.new("ShaderNodeVectorMath")
        nVecMulB.hide = True
        nVecMulB.location =  (-1600,-1150)
        nVecMulB.operation = "MULTIPLY"
		
        nVecModA = CurMat.nodes.new("ShaderNodeVectorMath")
        nVecModA.hide = True
        nVecModA.location =  (-1400,-850)
        nVecModA.operation = "MODULO"
        nVecModA.inputs[1].default_value = (0.5, 1, 1)
		
        nVecModB = CurMat.nodes.new("ShaderNodeVectorMath")
        nVecModB.hide = True
        nVecModB.location =  (-1400,-1150)
        nVecModB.operation = "MODULO"
        nVecModB.inputs[1].default_value = (0.5, 1, 1)

        nVecAdd = CurMat.nodes.new("ShaderNodeVectorMath")
        nVecAdd.hide = True
        nVecAdd.location =  (-1200,-1150)
        nVecAdd.operation = "ADD"
        nVecAdd.inputs[1].default_value = (0.5, 0, 0)

        nOverlay1 = CurMat.nodes.new("ShaderNodeMixRGB")
        nOverlay1.hide = True
        nOverlay1.location =  (-1000,-300)
        nOverlay1.blend_type ='OVERLAY'
		
        nOverlay2 = CurMat.nodes.new("ShaderNodeMixRGB")
        nOverlay2.hide = True
        nOverlay2.location =  (-700,-300)
        nOverlay2.blend_type ='OVERLAY'
		
        mdOverlay = CurMat.nodes.new("ShaderNodeMixRGB")
        mdOverlay.hide = True
        mdOverlay.location =  (-700,-450)
        mdOverlay.blend_type ='OVERLAY'
        mdOverlay.inputs[0].default_value = (1)

        nNormalMap = CurMat.nodes.new("ShaderNodeNormalMap")
        nNormalMap.location = (-300, -300)
        nNormalMap.hide = True
		
        nRebuildNormal = CreateRebildNormalGroup(CurMat)
        nRebuildNormal.hide = True
        nRebuildNormal.location =  (-500,-300)

        normal = eh.get_texture("Normal", True)
        if normal is not None:
            nMap = CreateShaderNodeTexImage(CurMat, normal, -1800, -300, "Normal")
            nMap.image.colorspace_settings.name='Non-Color'
        else:
            nMap = None
	
        detail_normal = eh.get_texture("DetailNormal", True)
        if detail_normal is not None:
            dnMap = CreateShaderNodeTexImage(CurMat, detail_normal, -1800, -450, "DetailNormal")
        else:
            dnMap = None
			
        detail_normal_influence = eh.get_scalar("DetailNormalInfluence")
        if detail_normal_influence is not None:
            nDNInfluence = CreateShaderNodeValue(CurMat, detail_normal_influence.scalar, -1250, -200, "DetailNormalInfluence")

        micro_detail = eh.get_texture("MicroDetail", True)
        if micro_detail is not None:
            mdMapA = CreateShaderNodeTexImage(CurMat, micro_detail, -1100, -450, "MicroDetail")
            mdMapB = CreateShaderNodeTexImage(CurMat, micro_detail, -1100, -650, "MicroDetail")
        else:
            mdMapA = None
            mdMapB = None

        micro_detail_uv_scale_01 = eh.get_scalar("MicroDetailUVScale01")
        if micro_detail_uv_scale_01 is not None:
            mdScale01 = CreateShaderNodeValue(CurMat, micro_detail_uv_scale_01.scalar, -2000, -1000, "MicroDetailUVScale01")

        micro_detail_uv_scale_02 = eh.get_scalar("MicroDetailUVScale02")
        if micro_detail_uv_scale_02 is not None:
            mdScale02 = CreateShaderNodeValue(CurMat, micro_detail_uv_scale_02.scalar, -2000, -1150, "MicroDetailUVScale02")

        micro_detail_influence = eh.get_scalar("MicroDetailInfluence")
        if micro_detail_influence is not None:
            mdInfluence = CreateShaderNodeValue(CurMat, micro_detail_influence.scalar, -1250, -100, "MicroDetailInfluence")

        detailmap_squash = eh.get_texture("Detailmap_Squash", True)
        if detailmap_squash is not None:
            ndSqImgNode = CreateShaderNodeTexImage(CurMat, detailmap_squash, -2000, 50, "Detailmap_Squash")

        detailmap_stretch = eh.get_texture("Detailmap_Squash", True)
        if detailmap_stretch is not None:
            ndStImg = CreateShaderNodeTexImage(CurMat, detailmap_stretch, -2000, 0, "Detailmap_Stretch")

        if rImgNode is not None:
            CurMat.links.new(rImgNode.outputs[0],rmSep.inputs[0])
        CurMat.links.new(rmSep.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Roughness'])
        CurMat.links.new(rmSep.outputs[2],rmSub.inputs[0])
        CurMat.links.new(rmSub.outputs[0],rmMul.inputs[0])
        CurMat.links.new(rmMul.outputs[0],nOverlay2.inputs[0])
        CurMat.links.new(mdInfluence.outputs[0],rmMul.inputs[1])

        if nMap is not None:
            CurMat.links.new(nMap.outputs[0],nOverlay1.inputs[1])
        if dnMap is not None:
            CurMat.links.new(dnMap.outputs[0],nOverlay1.inputs[2])
        CurMat.links.new(nDNInfluence.outputs[0],nOverlay1.inputs[0])

        CurMat.links.new(nMDCoordinates.outputs["UV"],nVecMulA.inputs[0])
        CurMat.links.new(nMDCoordinates.outputs["UV"],nVecMulB.inputs[0])
        CurMat.links.new(mdScale01.outputs[0],nVecMulAspectA.inputs[0])
        CurMat.links.new(mdScale02.outputs[0],nVecMulAspectB.inputs[0])
        CurMat.links.new(nVecMulAspectA.outputs[0],nVecMulA.inputs[1])
        CurMat.links.new(nVecMulAspectB.outputs[0],nVecMulB.inputs[1])
        CurMat.links.new(nVecMulA.outputs[0],nVecModA.inputs[0])
        CurMat.links.new(nVecMulB.outputs[0],nVecModB.inputs[0])

        if mdMapA is not None:
            CurMat.links.new(nVecModA.outputs[0],mdMapA.inputs[0])
        CurMat.links.new(nVecModB.outputs[0],nVecAdd.inputs[0])

        if mdMapB is not None:
            CurMat.links.new(nVecAdd.outputs[0],mdMapB.inputs[0])

        if mdMapA is not None:
            CurMat.links.new(mdMapA.outputs[0],mdOverlay.inputs[1])
        if mdMapB is not None:
            CurMat.links.new(mdMapB.outputs[0],mdOverlay.inputs[2])
		
        CurMat.links.new(nOverlay1.outputs[0],nOverlay2.inputs[1])
        CurMat.links.new(mdOverlay.outputs[0],nOverlay2.inputs[2])

        CurMat.links.new(nOverlay2.outputs[0],nRebuildNormal.inputs[0])
        CurMat.links.new(nRebuildNormal.outputs[0],nNormalMap.inputs[1])

        CurMat.links.new(nNormalMap.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Normal'])

#OTHER
        blood_color = eh.get_color("BloodColor")
        if blood_color is not None:
            bfColor = CreateShaderNodeRGB(CurMat, blood_color, -2000, 300, "BloodColor")

        bloodflow = eh.get_texture("Bloodflow")
        if bloodflow is not None:
            bfImgNode = CreateShaderNodeTexImage(CurMat, bloodflow, -2000, 350, "Bloodflow")