import bpy, bmesh
import random


def almost_same(a, b):
    if abs(a - b) < 0.0001:
        return True
    else:
        return False


# 개체의 벽면부(normal!=(0,0,+-1))만 magin_UV로 설정
def magic_UV(lst):

    # magic_uv addon을 켜줌
    bpy.ops.preferences.addon_enable(module="magic_uv")

    obj_original = lst[0][0]
    bpy.context.view_layer.objects.active = bpy.context.scene.objects.get(
        obj_original.name
    )
    bpy.ops.object.editmode_toggle()
    ob = bpy.context.object
    bm = bmesh.from_edit_mesh(ob.data)
    if ob.mode == "EDIT":
        bpy.ops.mesh.select_mode(type="FACE")
        bm.faces.ensure_lookup_table()
        for face in bm.faces:
            if almost_same(face.normal[0], 0) and almost_same(face.normal[1], 0):
                face.select_set(False)
            else:
                face.select_set(True)

    bpy.ops.uv.muv_uvw_box_map(assign_uvmap=True)
    bpy.ops.object.editmode_toggle()


# ImportFTP해서 받아온 material_collection에서 "Wall"로 시작되는 material을 적용
def apply_materials_wall(lst):

    obj_original = lst[0][0]

    # 만약 개체에 이미 material이 있다면 모두 삭제해줌
    for i in bpy.data.objects[obj_original.name].material_slots:
        bpy.ops.object.material_slot_remove()

    lst_material_wall = []
    for i in bpy.data.materials:
        if (i.name).startswith("Wall"):
            lst_material_wall.append(i.name)
    mateiral_wall = random.choice(lst_material_wall)
    bpy.context.active_object.data.materials.append(bpy.data.materials[mateiral_wall])


# ImportFTP해서 받아온 material_collection에서 "Roof"로 시작되는 material을 적용
def apply_materials_roof(lst):

    obj_original = lst[0][0]

    lst_material_roof = []
    for i in bpy.data.materials:
        if (i.name).startswith("Roof"):
            lst_material_roof.append(i.name)

    mateiral_roof = random.choice(lst_material_roof)
    bpy.context.active_object.data.materials.append(bpy.data.materials[mateiral_roof])

    # magic_UV 함수에서 벽면부가 선택이 된 상태라 선택을 모두 해제, 지붕부와 바닥부를 선택 후 material을 assign 해줌
    bpy.ops.object.editmode_toggle()
    ob = bpy.context.object
    bm = bmesh.from_edit_mesh(ob.data)
    if ob.mode == "EDIT":
        bpy.ops.mesh.select_mode(type="FACE")
        bm.faces.ensure_lookup_table()
        for face in bm.faces:
            if almost_same(face.normal[0], 0) and almost_same(face.normal[1], 0):
                face.select_set(True)
            else:
                face.select_set(False)

    bpy.data.objects[obj_original.name].active_material_index = 1
    bpy.ops.object.material_slot_assign()
    bpy.ops.object.editmode_toggle()
