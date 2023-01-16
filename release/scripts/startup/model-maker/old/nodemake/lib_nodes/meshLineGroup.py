import bpy
import math


def make_MeshLineGroup():

    # new node wall
    bpy.data.node_groups.new("MeshLineGroup", "GeometryNodeTree")
    MLgroup = bpy.data.node_groups["MeshLineGroup"]
    link = MLgroup.links.new

    Inputs = MLgroup.nodes.new("NodeGroupInput")
    Subtract = MLgroup.nodes.new("ShaderNodeVectorMath")
    Subtract.operation = "SUBTRACT"
    link(Inputs.outputs[0], Subtract.inputs[1])
    link(Inputs.outputs[1], Subtract.inputs[0])

    Add = MLgroup.nodes.new("ShaderNodeMath")
    Add.operation = "ADD"
    Add.inputs[1].default_value = 2.0

    MeshLine = MLgroup.nodes.new(type="GeometryNodeMeshLine")
    MeshLine.mode = "END_POINTS"
    MeshLine.inputs[0].default_value = 2
    link(Inputs.outputs[2], MeshLine.inputs[0])
    link(Inputs.outputs[2], Add.inputs[0])
    link(Add.outputs[0], MeshLine.inputs[0])
    link(Inputs.outputs[0], MeshLine.inputs[2])
    link(Inputs.outputs[1], MeshLine.inputs[3])

    VectorDistance1 = MLgroup.nodes.new(type="GeometryNodeLegacyAttributeVectorMath")
    VectorDistance1.operation = "DISTANCE"
    VectorDistance1.input_type_b = "VECTOR"
    link(MeshLine.outputs[0], VectorDistance1.inputs[0])
    VectorDistance1.inputs[1].default_value = "position"
    link(Inputs.outputs[0], VectorDistance1.inputs[4])
    VectorDistance1.inputs[9].default_value = "distFromStart"

    VectorDistance2 = MLgroup.nodes.new(type="GeometryNodeLegacyAttributeVectorMath")
    VectorDistance2.operation = "DISTANCE"
    VectorDistance2.input_type_b = "VECTOR"
    link(VectorDistance1.outputs[0], VectorDistance2.inputs[0])
    VectorDistance2.inputs[1].default_value = "position"
    link(Inputs.outputs[1], VectorDistance2.inputs[4])
    VectorDistance2.inputs[9].default_value = "distFromEnd"

    Compare1 = MLgroup.nodes.new(type="GeometryNodeLegacyAttributeMath")
    Compare1.operation = "COMPARE"
    Compare1.input_type_b = "FLOAT"
    Compare1.input_type_c = "FLOAT"
    link(VectorDistance2.outputs[0], Compare1.inputs[0])
    Compare1.inputs[1].default_value = "distFromStart"
    Compare1.inputs[6].default_value = 0.001
    Compare1.inputs[7].default_value = "isStartPoint"

    Compare2 = MLgroup.nodes.new(type="GeometryNodeLegacyAttributeMath")
    Compare2.operation = "COMPARE"
    Compare2.input_type_b = "FLOAT"
    Compare2.input_type_c = "FLOAT"
    link(Compare1.outputs[0], Compare2.inputs[0])
    Compare2.inputs[1].default_value = "distFromEnd"
    Compare2.inputs[6].default_value = 0.001
    Compare2.inputs[7].default_value = "isEndPoint"

    Add_attribute = MLgroup.nodes.new(type="GeometryNodeLegacyAttributeMath")
    link(Compare2.outputs[0], Add_attribute.inputs[0])
    Add_attribute.inputs[1].default_value = "isStartPoint"
    Add_attribute.inputs[3].default_value = "isEndPoint"
    Add_attribute.inputs[7].default_value = "BoundaryPoint"

    Align = MLgroup.nodes.new(type="GeometryNodeLegacyAlignRotationToVector")
    Align.axis = "Y"
    link(Add_attribute.outputs[0], Align.inputs[0])
    link(Subtract.outputs[0], Align.inputs[4])

    PointRotate = MLgroup.nodes.new(type="GeometryNodeLegacyRotatePoints")
    PointRotate.type = "AXIS_ANGLE"
    PointRotate.inputs[4].default_value = -math.pi / 2
    link(Align.outputs[0], PointRotate.inputs[0])

    Outputs = MLgroup.nodes.new("NodeGroupOutput")
    link(PointRotate.outputs[0], Outputs.inputs[0])

    VectorDivide = MLgroup.nodes.new("ShaderNodeVectorMath")
    VectorDivide.operation = "DIVIDE"
    link(Subtract.outputs[0], VectorDivide.inputs[0])
    link(Add.outputs[0], VectorDivide.inputs[1])

    VectorAdd = MLgroup.nodes.new("ShaderNodeVectorMath")
    VectorAdd.operation = "ADD"
    link(Inputs.outputs[0], VectorAdd.inputs[0])
    link(VectorDivide.outputs[0], VectorAdd.inputs[1])

    VectorLength = MLgroup.nodes.new("ShaderNodeVectorMath")
    VectorLength.operation = "LENGTH"
    link(Subtract.outputs[0], VectorLength.inputs[0])

    Divide = MLgroup.nodes.new("ShaderNodeMath")
    Divide.operation = "DIVIDE"
    link(VectorLength.outputs[1], Divide.inputs[0])
    link(Add.outputs[0], Divide.inputs[1])

    PointSeparate = MLgroup.nodes.new(type="GeometryNodeLegacyPointSeparate")
    PointSeparate.inputs[1].default_value = "BoundaryPoint"
    link(PointRotate.outputs[0], PointSeparate.inputs[0])

    VectorDistance3 = MLgroup.nodes.new(type="GeometryNodeLegacyAttributeVectorMath")
    VectorDistance3.operation = "DISTANCE"
    VectorDistance3.input_type_b = "VECTOR"
    link(PointSeparate.outputs[0], VectorDistance3.inputs[0])
    VectorDistance3.inputs[1].default_value = "position"
    link(VectorAdd.outputs[0], VectorDistance3.inputs[4])
    VectorDistance3.inputs[9].default_value = "distFromStart"

    Compare3 = MLgroup.nodes.new(type="GeometryNodeLegacyAttributeMath")
    Compare3.operation = "COMPARE"
    Compare3.input_type_b = "FLOAT"
    Compare3.input_type_c = "FLOAT"
    link(VectorDistance3.outputs[0], Compare3.inputs[0])
    Compare3.inputs[1].default_value = "distFromStart"
    link(Divide.outputs[0], Compare3.inputs[6])
    Compare3.inputs[7].default_value = "isFirstPoint"

    PointSeparate2 = MLgroup.nodes.new(type="GeometryNodeLegacyPointSeparate")
    PointSeparate2.inputs[1].default_value = "isFirstPoint"
    link(Compare3.outputs[0], PointSeparate2.inputs[0])
    link(PointSeparate2.outputs[0], Outputs.inputs[1])
    link(PointSeparate2.outputs[1], Outputs.inputs[2])
