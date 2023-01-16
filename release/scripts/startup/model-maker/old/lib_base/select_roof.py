##select roof face, and copy
##deselect original and select copy

import bpy, bmesh


def almost_same(a, b):
    if abs(a - b) < 0.0001:
        return True
    else:
        return False


# normal=(0,0,1)인 면만 select
def select_roof():
    bpy.ops.object.editmode_toggle()
    ob = bpy.context.object
    bm = bmesh.from_edit_mesh(ob.data)
    if ob.mode == "EDIT":
        bpy.ops.mesh.select_mode(type="FACE")
        bm.faces.ensure_lookup_table()  # ensure_loopup_table() 켜주기
        for face in bm.faces:
            if (
                almost_same(face.normal[0], 0)
                and almost_same(face.normal[1], 0)
                and almost_same(face.normal[2], 1)
            ):
                face.select_set(True)
            else:
                face.select_set(False)
        ob.data.update()
        bpy.ops.mesh.duplicate()
        bpy.ops.mesh.separate(type="SELECTED")

    bpy.ops.object.editmode_toggle()
