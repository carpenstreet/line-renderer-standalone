import bpy
from .utils_ftp import ftp_open


def append_NodeTree(Nodes_name, Download_Path, ftp):
    File_Name = Nodes_name + ".blend"  # Nodes_name을 파일명으로 동일하게 해줘야함
    ftp.cwd("/ModelMakerAsset/RND_NODES/OneRoom")
    ftp.set_pasv(False)
    ftp_open(File_Name, Download_Path, ftp)

    bpy.ops.wm.append(
        filepath=File_Name,
        directory=Download_Path + File_Name + "\\NodeTree\\",
        filename=Nodes_name,
        autoselect=False,
        active_collection=False,
        instance_object_data=False,
        use_recursive=False,
    )
