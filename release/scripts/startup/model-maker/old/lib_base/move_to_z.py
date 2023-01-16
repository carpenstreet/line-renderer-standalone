import bpy


def move_to_z():
    # 개체의 scale을 (1,1,1)로 변경함
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # 개체의 Origin을 Center-of-Mass로 설정한 뒤 z=0으로 이동
    bpy.ops.object.origin_set(type="ORIGIN_CENTER_OF_MASS")
    bpy.context.object.location[2] = 0
