import bpy

from .operator_modelmaker import operator_modelmaker


class ACON3DModelMakerPanel_PT_panel(bpy.types.Panel):
    bl_label = "ModelMaker Panel"
    bl_idname = "ACON3D_PT_model_maker_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Acon3d_Track1"

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="FILE_3D")

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Modelmaker")
        row = layout.row()
        row.operator(ACON3DModelMakerOperator_OT_oneroom.bl_idname)
        row = layout.row()
        row.operator(ACON3DModelMakerOperator_OT_oneroom_pillar.bl_idname)
        row = layout.row()
        row.operator(ACON3DModelMakerOperator_OT_oneroom_store.bl_idname)


class ACON3DModelMakerOperator_OT_oneroom(bpy.types.Operator):
    bl_idname = "oneroom.model_maker"
    bl_label = "OneRoom"

    Nodes_name = "OneRoom_Nodes1"
    lst_setting = ["Window", "Door"]  # lst_setting 첫번째는 무조건 Window!
    lst_obj = ["Roof_Entrance"]  # TODO: "Window_Stair","Vent"
    lst_collection = [
        "Material",
        "Roof_Deco",
        "Balcony",
        "OutdoorUnit_Wall",
        "OutdoorUnit_Window",
        "Sticker",
        "Waterline",
        "Roof_Handrail",
    ]  # TODO:

    @classmethod
    def poll(self, context):
        return len(context.selected_objects)

    def execute(self, context):
        operator_modelmaker(self)
        return {"FINISHED"}


class ACON3DModelMakerOperator_OT_oneroom_pillar(bpy.types.Operator):
    bl_idname = "oneroom_pillar.model_maker"
    bl_label = "OneRoom_Pillar"

    Nodes_name = "OneRoom_Nodes2"
    lst_setting = ["Window"]  # lst_setting 첫번째는 무조건 Window!
    lst_obj = ["EnterDoor", "ParkingLine", "ParkingBlock", "Roof_Entrance"]  # "Vent"
    lst_collection = [
        "Material",
        "Roof_Deco",
        "Balcony",
        "OutdoorUnit_Wall",
        "OutdoorUnit_Window",
        "Sticker",
        "Waterline",
        "Roof_Handrail",
    ]

    @classmethod
    def poll(self, context):
        return len(context.selected_objects)

    def execute(self, context):
        operator_modelmaker(self)
        return {"FINISHED"}


class ACON3DModelMakerOperator_OT_oneroom_store(bpy.types.Operator):
    bl_idname = "oneroom_store.model_maker"
    bl_label = "OneRoom_Store"

    Nodes_name = "OneRoom_Nodes3"
    lst_setting = ["Window", "Door"]  # lst_setting 첫번째는 무조건 Window!
    lst_obj = ["Roof_Entrance"]  # "Vent"
    lst_collection = [
        "Material",
        "Roof_Deco",
        "Balcony",
        "OutdoorUnit_Wall",
        "OutdoorUnit_Window",
        "Sticker",
        "Waterline",
        "Roof_Handrail",
    ]  # TODO: "Signboard_Width","Signboard_Height"

    @classmethod
    def poll(self, context):
        return len(context.selected_objects)

    def execute(self, context):
        operator_modelmaker(self)
        return {"FINISHED"}


######register
classes = [
    ACON3DModelMakerPanel_PT_panel,
    ACON3DModelMakerOperator_OT_oneroom,
    ACON3DModelMakerOperator_OT_oneroom_pillar,
    ACON3DModelMakerOperator_OT_oneroom_store,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
