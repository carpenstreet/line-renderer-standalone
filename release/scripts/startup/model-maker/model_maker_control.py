import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper
from .architecture import line_render


class LineRendererPanel(bpy.types.Panel):
    bl_label = "LineRenderer Panel"
    bl_idname = "DH_PT_model_maker_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LineRenderer"

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="FILE_3D")

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Line Render")
        row = layout.row()
        row.operator("wm.open_reference_image")
        row = layout.row()
        row.operator("wm.save_line_render")

        row = layout.row()
        row.label(text="Export")
        row = layout.row()
        row.operator("wm.save_as_mainfile", text="Save Blend")


class OpenReferenceImageOperator(bpy.types.Operator, ImportHelper):
    """Open line render reference image"""

    bl_idname = "wm.open_reference_image"
    bl_label = "Open Image"
    bl_options = {"REGISTER", "UNDO"}

    image_extension = "*.png;*.jpg;*psd"
    index: bpy.props.IntProperty(name="Index", default=0, options={"HIDDEN"})
    filter_glob: bpy.props.StringProperty(default=image_extension, options={"HIDDEN"})

    def execute(self, context):
        new_image = bpy.data.images.load(self.filepath)
        # TODO: new_image를 render
        # image = context.scene.camera.data.background_images[self.index]
        # image.image = new_image
        return {"FINISHED"}


class SaveLineRenderImageOperator(bpy.types.Operator, ExportHelper):
    """Save line render image"""

    bl_idname = "wm.save_line_render"
    bl_label = "Save Line Render"
    bl_options = {"REGISTER", "UNDO"}

    filename_ext = '.png'

    def execute(self, context):
        tuple_arg = (2.5, 2.5, 5)
        path = self.filepath
        line_render.render(tuple_arg, path)
        return {"FINISHED"}


######register
classes = [
    LineRendererPanel,
    OpenReferenceImageOperator,
    SaveLineRenderImageOperator,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
