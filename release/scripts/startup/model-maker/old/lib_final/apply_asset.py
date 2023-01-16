import bpy

# GeometryNodes 외부에서 modeling-asset을 넣어줍니다.
def apply_asset(verts, lst_setting):

    lst_asset_setting = []

    # lst_setting에 해당되는 modeling-asset들의 개체 이름을 lst_asset_setting에 넣어둠(ex."Window_1m_003")
    for setting in lst_setting:
        for i in bpy.data.collections["Asset"].objects:
            if (i.name).startswith(setting):
                lst_asset_setting.append(i.name)
                break

    # GeometryNodes의 asset 넣는 칸 밑에서부터 오브젝트를 넣어줌.
    # 밑에서부터 창문이 있고, 그 위로 door 등등이 들어갈 거라 창문의 갯수만큼 빈칸에 넣어주면 갯수가 맞음.
    cnt = 0
    print(lst_asset_setting)
    for i in reversed(bpy.context.object.modifiers["GeometryNodes"].keys()):
        if cnt < len(verts):
            if bpy.context.object.modifiers["GeometryNodes"][i] is None:
                bpy.context.object.modifiers["GeometryNodes"][i] = bpy.data.objects[
                    lst_asset_setting[0]
                ]
                cnt += 1

        else:
            if bpy.context.object.modifiers["GeometryNodes"][i] is None:
                bpy.context.object.modifiers["GeometryNodes"][i] = bpy.data.objects[
                    lst_asset_setting[1]
                ]
