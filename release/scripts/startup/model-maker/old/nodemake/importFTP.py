import ftplib, os, shutil
import bpy

from ..lib_base.utils_select import deselect_all
from .lib_FTP.append_nodetree import append_NodeTree
from .lib_FTP.object_to_Instance import object_to_Instance
from .lib_FTP.collection_to_Instance import collection_to_Instance


def importFTP(Nodes_name, lst_obj, lst_collection, lst_setting):

    # "Test"라는 폴더를 만들어주고 FTP로 불러온 파일들을 폴더에 저장해줌
    Folder_Name = "Test"
    try:
        os.mkdir(Folder_Name)
    except FileExistsError:
        pass
    Download_Path = Folder_Name + "/"
    # FTP 서버명과 로그인을 해줌
    ftp = ftplib.FTP()
    ftp.connect("175.209.222.13", 21)
    ftp.login("acon3d", "acon3d")

    # 노드를 불러옴
    append_NodeTree(Nodes_name, Download_Path, ftp)
    deselect_all()

    # 불러온 에셋을 담아줄 "Asset" Collection을 생성
    col_Asset = bpy.data.collections.get("Asset")
    if not col_Asset:
        col_Asset = bpy.data.collections.new("Asset")
        # bpy.context.scene.collection.children.link(col_Asset) #TODO: scene에 숨겨두는게 좋을지 판단

    # 단일 에셋들을 불러옴(리스트로 받아서)
    object_to_Instance(Nodes_name, Download_Path, ftp, lst_obj, lst_setting, col_Asset)
    # Collection 에셋들을 불러옴(리스트로 받아서)
    collection_to_Instance(Nodes_name, Download_Path, ftp, lst_collection, col_Asset)

    # FTP 작업이 끝나면 FTP 로그아웃을 해주고 Folder도 삭제해줌
    ftp.quit()
    shutil.rmtree(Folder_Name)
    col_Asset.hide_viewport = True
    col_Asset.hide_render = True
