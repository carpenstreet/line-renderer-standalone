from typing import Deque
import bpy
import random
from .utils_ftp import ftp_open


def object_to_Instance(Nodes_name, Download_Path, ftp, lst_obj, lst_setting, col_Asset):
    def import_object(obj, File_Name):

        Object_Name = File_Name[: File_Name.index(".fbx")]
        # Object가 파일안에 있는지 확인
        if Object_Name not in bpy.data.objects:
            ftp_open(File_Name, Download_Path, ftp)
            bpy.ops.import_scene.fbx(filepath=Download_Path + File_Name)
            lst_Object_to_Asset.append(bpy.context.selected_objects.pop())

            # 가져온 Object의 material을 "OPAQUE"로 바꿔줘야함
            bpy.data.materials[
                bpy.data.objects[Object_Name].material_slots[0].name
            ].blend_method = "OPAQUE"
        return Object_Name

    def apply_to_Instance(obj, Object_Name):
        for i in bpy.data.node_groups[Nodes_name].nodes:
            if i.name.endswith(obj):
                Instance_Name = i.name
                # Point_Instance일땐 inputs[1], Object Info일땐 inputs[0]
                if Instance_Name.startswith("Point"):
                    num = 1
                elif Instance_Name.startswith("Object"):
                    num = 0
                bpy.data.node_groups[Nodes_name].nodes[Instance_Name].inputs[
                    num
                ].default_value = bpy.data.objects[Object_Name]

    lst_Object_to_Asset = Deque()

    for obj in lst_obj:
        ftp.cwd("/ModelMakerAsset/FBX/" + obj)
        ftp.set_pasv(False)
        File_Name = random.choice(ftp.nlst())
        Object_Name = import_object(obj, File_Name)
        apply_to_Instance(obj, Object_Name)

    # lst_setting은 Point_Instance가 없으므로 불러오기만 함
    for obj in lst_setting:
        ftp.cwd("/ModelMakerAsset/FBX/" + obj)
        ftp.set_pasv(False)
        File_Name = random.choice(ftp.nlst())
        import_object(obj, File_Name)

    # 불러온 Object들을 기존의 콜렉션에서 unlink해주고 col_Asset에 넣어줌
    while lst_Object_to_Asset:
        obj = lst_Object_to_Asset.popleft()
        if obj.name in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.unlink(obj)
        else:
            for c in bpy.data.collections:
                if obj.name in c.objects:
                    c.objects.unlink(obj)
        col_Asset.objects.link(obj)
