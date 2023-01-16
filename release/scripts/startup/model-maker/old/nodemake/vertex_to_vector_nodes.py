##OneRoom_Nodes copy and join vertex_to_Vector nodes + MeshLinegroup/ObjectBBox/ObjectInstance

import bpy, math, mathutils
import random
from .lib_nodes.objectInstanceGroup import make_ObjectInstanceGroup
from .lib_nodes.objectBBoxGroup import make_ObjectBBoxGroup
from .lib_nodes.meshLineGroup import make_MeshLineGroup
from .importFTP import importFTP


def vertex_to_vector_nodes(
    Nodes_name, plain_verts, lst_obj, lst_collection, lst_setting
):

    # Node가 파일에 있는지 여부로 FTP를 호출함(Asset이 있다고 하더라도 내부에서 걸러주기 때문에 Node명을 기준으로 함)
    if not Nodes_name in bpy.data.node_groups:
        importFTP(Nodes_name, lst_obj, lst_collection, lst_setting)

    # Node 기본 세팅
    new_geometry_nodes = bpy.data.node_groups[Nodes_name].copy()
    group1 = bpy.data.node_groups[new_geometry_nodes.name]
    link = group1.links.new
    GroupInput = group1.nodes.new(type="NodeGroupInput")
    cnt = 0

    # 문이 필요한 Node인지 확인(있으면 FaceEntrance 노드가 있을거임)
    door_index = None
    if "FaceEntrance" in group1.nodes:
        door_index = random.choice(range(len(plain_verts)))

    # 꼭지점 갯수만큼 Vector와 그에 해당하는 Node들 생성
    for i in range(len(plain_verts)):

        Vector = group1.nodes.new(type="FunctionNodeInputVector")
        Vector.vector[0] = plain_verts[i][0]
        Vector.vector[1] = plain_verts[i][1]
        Vector.vector[2] = 0
        Vector.label = "Vector {}".format(cnt)
        Vector.name = "Vector {}".format(cnt)

        if not "MeshLineGroup" in bpy.data.node_groups:
            make_MeshLineGroup()
            make_ObjectBBoxGroup()
            make_ObjectInstanceGroup()

        MeshLineGroup = group1.nodes.new(type="GeometryNodeGroup")
        MeshLineGroup.node_tree = bpy.data.node_groups["MeshLineGroup"]
        MeshLineGroup.label = "MeshLineGroup {}".format(cnt)
        MeshLineGroup.name = "MeshLineGroup {}".format(cnt)
        link(Vector.outputs[0], MeshLineGroup.inputs[0])

        ObjectBBoxGroup = group1.nodes.new(type="GeometryNodeGroup")
        ObjectBBoxGroup.node_tree = bpy.data.node_groups["ObjectBBoxGroup"]
        ObjectBBoxGroup.label = "ObjectBBoxGroup {}".format(cnt)
        ObjectBBoxGroup.name = "ObjectBBoxGroup {}".format(cnt)
        # door가 있으면 MeshLineGroup의 두번째 아웃풋으로 연결
        if door_index is not None:
            if MeshLineGroup.name == "MeshLineGroup {}".format(door_index):
                link(MeshLineGroup.outputs[1], ObjectBBoxGroup.inputs[0])
            else:
                link(MeshLineGroup.outputs[0], ObjectBBoxGroup.inputs[0])
        else:
            link(MeshLineGroup.outputs[0], ObjectBBoxGroup.inputs[0])
        link(GroupInput.outputs[-1], ObjectBBoxGroup.inputs[1])

        ObjectInstanceGroup = group1.nodes.new(type="GeometryNodeGroup")
        ObjectInstanceGroup.node_tree = bpy.data.node_groups["ObjectInstanceGroup"]
        ObjectInstanceGroup.label = "ObjectInstanceGroup {}".format(cnt)
        ObjectInstanceGroup.name = "ObjectInstanceGroup {}".format(cnt)
        # door가 있으면 MeshLineGroup의 두번째 아웃풋으로 연결
        if door_index is not None:
            if MeshLineGroup.name == "MeshLineGroup {}".format(door_index):
                link(MeshLineGroup.outputs[1], ObjectInstanceGroup.inputs[0])
            else:
                link(MeshLineGroup.outputs[0], ObjectInstanceGroup.inputs[0])
        else:
            link(MeshLineGroup.outputs[0], ObjectInstanceGroup.inputs[0])
        link(GroupInput.outputs[-2], ObjectInstanceGroup.inputs[1])
        group1.inputs[-1].name = "Window"

        # 벽 길이에서 window_size로 나눔
        window_size = 3
        vec_0 = mathutils.Vector(plain_verts[i])
        vec_1 = mathutils.Vector(plain_verts[(i + 1) % (len(plain_verts))])
        length = math.floor(((vec_1 - vec_0).length) / window_size)
        MeshLineGroup.inputs[2].default_value = length

        link(GroupInput.outputs[-1], MeshLineGroup.inputs[2])
        group1.inputs[-1].min_value = 0
        cnt += 1

    # 각각의 노드들을 묶어줄 JoinGeometry 생성
    MeshLineJoin = group1.nodes.new(type="GeometryNodeJoinGeometry")
    MeshLineJoin.label = "MeshLineJoin"
    MeshWindowJoin = group1.nodes.new(type="GeometryNodeJoinGeometry")
    MeshWindowJoin.label = "MeshWindowJoin"
    ObjectBBoxJoin = group1.nodes.new(type="GeometryNodeJoinGeometry")
    ObjectBBoxJoin.label = "ObjectBBoxJoin"
    ObjectInstanceJoin = group1.nodes.new(type="GeometryNodeJoinGeometry")
    ObjectInstanceJoin.label = "ObjectInstanceJoin"

    # 생성한 노드들 link
    for i in range(len(plain_verts)):

        link(
            group1.nodes["Vector {}".format((i + 1) % len(plain_verts))].outputs[0],
            group1.nodes["MeshLineGroup {}".format(i)].inputs[1],
        )

        link(
            group1.nodes["MeshLineGroup {}".format(i)].outputs[0],
            MeshLineJoin.inputs[0],
        )

        # door_index가 있다면 분리해서 넣어줘야함, 없으면 모두 MeahLine의 0번 input에서 넣어줌
        if door_index is not None:
            if MeshLineGroup.name == "MeshLineGroup {}".format(door_index):
                link(
                    group1.nodes["MeshLineGroup {}".format(i)].outputs[1],
                    MeshWindowJoin.inputs[0],
                )
            else:
                link(
                    group1.nodes["MeshLineGroup {}".format(i)].outputs[0],
                    MeshWindowJoin.inputs[0],
                )
        else:
            link(
                group1.nodes["MeshLineGroup {}".format(i)].outputs[0],
                MeshWindowJoin.inputs[0],
            )

        link(
            group1.nodes["ObjectBBoxGroup {}".format(i)].outputs[0],
            ObjectBBoxJoin.inputs[0],
        )
        link(
            group1.nodes["ObjectInstanceGroup {}".format(i)].outputs[0],
            ObjectInstanceJoin.inputs[0],
        )

    link(MeshLineJoin.outputs[0], group1.nodes["MeshLineEntrance"].inputs[0])
    link(ObjectBBoxJoin.outputs[0], group1.nodes["ObjectBBoxEntrance"].inputs[0])
    link(
        ObjectInstanceJoin.outputs[0], group1.nodes["ObjectInstanceEntrance"].inputs[0]
    )

    # door가 있으면 FaceEntrance에 넣어줌
    if door_index is not None:
        link(
            group1.nodes["MeshLineGroup {}".format(door_index)].outputs[2],
            group1.nodes["FaceEntrance"].inputs[0],
        )

    return group1
