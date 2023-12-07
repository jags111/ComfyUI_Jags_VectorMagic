# only import if running as a custom node
"""
@author: jags111
@title: Jags_VectorMagic
@nickname: Jags_VectorMagic
@description: This extension offers various vector manipulation and  generation tools
"""
import sys, os, shutil
import importlib
import traceback
import json

import folder_paths

custom_nodes_path = os.path.join(folder_paths.base_path, "custom_nodes")
ComfyUI_Jags_VectorMagic_path = os.path.join(custom_nodes_path, "ComfyUI_Jags_VectorMagic")
sys.path.append(ComfyUI_Jags_VectorMagic_path)

#shutil.copytree(module_js_directory, application_web_extensions_directory, dirs_exist_ok=True)
# call classes used
from .base import *
from .yolo_seg import *
from .SVG_convert import *


# Node Names from the beginning
# Note: Name: Unique to all node classes
# NODE_CLASS_MAPPINGS = { "my unique name" : SimpleCustomNode }
NODE_CLASS_MAPPINGS = {
    "xy_Tiling_KSampler": xy_Tiling_KSampler,
    "CircularVAEDecode": CircularVAEDecode,
    "YoloSEGdetectionNode": YoloSEGdetectionNode,
    "YoloSegNode": YoloSegNode,
    "color_drop": color_drop,
    #"SVG": SVG,

}

#Main titles

NODE_DISPLAY_NAME_MAPPINGS = {
    "xy_Tiling_KSampler": "Jags-XY_tile sampler",
    "CircularVAEDecode": "Jags-CircularVAEDecode",
    "YoloSEGdetectionNode": 'Jags-YoloSEGdetectionNode',
    "YoloSegNode": 'Jags-YoloSegNode',
    "color_drop": "Jags-color_drop",
    #"SVG": "Jags-SVG",
}
CC_VERSION = 1.0

THIS_DIR=os.path.dirname(os.path.abspath(__file__))
DIR_DEV_JS=os.path.abspath(f'{THIS_DIR}/js')
DIR_PY=os.path.abspath(f'{THIS_DIR}/py')
DIR_WEB_JS=os.path.abspath(f'{THIS_DIR}/../../web/extensions/comfyui_jags_Vectormagic')
if not os.path.exists(DIR_WEB_JS):
    os.makedirs(DIR_WEB_JS)

shutil.copytree(DIR_DEV_JS, DIR_WEB_JS, dirs_exist_ok=True)

# web ui feature
WEB_DIRECTORY = "js"

#print confirmation

print('--------------')
print('*ComfyUI_Jags_VectorMagic- nodes_loaded*')
print('--------------')
#__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
__ALL__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'CC_VERSION']



