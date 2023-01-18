import bpy


def render(width, dynamics, jitter):
    # LineRender 이미지를 추출
    
    if dynamics > 1: dynamcis = 1
    elif dynamics < 0: dynamics = 0
    
    if jitter > 1: jitter = 1
    elif jitter < 0: jitter = 0
        
    min_width = width * (1 - dynamics)
    max_width = width
    
    bpy.data.linestyles["LineStyle"].thickness_modifiers["Along Stroke"].value_min = min_width
    bpy.data.linestyles["LineStyle"].thickness_modifiers["Along Stroke"].value_max = max_width
    bpy.data.linestyles["LineStyle"].thickness_modifiers["Noise"].amplitude = jitter
    
    bpy.ops.render.render(use_viewport=True)
    
    filename = "w" + str(width) + "d" + str(dynamics) + "j" + str(jitter) + ".png"
    
    # <PATH>: 렌더 결과 이미지들을 저장하려는 위치의 경로
    # bpy.data.images[0].save_render(<PATH> + filename)


## 이미지 추가를 위한 예시
# def fillList(list, value=0, step=0.1, maxValue=1):

#     if value > maxValue: return

#     list.append(value)
#     return fillList(list, value + step, step, maxValue)


# widthList = []
# dynamicsList = []
# jitterList = []

# # 이미지를 1000장 만드려면 다음 코드를 이용해주세요.
# #fillList(widthList, 1, 0.5, 6)
# #fillList(dynamicsList)
# #fillList(jitterList)

# # 이미지를 8장만 만드려면 다음 코드를 이용해주세요.
# fillList(widthList, 1, 3, 6)
# fillList(dynamicsList, 0, 0.6)
# fillList(jitterList, 0, 0.6)

# for width in widthList:
#     for dynamics in dynamicsList:
#         for jitter in jitterList:
#             render(width, dynamics, jitter)