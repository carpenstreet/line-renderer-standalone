import bpy
from bpy.app.handlers import persistent


def init_setting():
    init_screen = bpy.data.screens["ACON3D"].areas[0].spaces[0]
    init_screen.shading.type = "SOLID"
    init_screen.overlay.show_ortho_grid = True
    init_screen.overlay.show_floor = True
    init_screen.overlay.show_axis_x = True
    init_screen.overlay.show_axis_y = True


@persistent
def load_handler(dummy):
    bpy.app.timers.register(delayed_load_handler)


def delayed_load_handler():
    init_setting()


######register
def register():
    bpy.app.handlers.load_post.append(load_handler)


def unregister():
    bpy.app.handlers.load_post.remove(load_handler)


if __name__ == "__main__":
    register()
