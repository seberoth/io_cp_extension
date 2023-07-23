import bpy
import os
from ..main.common import *
from ..ExtensionHelper import ExtensionHelper

import json

class Hair:

    def __init__(self):
        self.BasePath = bpy.context.preferences.addons["io_cp_extension"].preferences.depot_path
        self.image_format = "png"

    def create(self, eh: ExtensionHelper, Mat):
        hp_path = eh.get_path("HairProfile")
        if hp_path is None:
            return

        file = open(self.BasePath + hp_path + ".json",mode='r')
        profile = json.loads(file.read())["Data"]["RootChunk"]
        file.close()

        Mat.blend_method = 'HASHED'
        Mat.shadow_method = 'HASHED'

        CurMat = Mat.node_tree

        strand_alpha = eh.get_texture("Strand_Alpha")
        aImgNode = CreateShaderNodeTexImage(CurMat, strand_alpha, -300, -150, "Strand_Alpha")
        CurMat.links.new(aImgNode.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Alpha'])

        CurMat.nodes['Principled BSDF'].inputs['Specular'].default_value = 0

        strand_gradient = eh.get_texture("Strand_Gradient", True)
        gImgNode = CreateShaderNodeTexImage(CurMat, strand_gradient, -1100, 50, "Strand_Gradient")

        RootToTip = CurMat.nodes.new("ShaderNodeValToRGB")
        RootToTip.location = (-800,50)
        RootToTip.label = "GradientEntriesRootToTip"

        RootToTip.color_ramp.elements.remove(RootToTip.color_ramp.elements[0])
        counter = 0
        for Entry in profile["gradientEntriesRootToTip"]:
            if counter == 0:
                RootToTip.color_ramp.elements[0].position = Entry.get("value",0)
                colr = Entry["color"]
                RootToTip.color_ramp.elements[0].color = (float(colr["Red"])/255,float(colr["Green"])/255,float(colr["Blue"])/255,float(1))
            else:
                element = RootToTip.color_ramp.elements.new(Entry.get("value",0))
                colr = Entry["color"]
                element.color =  (float(colr["Red"])/255,float(colr["Green"])/255,float(colr["Blue"])/255,float(1))
            counter = counter + 1

        CurMat.links.new(gImgNode.outputs[0],RootToTip.inputs[0])

        strand_id = eh.get_texture("Strand_ID", True)
        idImgNode = CreateShaderNodeTexImage(CurMat, strand_id, -1100, 350, "Strand_ID")

        ID = CurMat.nodes.new("ShaderNodeValToRGB")
        ID.location = (-800,350)
        ID.label = "GradientEntriesID"

        ID.color_ramp.elements.remove(ID.color_ramp.elements[0])
        counter = 0
        for Entry in profile["gradientEntriesID"]:
            if counter == 0:
                ID.color_ramp.elements[0].position = Entry.get("value",0)
                colr = Entry["color"]
                ID.color_ramp.elements[0].color = (float(colr["Red"])/255,float(colr["Green"])/255,float(colr["Blue"])/255,float(1))
            else:
                element = ID.color_ramp.elements.new(Entry.get("value",0))
                colr = Entry["color"]
                element.color = (float(colr["Red"])/255,float(colr["Green"])/255,float(colr["Blue"])/255,float(1))
            counter = counter + 1
			
        CurMat.links.new(idImgNode.outputs[0],ID.inputs[0])

        mulNode = CurMat.nodes.new("ShaderNodeMixRGB")
        mulNode.inputs[0].default_value = 1
        mulNode.blend_type = 'MULTIPLY'
        mulNode.location = (-400,200)

        CurMat.links.new(ID.outputs[0],mulNode.inputs[1])
        CurMat.links.new(RootToTip.outputs[0],mulNode.inputs[2])

        gamma0 = CurMat.nodes.new("ShaderNodeGamma")
        gamma0.inputs[1].default_value = 2.2
        gamma0.location = (-200,200)
        CurMat.links.new(mulNode.outputs[0],gamma0.inputs[0])

        CurMat.links.new(gamma0.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Base Color'])

        flow = eh.get_texture("Flow")
        nMap = CreateShaderNodeNormalMap(CurMat, flow, -200, -250, "Flow")
        CurMat.links.new(nMap.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Normal'])