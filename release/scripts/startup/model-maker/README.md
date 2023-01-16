
# Model Maker #
주어진 베이스와 익스트루젼 방법으로부터 건물 모델을 만듭니다.
![](https://github.com/ACON3D/Model-Maker-Blender/blob/main/img_building_created.png?raw=true)


## ModelMaker Installation ##
1. ModelMaker.zip을 다운로드 합니다.

![](https://github.com/ACON3D/Model-Maker-Blender/blob/main/img_preferences.png?raw=true)

2. Blender를 켜고 Edit - Preference 창을 엽니다.

![](https://github.com/ACON3D/Model-Maker-Blender/blob/main/img_addon_install.png?raw=true)

3. Install 버튼을 누르고 ModelMaker.zip을 선택합니다.


## ModelMaker Panel ##
![](https://github.com/ACON3D/Model-Maker-Blender/blob/main/img_new_base.png?raw=true)

1. New Base
    - New Base 버튼을 누르고 건물 베이스의 각 점을 클릭합니다.
    - 모든 점을 누른 후 Esc 또는 우클릭으로 베이스 생성을 마칩니다.

![](https://github.com/ACON3D/Model-Maker-Blender/blob/main/img_new_building.png?raw=true)

2. New Building From Base
    - 생성한 베이스를 선택한 상태에서 New Building From Base 버튼을 누릅니다.
    - Box, Piloti, Bevel, Parapet 중 하나의 Extrusion Scheme을 선택합니다.
    - 선택한 Extrusion Scheme에 따라 변수를 입력합니다.
        - Box
            Height: 건물의 높이
        - Piloti
            Height: 건물의 높이
            Piloti Height: 1층에서 필로티의 높이
        - Bevel
            Height: 건물의 높이
            Bevel Depth: 지붕이 깎이는 깊이
        - Parapet
            Height: 건물의 높이
            Parapet Height: 지붕에서 파라펫의 높이
            Parapet Depth: 지붕에서 파라펫의 깊이
    - 변수 입력 후 OK 버튼을 눌러 새 건물 모델을 생성합니다.

![](https://github.com/ACON3D/Model-Maker-Blender/blob/main/img_choose_window.png?raw=true)

3. Choose Window
    - 생성된 건물 모델을 선택한 상태에서 Choose Window 버튼을 눌러 창문의 종류를 바꿀 수 있습니다.
    - Model-Maker-Blender 애드온의 설치 경로에서 ModelMakerAsset/FBX/Window 폴더 안이 .fbx 파일 중 하나를 선택합니다.
    - Choose Window 버튼을 누르면 건물 모델의 창문이 위에 선택한 모델로 바뀝니다.

![](https://github.com/ACON3D/Model-Maker-Blender/blob/main/img_choose_door.png?raw=true)

4. Choose Door
    - 생성된 건물 모델을 선택한 상태에서 Choose Door 버튼을 눌러 문의 종류를 바꿀 수 있습니다.
    - Model-Maker-Blender 애드온의 설치 경로에서 ModelMakerAsset/FBX/Door 폴더 안이 .fbx 파일 중 하나를 선택합니다.
    - Choose Door 버튼을 누르면 건물 모델의 문이 위에 선택한 모델로 바뀝니다.
