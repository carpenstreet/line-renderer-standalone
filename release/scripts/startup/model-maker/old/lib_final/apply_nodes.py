# After extract vectors of vertex, delete copy roof and 'geometry nodes.001', and apply nodes to obj_origianl

import bpy

from ..lib_base.utils_select import deselect_all


def apply_nodes(lst, group1):

    deselect_all()

    # delete obj_copy
    obj_copy = lst[0][-1]
    bpy.context.view_layer.objects[obj_copy.name].select_set(True)
    bpy.ops.object.delete(use_global=False)

    # active_object를 original 개체로 변경해줌
    obj_original = lst[0][0]
    bpy.context.view_layer.objects.active = bpy.context.scene.objects.get(
        obj_original.name
    )

    # 원래 개체에 GeometryNodes가 적용되어 있다면 삭제해줌
    if bpy.data.objects[obj_original.name].modifiers.values():
        bpy.ops.object.modifier_remove(modifier="GeometryNodes")

    # 새로운 GeometryNodes를 적용해줌
    bpy.ops.object.modifier_add(type="NODES")
    lst_GeoNodes = [
        bpy.data.objects[obj_original.name].modifiers["GeometryNodes"].node_group
    ]
    bpy.data.objects[obj_original.name].modifiers[
        "GeometryNodes"
    ].node_group = bpy.data.node_groups[group1.name]
    bpy.data.node_groups.remove(lst_GeoNodes[0])
