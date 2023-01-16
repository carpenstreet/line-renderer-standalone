import bpy
from .utils_ftp import ftp_open


def collection_to_Instance(Nodes_name, Download_Path, ftp, lst_collection, col_Asset):
    def model_asset_to_collection(collection):

        Collection_Name = collection + "_Collection"
        File_Name = Collection_Name + ".fbx"

        # Collection이 파일안에 있는지 확인
        if Collection_Name not in bpy.data.collections:
            ftp_open(File_Name, Download_Path, ftp)
            bpy.ops.import_scene.fbx(filepath=Download_Path + File_Name)

            # Collection 파일의 Object들을 불러오고 기존의 콜렉션에서 unlink해주고
            # 새로운 콜렉션을 만든 뒤 그 콜렉션을 col_Asset에 넣어줌
            col_Collection = bpy.data.collections.new(Collection_Name)
            for obj in bpy.context.selected_objects:
                if obj.name in bpy.context.scene.collection.objects:
                    bpy.context.scene.collection.objects.unlink(obj)
                else:
                    for c in bpy.data.collections:
                        if obj.name in c.objects:
                            c.objects.unlink(obj)
                col_Collection.objects.link(obj)
            col_Asset.children.link(col_Collection)

        for i in bpy.data.node_groups[Nodes_name].nodes:
            if i.name.endswith(collection):
                Instance_Name = i.name

                # Point_Instance일땐 inputs[2], Collection Info일땐 inputs[0]
                if Instance_Name.startswith("Point"):
                    num = 2
                elif Instance_Name.startswith("Collection"):
                    num = 0
                bpy.data.node_groups[Nodes_name].nodes[Instance_Name].inputs[
                    num
                ].default_value = bpy.data.collections[Collection_Name]

    for collection in lst_collection:
        ftp.cwd("/ModelMakerAsset/FBX/" + collection)
        ftp.set_pasv(False)
        model_asset_to_collection(collection)
