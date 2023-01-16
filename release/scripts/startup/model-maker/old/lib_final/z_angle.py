import bpy, mathutils, math

# 개체가 z축을 기점으로 회전되어 있다면 각 꼭지점들을 이은 벡터를 x축과 비교해
# 가장 낮은 값을 반환해서 GeometryNodes에 있는 "Z_Axis" 노드에 넣어줌
def z_angle(plain_verts, group1):

    lst_verts = []
    for i in range(len(plain_verts)):
        vec_0 = mathutils.Vector(plain_verts[i])
        vec_1 = mathutils.Vector(plain_verts[(i + 1) % (len(plain_verts))])
        n_vec = (vec_1 - vec_0).normalized()

        # 만약 회전되어 있지 않다면 무조건 하나의 벡터는 y축과 평행, 그 때에 for문을 break해주면 lst_verts는 빈 리스트가 됨
        if n_vec == mathutils.Vector((0.0, 1.0, 0.0)) or n_vec == mathutils.Vector(
            (0.0, -1.0, 0.0)
        ):
            break
        vec_x = mathutils.Vector((1.0, 0.0, 0.0))
        degree_x = math.degrees(math.acos(n_vec.dot(vec_x)))
        lst_verts.append(min(degree_x, 180 - degree_x))

    group1.nodes["Z_Axis"].outputs[0].default_value = min(lst_verts) if lst_verts else 0
