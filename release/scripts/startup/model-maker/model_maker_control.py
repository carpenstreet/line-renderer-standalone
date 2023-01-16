import bpy
import bmesh
import os
from bpy_extras.io_utils import ImportHelper
from bpy_extras.view3d_utils import region_2d_to_vector_3d, region_2d_to_location_3d
from .architecture.building import Building, load_building


class ModelMakerPanel(bpy.types.Panel):
    bl_label = "ModelMaker Panel"
    bl_idname = "DH_PT_model_maker_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ModelMaker"

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="FILE_3D")

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Model Maker")
        row = layout.row()
        row.operator(BaseMakerOperator.bl_idname)
        row = layout.row()
        row.operator(BuildingMakerOperator.bl_idname)

        row = layout.row()
        row.label(text="Change Asset")
        row = layout.row()
        row.operator(WindowChooserOperator.bl_idname)
        row = layout.row()
        row.operator(DoorChooserOperator.bl_idname)

        row = layout.row()
        row.label(text="Export")
        row = layout.row()
        row.operator("wm.save_as_mainfile", text="Save Blend")
        row = layout.row()
        row.operator("export_scene.fbx", text="Save FBX")


class BaseMakerOperator(bpy.types.Operator):
    bl_idname = "wm.base_maker_operator"
    bl_label = "New Base"

    base_num = 0
    drawing = False

    @property
    def ob_name(cls):
        return f"Base Object {BaseMakerOperator.base_num:03}"

    def __get_collection(self):
        collection_name = f"Building Collection {BaseMakerOperator.base_num:03}"
        mm_col = bpy.data.collections.get(collection_name)
        if not mm_col:
            bpy.data.collections.new(collection_name)
            bpy.context.scene.collection.children.link(
                bpy.data.collections[collection_name]
            )
        return bpy.data.collections[collection_name]

    def __get_base(self):
        ob_name = self.ob_name

        if not self.drawing:
            mesh_name = f"Base Mesh {BaseMakerOperator.base_num:03}"

            base_mesh = bpy.data.meshes.new(mesh_name)
            base_obj = bpy.data.objects.new(ob_name, base_mesh)

            # give base ModelMakerType property of "base"
            base_obj["ModelMakerType"] = "base"
            base_obj["BuildingId"] = int(self.base_num)
            self.__get_collection().objects.link(base_obj)

        return bpy.data.objects[ob_name]

    def modal(self, context, event):
        if event.type in {"RIGHTMOUSE", "ESC"}:
            # right click or esc finishes drawing mesh
            self.execute(context)
            return {"FINISHED"}

        if event.type == "LEFTMOUSE" and event.value == "PRESS":
            # left click adds a point to base mesh

            if context.area.type == "VIEW_3D":
                # get base
                base = self.__get_base()

                # set top down view

                # get new vertex location
                region = context.region
                r3d = context.space_data.region_3d
                x, y = event.mouse_region_x, event.mouse_region_y
                view = region_2d_to_vector_3d(region, r3d, (x, y))
                loc = region_2d_to_location_3d(region, r3d, (x, y), view)
                loc.z = 0

                # set base to active
                bpy.context.view_layer.objects.active = base

                # add new vertex to base mesh
                bm = bmesh.new()
                bm.from_mesh(base.data)
                bm_verts = bm.verts
                bm_verts.new(loc)
                new_base = bmesh.ops.contextual_create(bm, geom=bm_verts)["faces"]

                bm.faces.ensure_lookup_table()
                for f in bm.faces:
                    if f not in new_base:
                        bm.faces.remove(f)

                bm.normal_update()
                bm.to_mesh(base.data)
                bm.free()

                # start drawing
                self.drawing = True

        return {"PASS_THROUGH"}

    def invoke(self, context, event):
        if context.area.type != "VIEW_3D":
            print("Must use in a 3d region")
            return {"CANCELLED"}

        # Top View 전환
        for area in context.screen.areas:
            if area.type == "VIEW_3D":
                override = bpy.context.copy()
                override["area"] = area
                bpy.ops.view3d.view_axis(override, type="TOP")
                break

        wm = context.window_manager
        wm.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        # finish drawing
        BaseMakerOperator.drawing = False
        BaseMakerOperator.base_num += 1

        return {"FINISHED"}


class BuildingMakerOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "wm.building_maker_operator"
    bl_label = "New Building From Base"

    # Extrusion Scheme
    extrusion_scheme: bpy.props.EnumProperty(
        items=[
            ("Box", "Box", "Box", "Box", 0),
            ("Piloti", "Piloti", "Piloti", "Piloti", 1),
            ("Bevel", "Bevel", "Bevel", "Bevel", 2),
            ("Parapet", "Parapet", "Parapet", "Parapet", 3),
        ],
        default="Box",
    )

    # Common Extrusion Scheme Parameter
    height: bpy.props.FloatProperty(
        name="Height",
        description="Height of Building",
        default=10,
        min=0,
        max=100,
        precision=2,
    )

    # Piloti Extrusion Scheme Parameter
    piloti_height: bpy.props.FloatProperty(
        name="Piloti Height",
        description="Height of Piloti",
        default=3,
        min=0,
        max=10,
        precision=2,
    )

    # Bevel Extrusion Scheme Parameter
    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth",
        description="Depth of Bevel",
        default=1,
        min=0,
        max=10,
        precision=2,
    )

    # Parapet Extrusion Scheme Parameter
    parapet_height: bpy.props.FloatProperty(
        name="Parapet Height",
        description="Height of Parapet",
        default=1,
        min=0,
        max=10,
        precision=2,
    )

    # Parapet Extrusion Scheme Parameter
    parapet_depth: bpy.props.FloatProperty(
        name="Parapet Depth",
        description="Depth of Parapet",
        default=1,
        min=0,
        max=10,
        precision=2,
    )

    def __init__(self):
        self.base = None

    def __make_building(self):
        # TODO: facade definition?
        extrusion_parameter = {
            "piloti_height": self.piloti_height,
            "bevel_depth": self.bevel_depth,
            "parapet_height": self.parapet_height,
            "parapet_depth": self.parapet_depth,
        }
        building = Building(
            self.base, self.height, self.extrusion_scheme, extrusion_parameter, {}
        )
        building_info = building.dumps()
        building.building["info"] = building_info
        print(building_info)
        return building

    @classmethod
    def poll(self, context):
        if len(context.selected_objects) > 0:
            if "ModelMakerType" in context.selected_objects[0]:
                return context.selected_objects[0]["ModelMakerType"] == "base"
        return False

    def invoke(self, context, event):
        self.base = context.selected_objects[0]
        return context.window_manager.invoke_props_dialog(self, width=300)

    def execute(self, context):
        building = self.__make_building()
        self.report({"INFO"}, f"height is {self.height}")
        self.report({"INFO"}, str(building))

        # camera 시점 뷰로 전환
        bpy.ops.object.select_by_type(extend=False, type="CAMERA")
        context.view_layer.objects.active = context.selected_objects[0]
        bpy.ops.view3d.object_as_camera()

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "extrusion_scheme", expand=True)
        layout.prop(self, "height")
        if self.extrusion_scheme == "Piloti":
            layout.prop(self, "piloti_height")
        elif self.extrusion_scheme == "Bevel":
            layout.prop(self, "bevel_depth")
        elif self.extrusion_scheme == "Parapet":
            layout.prop(self, "parapet_height"),
            layout.prop(self, "parapet_depth")


class WindowChooserOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "wm.window_chooser_operator"
    bl_label = "Choose Window"

    @classmethod
    def poll(self, context):
        if len(context.selected_objects) > 0:
            if "ModelMakerType" in context.selected_objects[0]:
                return context.selected_objects[0]["ModelMakerType"] == "building"
        return False

    def invoke(self, context, event):
        path_abler = bpy.utils.preset_paths("assets")[0]
        self.filepath = path_abler + "/Window/"
        wm = context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        building_obj = context.selected_objects[0]
        building_info = building_obj["info"]
        building = load_building(building_obj["info"])
        fdir = self.properties.filepath

        window_name = os.path.split(fdir)[1].split(".fbx")[0]
        cur_facade = building_info.get("facade_definition", {})
        cur_facade.update({"window_names": [window_name]})
        building.set_facade(cur_facade)
        return {"FINISHED"}


class DoorChooserOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "wm.door_chooser_operator"
    bl_label = "Choose Door"

    @classmethod
    def poll(self, context):
        if len(context.selected_objects) > 0:
            if "ModelMakerType" in context.selected_objects[0]:
                return context.selected_objects[0]["ModelMakerType"] == "building"
        return False

    def invoke(self, context, event):
        path_abler = bpy.utils.preset_paths("assets")[0]
        self.filepath = path_abler + "/Door/"
        wm = context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        building_obj = context.selected_objects[0]
        building_info = building_obj["info"]
        building = load_building(building_obj["info"])
        fdir = self.properties.filepath

        door_name = os.path.split(fdir)[1].split(".fbx")[0]
        cur_facade = building_info.get("facade_definition", {})
        cur_facade.update({"door_names": [door_name]})
        building.set_facade(cur_facade)
        return {"FINISHED"}


######register
classes = [
    ModelMakerPanel,
    BaseMakerOperator,
    BuildingMakerOperator,
    WindowChooserOperator,
    DoorChooserOperator,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
