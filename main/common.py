import os
import bpy
from bpy.types import Image
from ..data_types import *


def imageFromPath(Img,image_format,isNormal = False):
    # The speedtree materials use the same name textures for different plants this code was loading the same leaves on all of them
    Im = bpy.data.images.get(os.path.basename(Img)[:-4])    
    if Im and Im.filepath==Img[:-3]+ image_format:
        if Im.colorspace_settings.name != 'Non-Color':
            if isNormal:
                Im = None
        else:
            if not isNormal:
                Im = None
    else: 
        Im=None
    if not Im :
        Im = bpy.data.images.get(os.path.basename(Img)[:-4] + ".001")
        if Im and Im.filepath==Img[:-3]+ image_format:
            if Im.colorspace_settings.name != 'Non-Color':
                if isNormal:
                    Im = None
            else:
                if not isNormal:
                    Im = None
        else :
            Im = None
    
    if not Im:
        Im = bpy.data.images.new(os.path.basename(Img)[:-4],1,1)
        Im.source = "FILE"
        Im.filepath = Img[:-3]+ image_format
        if isNormal:
            Im.colorspace_settings.name = 'Non-Color'
    return Im


def CreateShaderNodeTexImage(cur_mat, image: Image = None, x = 0, y = 0, name = None):
    ImgNode = cur_mat.nodes.new("ShaderNodeTexImage")
    ImgNode.location = (x, y)
    ImgNode.hide = True
    if name is not None:
        ImgNode.label = name
    if image is not None:
        ImgNode.image = image

    return ImgNode


def CreateShaderNodeRGB(curMat, data: Color | Vector, x = 0, y = 0, name = None):
    rgbNode = curMat.nodes.new("ShaderNodeRGB")
    rgbNode.location = (x, y)
    rgbNode.hide = True
    if name is not None:
        rgbNode.label = name

    if isinstance(data, Color):
        rgbNode.outputs[0].default_value = (float(data.red / 255), float(data.green / 255), float(data.blue / 255), float(data.alpha / 255))
    elif isinstance(data, Vector):
        rgbNode.outputs[0].default_value = (data.x, data.y, data.z, data.w)
    else:
        raise Exception("Invalid data type")

    return rgbNode


def CreateShaderNodeValue(curMat, value = 0 , x = 0, y = 0, name = None):
    valNode = curMat.nodes.new("ShaderNodeValue")
    valNode.location = (x,y)
    valNode.outputs[0].default_value = float(value)
    valNode.hide = True
    if name is not None:
        valNode.label = name

    return valNode


def create_node(NG, type, loc, hide=True, operation=None, image=None, label=None, blend_type=None):
    Node=NG.new(type)
    Node.hide = hide
    Node.location = loc
    if operation:
        Node.operation=operation
    if image:
        Node.image=image
    if label:
        Node.label=label
    if blend_type:
        Node.blend_type=blend_type
    return Node


