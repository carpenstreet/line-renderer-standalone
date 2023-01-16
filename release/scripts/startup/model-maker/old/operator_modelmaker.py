import bpy

from .lib_base.move_to_z import move_to_z
from .lib_base.select_roof import select_roof
from .lib_base.utils_select import change_active
from .lib_base.clockwise_array import clockwise_array

from .nodemake.vertex_to_vector_nodes import vertex_to_vector_nodes

from .lib_final.z_angle import z_angle
from .lib_final.apply_nodes import apply_nodes
from .lib_final.apply_asset import apply_asset
from .lib_final.apply_materials import (
    apply_materials_roof,
    apply_materials_wall,
    magic_UV,
)


def operator_modelmaker(self):
    ##lib_base
    # 개체를 z=0으로 옮겨주고 roof만 따로 떼어내줌
    move_to_z()
    select_roof()

    lst = []
    obj_dup = bpy.context.selected_objects
    lst.append(obj_dup)

    # 원래 개체에서 roof로 active를 바꿔주고 roof의 꼭지점을 시계방향으로 배열해줌
    change_active()
    bpy.context.scene.objects[obj_dup[-1].name].select_set(True)
    clockwise_array()

    verts = [vert.co for vert in bpy.context.active_object.data.vertices]
    plain_verts = [vert.to_tuple() for vert in verts]

    # roof의 꼭지점을 받아온 plain_verts를 Node에 넣어줌
    Nodes_name = self.Nodes_name
    lst_setting = self.lst_setting
    lst_obj = self.lst_obj
    lst_collection = self.lst_collection

    group1 = vertex_to_vector_nodes(
        Nodes_name, plain_verts, lst_obj, lst_collection, lst_setting
    )

    ##lib_fianl
    # Node가 완성되면 원래 개체에 Node, asset(바깥에서 넣어주는 에셋들), material을 적용해줌
    z_angle(plain_verts, group1)
    apply_nodes(lst, group1)
    apply_asset(verts, lst_setting)
    # magic_UV와 벽면부, 지붕부 material을 따로 적용해줌
    magic_UV(lst)
    apply_materials_wall(lst)
    apply_materials_roof(lst)
    del lst
