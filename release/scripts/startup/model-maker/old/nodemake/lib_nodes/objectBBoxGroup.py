import bpy


def make_ObjectBBoxGroup():

    bpy.data.node_groups.new("ObjectBBoxGroup", "GeometryNodeTree")
    OBgroup = bpy.data.node_groups["ObjectBBoxGroup"]
    link = OBgroup.links.new

    Inputs = OBgroup.nodes.new("NodeGroupInput")
    PointSeparate = OBgroup.nodes.new("GeometryNodeLegacyPointSeparate")
    PointSeparate.inputs[1].default_value = "BoundaryPoint"
    link(Inputs.outputs[0], PointSeparate.inputs[0])

    PointScale = OBgroup.nodes.new("GeometryNodeLegacyPointScale")
    PointScale.input_type = "VECTOR"
    PointScale.inputs[2].default_value[1] = -50
    link(PointSeparate.outputs[0], PointScale.inputs[0])

    ObjectInfo = OBgroup.nodes.new("GeometryNodeObjectInfo")
    link(Inputs.outputs[1], ObjectInfo.inputs[0])

    BoundingBox = OBgroup.nodes.new("GeometryNodeBoundBox")
    link(ObjectInfo.outputs[3], BoundingBox.inputs[0])

    PointInstance = OBgroup.nodes.new("GeometryNodeLegacyPointInstance")
    PointInstance.instance_type = "GEOMETRY" 
    link(BoundingBox.outputs[0], PointInstance.inputs[3])
    link(PointScale.outputs[0], PointInstance.inputs[0])

    Outputs = OBgroup.nodes.new("NodeGroupOutput")
    link(PointInstance.outputs[0], Outputs.inputs[0])