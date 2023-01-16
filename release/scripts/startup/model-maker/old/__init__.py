bl_info = {
    "name": "Track1 Addon",
    "author": "youjin@acon3d.com",
    "version": (0, 0, 2),
    "blender": (2, 80, 0),
    "location": "",
    "description": "Auto Modeling",
    "warning": "",
    "doc_url": "",
    "category": "ACON3D",
}


import bpy

from . import wm
from types import ModuleType


# =========================================================================
# Registration:
# =========================================================================

importedLibrary = [wm]


def register():
    for item in importedLibrary:
        if not isinstance(item, ModuleType):
            continue
        try:
            item.register()
        except Exception as e:
            print(f"ABLER: Failed to register {str(item.__name__)}\n" + str(e))


def unregister():
    for item in importedLibrary.reverse():
        if not isinstance(item, ModuleType):
            continue
        try:
            item.unregister()
        except Exception as e:
            print(f"ABLER: Failed to unregister {str(item.__name__)}\n" + str(e))


if __name__ == "__main__":
    register()
