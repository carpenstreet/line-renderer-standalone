import bpy, bmesh

# roof의 배열을 뒤집어 줌(경우에 따라서 두번 실행해줘야함)
def flip_array():
    bpy.ops.object.convert(target="CURVE", keep_original=False)
    bpy.ops.object.convert(target="MESH", keep_original=False)


def clockwise_array():

    bpy.ops.object.editmode_toggle()
    me = bpy.context.object.data
    bm = bmesh.from_edit_mesh(me)
    bm.verts.ensure_lookup_table()
    # index of the start vertex
    initial = bm.verts[0]

    vert = initial
    prev = None
    for i in range(len(bm.verts)):
        print(vert.index, i)
        vert.index = i
        next = None
        adjacent = []
        for v in [e.other_vert(vert) for e in vert.link_edges]:
            if v != prev and v != initial:
                next = v
        if next == None:
            break
        prev, vert = vert, next

    bm.verts.sort()
    bmesh.update_edit_mesh(me)

    # 벡터의 외적이 음인지 양인지 비교해 flip_array()를 실행, 후에 다시 비교해서 flip_array()를 한번더 실행
    V1, V2, V3 = change_verts_to_vector()
    if (V1.cross(V2).z) > 0:
        bpy.ops.object.editmode_toggle()
        flip_array()
        bpy.ops.object.editmode_toggle()
        V1, V2, V3 = change_verts_to_vector()
        if (V1.cross(V2).z) > 0:
            bpy.ops.object.editmode_toggle()
            flip_array()
        else:
            bpy.ops.object.editmode_toggle()

    # V1,V2 외적이 양이라도 V2,V3가 음일 수 있으므로 한번더 확인해줌
    else:
        if (V2.cross(V3).z) > 0:
            bpy.ops.object.editmode_toggle()
            flip_array()
        bpy.ops.object.editmode_toggle()


# 꼭지점을 벡터로 바꿔줌
def change_verts_to_vector():
    bmesh.from_edit_mesh(
        bpy.context.object.data
    ).verts.ensure_lookup_table()  # 'verts' ensure_loopup_table() 켜주기
    V1 = (
        bmesh.from_edit_mesh(bpy.context.object.data).verts[1].co
        - bmesh.from_edit_mesh(bpy.context.object.data).verts[0].co
    )
    V2 = (
        bmesh.from_edit_mesh(bpy.context.object.data).verts[2].co
        - bmesh.from_edit_mesh(bpy.context.object.data).verts[0].co
    )
    V3 = (
        bmesh.from_edit_mesh(bpy.context.object.data).verts[3].co
        - bmesh.from_edit_mesh(bpy.context.object.data).verts[0].co
    )
    return V1, V2, V3
