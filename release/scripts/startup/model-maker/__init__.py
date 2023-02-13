bl_info = {
    "name": "Line Renderer",
    "author": "aamo@acon3d.com",
    "version": (1, 0, 0),
    "blender": (3, 1, 2),
    "location": "",
    "description": "Line Style Rendering",
    "warning": "",
    "doc_url": "",
    "category": "ACON3D",
}

import bpy

from . import pref
from . import model_maker_control
from types import ModuleType

# =========================================================================
# Registration:
# =========================================================================

importedLibrary = [pref, model_maker_control]


def register():
    for item in importedLibrary:
        if not isinstance(item, ModuleType):
            continue
        try:
            item.register()
        except Exception as e:
            print(f"ABLER: Failed to register {str(item.__name__)}\n{str(e)}")


def unregister():
    for item in importedLibrary.reverse():
        if not isinstance(item, ModuleType):
            continue
        try:
            item.unregister()
        except Exception as e:
            print(f"ABLER: Failed to unregister {str(item.__name__)}\n{str(e)}")


if __name__ == "__main__":
    register()
