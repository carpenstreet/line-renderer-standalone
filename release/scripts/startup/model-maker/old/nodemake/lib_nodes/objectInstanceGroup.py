import bpy


def make_ObjectInstanceGroup():

    bpy.data.node_groups.new("ObjectInstanceGroup", "GeometryNodeTree")
    OIgroup = bpy.data.node_groups["ObjectInstanceGroup"]
    link = OIgroup.links.new

    Inputs = OIgroup.nodes.new("NodeGroupInput")
    PointSeparate = OIgroup.nodes.new("GeometryNodeLegacyPointSeparate")
    PointSeparate.inputs[1].default_value = "BoundaryPoint"
    link(Inputs.outputs[0], PointSeparate.inputs[0])

    PointInstance = OIgroup.nodes.new("GeometryNodeLegacyPointInstance")
    PointInstance.instance_type = "OBJECT" 
    link(Inputs.outputs[1], PointInstance.inputs[1])
    link(PointSeparate.outputs[0], PointInstance.inputs[0])

    Outputs = OIgroup.nodes.new("NodeGroupOutput")
    link(PointInstance.outputs[0], Outputs.inputs[0])