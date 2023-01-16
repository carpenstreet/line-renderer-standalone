import bpy
import bmesh
import os
import random
from bmesh.types import BMVert
from mathutils import Vector
from enum import Enum


def parametrize_face(face: bmesh.types.BMFace):
    '''Finds the x vector and y vector of the face plane'''
    origin = face.loops[0].vert.co
    vec_1 = face.loops[-1].vert.co - face.loops[0].vert.co
    vec_2 = face.loops[1].vert.co - face.loops[0].vert.co
    axis = [vec_1, vec_2]

    # find the axis closest to z vector
    y_index = min([0, 1], key=lambda i: axis[i].cross(Vector((0, 0, 1))).length)

    y_vec = axis.pop(y_index)
    x_vec = axis[0]

    return (origin, x_vec, y_vec)


def load_building(building_info: dict):
    '''Loads building from building information dictionary'''
    base = bpy.data.objects[f"Base Object {building_info.get('building_id', 0):03}"]
    building = Building(base, building_info.get("height", 10), building_info.get("extrusion_schem", "A"), building_info.get("extrusion_paramter", {}), building_info.get("facade_def", {}), building_exists=True)
    return building


class Building:
    window_col_name = "ModelMakerWindows"
    door_col_name = "ModelMakerDoors"
    material_col_name = "ModelMakerMaterials"

    # TODO: better way to store fbx files...?
    all_window_names = [fname.split(".fbx")[0] for fname in os.listdir(f"{os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]}/ModelMakerAsset/FBX/Window")]
    all_door_names = [fname.split(".fbx")[0] for fname in os.listdir(f"{os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]}/ModelMakerAsset/FBX/Door")]
    all_material_collections = [fname.split(".fbx")[0] for fname in os.listdir(f"{os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]}/ModelMakerAsset/FBX/Material")]

    def __init__(self, base: bpy.types.Object, height: float, extrusion_scheme: Enum, extrusion_parameter: dict, facade_def: dict={}, building_exists: bool=False) -> None:
        self.data = None
        self.collection: bpy.types.Collection = bpy.data.collections[f"Building Collection {base['BuildingId']:03}"]
        self.base: bpy.types.Object = base
        self.height: float = height
        self.extrusion_scheme: Enum = extrusion_scheme
        self.extrusion_parameter = extrusion_parameter
        self.facade_def = facade_def

        # possible window names pool
        self.window_names = ["Window_1m_001"]
        # possible door names pool
        self.door_names = ["Door_001"]
        # materials pool
        self.material_collection = "Material_Collection"

        # opening interval
        self.x_interval = 4
        self.y_interval = 3

        # opening offset from facade face
        self.offset = 0.05

        # make building object
        if not building_exists:
            extrusion_map = {
                "Box": self.__extrude_box,
                "Piloti": self.__extrude_piloti,
                "Bevel": self.__extrude_bevel,
                "Parapet": self.__extrude_parapet
            }
            self.building = extrusion_map[self.extrusion_scheme](self.extrusion_parameter)
        else:
            self.building = bpy.data.objects[f"Building Object {base['BuildingId']:03}"]

        self.set_facade(facade_def)


    def dumps(self) -> dict:
        info = {
            "building_id": self.base["BuildingId"],
            "height": self.height,
            "extrusion_scheme": self.extrusion_scheme,
            "extrusion_parameter": self.extrusion_parameter,
            "facade_definition": {
                "window_names": self.window_names,
                "door_names": self.door_names,
                "material_colleciton": self.material_collection
            }
        }
        return info


    def set_facade(self, facade_def: dict = {}) -> None:
        # clean up current facade
        for child_col in self.collection.children:
            child_col: bpy.types.Collection
            for obj in child_col.objects:
                child_col.objects.unlink(obj)

        # set facade
        self.window_names = facade_def.get("window_names", Building.all_window_names)
        self.door_names = facade_def.get("door_names", Building.all_door_names)
        self.material_collection = facade_def.get("material_collection", Building.all_material_collections[0])

        self.__import_window()
        self.__import_door()
        self.__import_material()
        self.__update_facade()


    def __import_window(self) -> None:
        if self.window_col_name not in bpy.data.collections:
            bpy.data.collections.new(self.window_col_name)

        window_col = bpy.data.collections[self.window_col_name]

        for name in self.window_names:
            window_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]+f"/ModelMakerAsset/FBX/Window/{name}.fbx"
            bpy.ops.import_scene.fbx(filepath=window_path)

            for obj in bpy.context.selected_objects:
                if obj.name in bpy.context.scene.collection.objects:
                    bpy.context.scene.collection.objects.unlink(obj)
                else:
                    for c in bpy.data.collections:
                        if obj.name in c.objects:
                            c.objects.unlink(obj)
                window_col.objects.link(obj)


    def __import_door(self) -> None:
        if self.door_col_name not in bpy.data.collections:
            bpy.data.collections.new(self.door_col_name)

        door_col = bpy.data.collections[self.door_col_name]

        for name in self.door_names:
            door_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]+f"/ModelMakerAsset/FBX/Door/{name}.fbx"
            bpy.ops.import_scene.fbx(filepath=door_path)

            for obj in bpy.context.selected_objects:
                if obj.name in bpy.context.scene.collection.objects:
                    bpy.context.scene.collection.objects.unlink(obj)
                else:
                    for c in bpy.data.collections:
                        if obj.name in c.objects:
                            c.objects.unlink(obj)
                door_col.objects.link(obj)


    def __import_material(self) -> None:
        if self.material_col_name not in bpy.data.collections:
            bpy.data.collections.new(self.material_col_name)

        material_col = bpy.data.collections[self.material_col_name]

        material_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]+f"/ModelMakerAsset/FBX/Material/{self.material_collection}.fbx"
        bpy.ops.import_scene.fbx(filepath=material_path)

        for obj in bpy.context.selected_objects:
            if obj.name in bpy.context.scene.collection.objects:
                bpy.context.scene.collection.objects.unlink(obj)
            else:
                for c in bpy.data.collections:
                    if obj.name in c.objects:
                        c.objects.unlink(obj)
            material_col.objects.link(obj)


    def __link_obj(self, obj: bpy.types.Object, obj_type:str) -> None:
        col_name = f"{obj_type.capitalize()} Collection {self.base['BuildingId']:03}"

        # make new child collection if it doesn't exist
        if col_name not in self.collection.children:
            self.collection.children.link(bpy.data.collections.new(col_name))

        self.collection.children[col_name].objects.link(obj)


    @staticmethod
    def is_roof(f: bmesh.types.BMFace) -> bool:
        return abs(abs(f.normal.dot(Vector([0,0,1]))) - 1) < 0.1


    def __extrude_base(self, building, start_height, end_height) -> None:
        base = self.base

        self.collection.objects.unlink(base)
        self.collection.objects.link(building)

        # set base to active
        bpy.context.view_layer.objects.active = building
        bm = bmesh.new()

        bm.from_mesh(building.data)

        bm.edges.ensure_lookup_table()
        edges_to_remove = []

        for i in range(len(bm.edges)):
            e = bm.edges[i]
            if not e.is_boundary:
                edges_to_remove.append(e)

        for e in edges_to_remove:
            bm.edges.remove(e)
            bm.edges.ensure_lookup_table()

        # Get geometry to extrude
        bm.faces.ensure_lookup_table()

        # Extrude
        bmesh.ops.translate(bm, vec=Vector((0, 0, end_height)), verts = bm.verts)
        extruded = bmesh.ops.extrude_edge_only(bm, edges=bm.edges)

        # Move extruded geometry
        translate_verts = [v for v in extruded['geom'] if isinstance(v, BMVert)]

        bmesh.ops.translate(bm, vec=Vector((0, 0, start_height-end_height)), verts=translate_verts)

        bmesh.ops.delete(bm, geom=bm.edges)

        # Remove doubles
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)

        # Update mesh and free Bmesh
        bm.normal_update()
        bm.to_mesh(building.data)
        bm.free()


    # box
    def __extrude_box(self, extrusion_parameter) -> bpy.types.Object:
        # make mesh from base and height
        base = self.base

        building = bpy.data.objects.new(f"Building Object {base['BuildingId']:03}", base.data)

        building["ModelMakerType"] = "building"
        building["BuildingId"] = base["BuildingId"]

        self.__extrude_base(building, 0, self.height)

        return building


    # piloti
    def __extrude_piloti(self, extrusion_parameter) -> bpy.types.Object:
        # parameters
        height = self.height
        piloti_height = extrusion_parameter["piloti_height"]

        # make mesh from base and height
        base = self.base

        building = bpy.data.objects.new(f"Building Object {base['BuildingId']:03}", base.data)

        building["ModelMakerType"] = "building"
        building["BuildingId"] = base["BuildingId"]

        piloti_height = extrusion_parameter["piloti_height"]
        self.__extrude_base(building, piloti_height, height)

        # Make Piloti
        bpy.ops.object.editmode_toggle()
        building = bpy.context.object
        bm = bmesh.from_edit_mesh(building.data)

        bpy.ops.mesh.select_mode(type="FACE")
        bm.faces.ensure_lookup_table()

        # Select roof
        for face in bm.faces:
            if self.is_roof(face):
                face.select_set(True)
            else:
                face.select_set(False)
        building.data.update()

        # Copy roof to bottom
        bpy.ops.mesh.duplicate()
        bpy.ops.mesh.separate(type="SELECTED")
        bottom = bpy.context.selected_objects[0]
        bpy.ops.object.editmode_toggle()
        bpy.context.view_layer.objects.active = bottom
        bpy.ops.transform.translate(value=(0, 0, piloti_height-height))

        # Inset
        bpy.ops.object.editmode_toggle()
        bottommesh = bmesh.from_edit_mesh(bottom.data)
        for face in bottommesh.faces:
            face.select_set(True)
        bottom.data.update()

        bpy.ops.mesh.inset(thickness=1)
        bpy.ops.mesh.separate(type="SELECTED")
        bpy.ops.object.editmode_toggle()


        # Make cylindrical columns
        bottom.select_set(False)
        pilotibase = bpy.context.selected_objects[0]
        bpy.context.view_layer.objects.active = pilotibase
        bpy.ops.object.editmode_toggle()
        pilotimesh = bmesh.from_edit_mesh(pilotibase.data)

        piloti_locs = []
        for v in pilotimesh.verts:
            piloti_locs.append((v.co.x, v.co.y, piloti_height/2))
        for loc in piloti_locs:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=piloti_height, location=loc)
        bpy.ops.object.editmode_toggle()

        return building


    # bevel
    def __extrude_bevel(self, extrusion_parameter) -> bpy.types.Object:
        # parameters
        height = self.height
        bevel_depth = extrusion_parameter["bevel_depth"]

        # make mesh from base and height
        base = self.base

        building = bpy.data.objects.new(f"Building Object {base['BuildingId']:03}", base.data)

        building["ModelMakerType"] = "building"
        building["BuildingId"] = base["BuildingId"]

        self.__extrude_base(building, 0, height)


        # Bevel roof
        bpy.ops.object.editmode_toggle()
        building = bpy.context.object
        bm = bmesh.from_edit_mesh(building.data)
        if building.mode == "EDIT":
            bpy.ops.mesh.select_mode(type="FACE")
            bm.faces.ensure_lookup_table()
            for face in bm.faces:
                if self.is_roof(face):
                    face.select_set(True)
                else:
                    face.select_set(False)
            building.data.update()
            bpy.ops.mesh.bevel(offset=bevel_depth)
        bpy.ops.object.editmode_toggle()

        return building


    # parapet
    def __extrude_parapet(self, extrusion_parameter) -> bpy.types.Object:
        # parameters
        height = self.height
        parapet_depth = extrusion_parameter["parapet_depth"]
        parapet_height = extrusion_parameter["parapet_height"]

        # make mesh from base and height
        base = self.base

        building = bpy.data.objects.new(f"Building Object {base['BuildingId']:03}", base.data)

        building["ModelMakerType"] = "building"
        building["BuildingId"] = base["BuildingId"]

        self.__extrude_base(building, 0, height)

        # Make parapet on roof
        bpy.ops.object.editmode_toggle()
        building = bpy.context.object
        bm = bmesh.from_edit_mesh(building.data)

        bpy.ops.mesh.select_mode(type="FACE")
        bm.faces.ensure_lookup_table()
        for face in bm.faces:
            if self.is_roof(face):
                face.select_set(True)
            else:
                face.select_set(False)
        building.data.update()
        bpy.ops.mesh.inset(thickness=parapet_depth)
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":Vector((0, 0, -parapet_height))})
        bpy.ops.object.editmode_toggle()
        building.data.update()

        return building


    def __update_facade(self):

        # magic_uv addon을 켜줌
        bpy.ops.preferences.addon_enable(module="magic_uv")

        # get building object
        building: bpy.types.Object = self.building

        # set building to active
        bpy.context.view_layer.objects.active = building

        # append materials to building object
        lst_material_wall = []
        lst_material_roof = []
        for i in bpy.data.materials:
            if (i.name).startswith("Wall"):
                lst_material_wall.append(i.name)
            elif (i.name).startswith("Roof"):
                lst_material_roof.append(i.name)
        material_wall = random.choice(lst_material_wall)
        material_roof = random.choice(lst_material_roof)

        # material index - 0: roof, 1: facade
        building.data.materials.clear()
        building.data.materials.append(bpy.data.materials[material_roof])
        building.data.materials.append(bpy.data.materials[material_wall])

        # apply box mapping using magic uv
        bpy.ops.object.editmode_toggle()
        bm_uv = bmesh.from_edit_mesh(building.data)

        bm_uv.faces.ensure_lookup_table()

        if building.mode == "EDIT":
            bpy.ops.mesh.select_mode(type="FACE")
            for f in bm_uv.faces:
                if self.is_roof(f):
                    f.material_index = 0
                else:
                    f.material_index = 1
                f.select_set(True)

        bpy.ops.uv.muv_uvw_box_map(assign_uvmap=True)
        bpy.ops.object.editmode_toggle()


        # new mesh for openings
        bm = bmesh.new()
        bm.from_mesh(building.data)

        facade_faces = []
        roof_faces = []

        flip_normal = False

        # find roof
        for f in bm.faces:
            if self.is_roof(f):
                # check and set flip_normal
                if f.normal[2] < 0:
                    flip_normal = True
                    f.normal_flip()
                roof_faces.append(f)
            else:
                facade_faces.append(f)

        for f in facade_faces:
            f: bmesh.types.BMFace

            # check normal
            if flip_normal:
                f.normal_flip()

            n = f.normal
            origin, x_vec, y_vec = parametrize_face(f)

            x_count = int(x_vec.length//self.x_interval)
            y_count = int(y_vec.length//self.y_interval)

            if x_count > 0 and y_count > 0:
                parameters = [[((i+1)/(x_count+1), (j+1)/(y_count+1)) for i in range(x_count)] for j in range(y_count)]

                facade_openings = [["window" for i in range(x_count)] for j in range(y_count)]

                if self.extrusion_scheme != "Piloti":
                    # randomly assign door
                    facade_openings[-1][random.choice(range(x_count))] = "door"

                locs = [[origin + floor_param[0]*x_vec + floor_param[1]*y_vec for floor_param in floor] for floor in parameters]
                for row_objs, row_locs in zip(facade_openings, locs):
                    for obj_type, loc in zip(row_objs, row_locs):
                        if obj_type == "window":
                            new_obj = bpy.data.objects.new("facade_window", bpy.data.objects[random.choice(self.window_names)].data)
                        elif obj_type == "door":
                            new_obj = bpy.data.objects.new("facade_door", bpy.data.objects[random.choice(self.door_names)].data)
                        else:
                            continue
                        new_obj.location = loc
                        new_obj.rotation_mode = "QUATERNION"
                        new_obj.rotation_quaternion = n.to_track_quat("Y", "Z")
                        new_obj.delta_location = n * self.offset
                        if obj_type == "door":
                            new_obj.location = [new_obj.location[0], new_obj.location[1], 0]

                        # add new obj in appropriate children collection of building collection
                        self.__link_obj(new_obj, obj_type)

        bm.normal_update()
        bm.to_mesh(building.data)
        bm.free()
