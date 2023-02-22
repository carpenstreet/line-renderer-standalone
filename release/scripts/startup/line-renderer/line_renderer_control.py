import os
import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper
from .render_lib import line_render
from .line_lib import line_render_lib


def draw_section(layout, text):
    result = layout.row()
    result.label(text=text)
    result = layout.row()
    return result


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

        row = draw_section(layout, "Line Render")
        row.operator("wm.open_reference_image")


class OpenReferenceImageOperator(bpy.types.Operator, ImportHelper):
    """Open line render reference image"""

    bl_idname = "wm.open_reference_image"
    bl_label = "Open and Generate Image"
    bl_options = {"REGISTER", "UNDO"}

    image_extension = "*.png;*.jpg;*psd"
    index: bpy.props.IntProperty(name="Index", default=0, options={"HIDDEN"})
    filter_glob: bpy.props.StringProperty(default=image_extension, options={"HIDDEN"})

    def execute(self, context):
        dirname = os.path.dirname(self.filepath)
        for file in os.listdir(dirname):
            if file.endswith(".png"):
                result = line_render_lib.usage(os.path.join(dirname, file))
                save_result = line_render.render(result[0], os.path.join(dirname, file))
                if save_result is None:
                    print(f"Error occured for {file}")
        self.report({'INFO'}, f"Saved to {os.path.dirname(save_result)}")
        return {"FINISHED"}


# register
classes = [
    LineRendererPanel,
    OpenReferenceImageOperator,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
