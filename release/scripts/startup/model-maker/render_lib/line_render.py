import bpy
import os


def render(tuple_arg, path):
    # LineRender 이미지를 추출

    (width, dynamics, jitter) = tuple_arg

    if dynamics > 1:
        dynamics = 1
    elif dynamics < 0:
        dynamics = 0

    if jitter > 1:
        jitter = 1
    elif jitter < 0:
        jitter = 0

    min_width = width * (1 - dynamics)
    max_width = width

    bpy.data.linestyles["LineStyle"].thickness_modifiers["Along Stroke"].value_min = min_width
    bpy.data.linestyles["LineStyle"].thickness_modifiers["Along Stroke"].value_max = max_width
    bpy.data.linestyles["LineStyle"].thickness_modifiers["Noise"].amplitude = jitter

    bpy.ops.render.render(use_viewport=True)

    dirname = os.path.dirname(path)
    filename = f"w{str(width)}d{str(dynamics)}j{str(jitter)}.png"
    bpy.data.images[0].save_render(os.path.join(dirname, filename))
