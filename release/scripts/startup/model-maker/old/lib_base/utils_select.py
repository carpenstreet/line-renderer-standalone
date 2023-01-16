import bpy


def change_active():
    bpy.context.active_object.select_set(False)
    for obj in bpy.context.selected_objects:
        bpy.context.view_layer.objects.active = obj


def deselect_all():
    for obj in bpy.context.selected_objects:
        bpy.context.view_layer.objects.active = obj
        bpy.context.active_object.select_set(False)