def CreateRebildNormalGroup(curMat, x = 0, y = 0,name = 'Rebuild Normal Z'):
    group = bpy.data.node_groups.get("Rebuild Normal Z")

    if group is None:
        group = bpy.data.node_groups.new("Rebuild Normal Z","ShaderNodeTree")
    
        GroupInN = group.nodes.new("NodeGroupInput")
        GroupInN.location = (-1400,0)
    
        GroupOutN = group.nodes.new("NodeGroupOutput")
        GroupOutN.location = (200,0)
    
        group.inputs.new('NodeSocketColor','Image')
        group.outputs.new('NodeSocketColor','Image')
    
        VMup = group.nodes.new("ShaderNodeVectorMath")
        VMup.location = (-1200,-200)
        VMup.operation = 'MULTIPLY'
        VMup.inputs[1].default_value[0] = 2.0
        VMup.inputs[1].default_value[1] = 2.0
    
        VSub = group.nodes.new("ShaderNodeVectorMath")
        VSub.location = (-1000,-200)
        VSub.operation = 'SUBTRACT'
        VSub.inputs[1].default_value[0] = 1.0
        VSub.inputs[1].default_value[1] = 1.0
    
        VDot = group.nodes.new("ShaderNodeVectorMath")
        VDot.location = (-800,-200)
        VDot.operation = 'DOT_PRODUCT'
    
        Sub = group.nodes.new("ShaderNodeMath")
        Sub.location = (-600,-200)
        Sub.operation = 'SUBTRACT'
        group.links.new(VDot.outputs[0],Sub.inputs[1])
        Sub.inputs[0].default_value = 1.020
    
        SQR = group.nodes.new("ShaderNodeMath")
        SQR.location = (-400,-200)
        SQR.operation = 'SQRT'

        Range = group.nodes.new("ShaderNodeMapRange")
        Range.location = (-200,-200)
        Range.clamp = True
        Range.inputs[1].default_value = -1.0

        Sep = group.nodes.new("ShaderNodeSeparateRGB")
        Sep.location = (-600,0)
        Comb = group.nodes.new("ShaderNodeCombineRGB")
        Comb.location = (-300,0)
        
        RGBCurvesConvert = group.nodes.new("ShaderNodeRGBCurve")
        RGBCurvesConvert.label = "Convert DX to OpenGL Normal"
        RGBCurvesConvert.hide = True
        RGBCurvesConvert.location = (-100,0)
        RGBCurvesConvert.mapping.curves[1].points[0].location = (0,1)
        RGBCurvesConvert.mapping.curves[1].points[1].location = (1,0)
    
        group.links.new(GroupInN.outputs[0],VMup.inputs[0])
        group.links.new(VMup.outputs[0],VSub.inputs[0])
        group.links.new(VSub.outputs[0],VDot.inputs[0])
        group.links.new(VSub.outputs[0],VDot.inputs[1])
        group.links.new(VDot.outputs["Value"],Sub.inputs[1])
        group.links.new(Sub.outputs[0],SQR.inputs[0])
        group.links.new(SQR.outputs[0],Range.inputs[0])
        group.links.new(GroupInN.outputs[0],Sep.inputs[0])
        group.links.new(Sep.outputs[0],Comb.inputs[0])
        group.links.new(Sep.outputs[1],Comb.inputs[1])
        group.links.new(Range.outputs[0],Comb.inputs[2])
        group.links.new(Comb.outputs[0],RGBCurvesConvert.inputs[1])
        group.links.new(RGBCurvesConvert.outputs[0],GroupOutN.inputs[0])
    
    ShaderGroup = curMat.nodes.new("ShaderNodeGroup")
    ShaderGroup.location = (x,y)
    ShaderGroup.hide = True
    ShaderGroup.node_tree = group
    ShaderGroup.name = name

    return ShaderGroup


def CreateShaderNodeNormalMap(curMat,path = None, x = 0, y = 0, name = None,image_format = 'png', nonCol = True):
    nMap = curMat.nodes.new("ShaderNodeNormalMap")
    nMap.location = (x,y)
    nMap.hide = True

    if path is not None:
        ImgNode = curMat.nodes.new("ShaderNodeTexImage")
        ImgNode.location = (x - 400, y)
        ImgNode.hide = True
        if name is not None:
            ImgNode.label = name
        if isinstance(path, Image):
            ImgNode.image = path
        else:
            ImgNode.image = imageFromPath(path,image_format,nonCol)

        NormalRebuildGroup = CreateRebildNormalGroup(curMat, x - 150, y, name + ' Rebuilt')

        curMat.links.new(ImgNode.outputs[0],NormalRebuildGroup.inputs[0])
        curMat.links.new(NormalRebuildGroup.outputs[0],nMap.inputs[1])

    return nMap


def createOverrideTable(matTemplateObj):
        OverList = matTemplateObj["overrides"]
        if OverList is None:
            OverList = matTemplateObj.get("Overrides")
        Output = {}
        Output["ColorScale"] = {}
        Output["NormalStrength"] = {}
        Output["RoughLevelsOut"] = {}
        Output["MetalLevelsOut"] = {}
        for x in OverList["colorScale"]:
            tmpName = x["n"]["$value"]
            tmpR = float(x["v"]["Elements"][0])
            tmpG = float(x["v"]["Elements"][1])
            tmpB = float(x["v"]["Elements"][2])
            Output["ColorScale"][tmpName] = (tmpR,tmpG,tmpB,1)
        for x in OverList["normalStrength"]:
            tmpName = x["n"]["$value"]
            tmpStrength = 0
            if x.get("v") is not None:
                tmpStrength = float(x["v"])
            Output["NormalStrength"][tmpName] = tmpStrength
        for x in OverList["roughLevelsOut"]:
            tmpName = x["n"]["$value"]
            tmpStrength0 = float(x["v"]["Elements"][0])
            tmpStrength1 = float(x["v"]["Elements"][1])
            Output["RoughLevelsOut"][tmpName] = [(tmpStrength0,tmpStrength0,tmpStrength0,1),(tmpStrength1,tmpStrength1,tmpStrength1,1)]
        for x in OverList["metalLevelsOut"]:
            tmpName = x["n"]["$value"]
            if x.get("v") is not None:
                tmpStrength0 = float(x["v"]["Elements"][0])
                tmpStrength1 = float(x["v"]["Elements"][1])
            else:
                tmpStrength0 = 0
                tmpStrength1 = 1
            Output["MetalLevelsOut"][tmpName] = [(tmpStrength0,tmpStrength0,tmpStrength0,1),(tmpStrength1,tmpStrength1,tmpStrength1,1)]
        return Output