from typing import Optional

import bpy
import os


def render(dict_arg, path) -> Optional[str]:
    try:
        # LineRender 이미지를 추출
        width = dict_arg["width"]
        dynamics = dict_arg["dynamics"]
        jitter = dict_arg["jitter"]

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
        
        dirname = os.path.join(os.path.dirname(path), "generated")
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        basename = os.path.basename(path)
        filename = f"{os.path.splitext(basename)[0]}-w{str(width)}d{str(dynamics)}j{str(jitter)}.png"
        bpy.data.images[0].save_render(os.path.join(dirname, filename))
        return os.path.join(dirname, filename)
    except Exception as e:
        print(e)
        return None
