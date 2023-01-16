
## Architecture ##

#### [load_building(building_info: dict)](https://github.com/ACON3D/Model-Maker-Blender/blob/915965b12613d13e85b5762f20bbcb3a3f0a1e36/architecture/building.py#L26-L30) -> Building

    building_info: 빌딩을 구성할 수 있는 dictionary 형태의 정보

    returns: Building 객체

### *class* Building(base: bpy.types.Object, height: float, extrusion_scheme: Enum, extrusion_parameter: dict, facade_def: dict = {}, building_exists: bool = False)
    '''정해진 extrusion scheme과 base로 빌딩을 만들고 빌딩의 정보를 업데이트 한다.'''

    base: 빌딩의 베이스가 되는 bpy Object
    height: 빌딩의 높이
    extrusion_scheme: BuildingMakerOperator에서 정해진 extrusion 방식
    extrusion_parameter: extrusion_scheme에 맞게 건물을 생성하기 위해 필요한 변수들
    facade_def: 건물의 파사드 정의
    building_exists: 현재 건물의 블렌더에서 존재 여부

#### Building.[dumps()](https://github.com/ACON3D/Model-Maker-Blender/blob/915965b12613d13e85b5762f20bbcb3a3f0a1e36/architecture/building.py#L81-L93) -> dict

    '''빌딩의 정보를 serializable한 dictionary로 변환한다.'''

    returns: dictionary 형태의 건물 정보

#### Building.[set_facade(facade_def: dict)](https://github.com/ACON3D/Model-Maker-Blender/blob/915965b12613d13e85b5762f20bbcb3a3f0a1e36/architecture/building.py#L96-L111) -> None

    '''facade의 정보 (창문, 문, 텍스쳐의 종류)를 받아서 빌딩에 적용시킨다.'''

    facade_def: window, door, material로 이루어진 dictionary

    returns: None

#### Building.[__import_window()](https://github.com/ACON3D/Model-Maker-Blender/blob/915965b12613d13e85b5762f20bbcb3a3f0a1e36/architecture/building.py#L114-L131) -> None

    '''facade에서 지정된 window fbx 파일을 읽어서 가져온다.'''

    returns: None

#### Building.[__import_door()](https://github.com/ACON3D/Model-Maker-Blender/blob/915965b12613d13e85b5762f20bbcb3a3f0a1e36/architecture/building.py#L134-L151) -> None

    '''facade에서 지정된 door fbx 파일을 읽어서 가져온다.'''

    returns: None

#### Building.[__import_material()](https://github.com/ACON3D/Model-Maker-Blender/blob/915965b12613d13e85b5762f20bbcb3a3f0a1e36/architecture/building.py#L154-L170) -> None

    '''facade에서 지정된 material fbx 파일을 읽어서 가져온다.'''

    returns: None

#### Building.[__extrude_base(building: bpy.types.Object, start_height: float, end_height: float)](https://github.com/ACON3D/Model-Maker-Blender/blob/915965b12613d13e85b5762f20bbcb3a3f0a1e36/architecture/building.py#L187-L231) -> None

    '''base를 start_height에서 end_height까지 extrude 한다.'''

    building: 빌딩의 베이스가 될 bpy Object
    start_height: 건물의 시작 높이
    end_height: 건물의 최종 높이

    returns: None

#### Building.[__extrude_box(extrusion_parameter: dict)](https://github.com/ACON3D/Model-Maker-Blender/blob/915965b12613d13e85b5762f20bbcb3a3f0a1e36/architecture/building.py#L235-L246) -> bpy.types.Object

    '''box extrusion scheme에 맞춰서 빌딩의 모양을 생성한다.'''

    extrusion_parameter: 빌딩을 extrude하기 위해 필요한 변수들

    returns: extrude 된 빌딩 bpy Object 개체

#### Building.[__extrude_piloti(extrusion_parameter: dict)](https://github.com/ACON3D/Model-Maker-Blender/blob/915965b12613d13e85b5762f20bbcb3a3f0a1e36/architecture/building.py#L250-L316) -> bpy.types.Object

    '''piloti extrusion scheme에 맞춰서 빌딩의 모양을 생성한다.'''

    extrusion_parameter: 빌딩을 extrude하기 위해 필요한 변수들

    returns: extrude 된 빌딩 bpy Object 개체

#### Building.[__extrude_bevel(extrusion_parameter: dict)](https://github.com/ACON3D/Model-Maker-Blender/blob/915965b12613d13e85b5762f20bbcb3a3f0a1e36/architecture/building.py#L320-L352) -> bpy.types.Object

    '''bevel extrusion scheme에 맞춰서 빌딩의 모양을 생성한다.'''

    extrusion_parameter: 빌딩을 extrude하기 위해 필요한 변수들

    returns: extrude 된 빌딩 bpy Object 개체

#### Building.[__extrude_parapet(extrusion_parameter: dict)](https://github.com/ACON3D/Model-Maker-Blender/blob/915965b12613d13e85b5762f20bbcb3a3f0a1e36/architecture/building.py#L356-L390) -> bpy.types.Object

    '''parapet extrusion scheme에 맞춰서 빌딩의 모양을 생성한다.'''

    extrusion_parameter: 빌딩을 extrude하기 위해 필요한 변수들

    returns: extrude 된 빌딩 bpy Object 개체

#### Building.[__update_facade()](https://github.com/ACON3D/Model-Maker-Blender/blob/915965b12613d13e85b5762f20bbcb3a3f0a1e36/architecture/building.py#L393-L502) -> None

    '''빌딩의 facade 정보를 업데이트 해준다.'''

    returns: None

## Adding an Extrusion Scheme ##

1. [BuildingMakerOperator](https://github.com/ACON3D/Model-Maker-Blender/blob/915965b12613d13e85b5762f20bbcb3a3f0a1e36/model_maker_control.py#L134-L245) 에 새로운 extrusion scheme Enum과 필요한 property들을 만든다.

2. BuildingMakerOperator의 draw()함수에 extrusion scheme 에 맞는 property를 넣어 패널에서 보여준다.

3. [Buiilding](https://github.com/ACON3D/Model-Maker-Blender/blob/915965b12613d13e85b5762f20bbcb3a3f0a1e36/architecture/building.py#L33) 클래스에서 새로운 extrusion scheme 로직을 추가한다. 네이밍 컨벤션은 __extrude_schemename()으로 한다.

4. Building 클래스의 __init__ 함수에서 [extrusion_map](https://github.com/ACON3D/Model-Maker-Blender/blob/915965b12613d13e85b5762f20bbcb3a3f0a1e36/architecture/building.py#L68-L73)에 추가한 extrusion scheme Enum과 extrusions scheme 함수를 매핑한다.