import os
import subprocess
import importlib.util
import sys

python = sys.executable
module_js_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js")
application_root_directory = os.path.dirname(__file__)
application_web_extensions_directory = os.path.join(application_root_directory, "web", "extensions")

#shutil.copytree(module_js_directory, application_web_extensions_directory, dirs_exist_ok=True)
# call classes used
from .base import xy_Tiling_KSampler
from .base import CircularVAEDecode

# Node Names from the beginning
# Note: Name: Unique to all node classes
# NODE_CLASS_MAPPINGS = { "my unique name" : SimpleCustomNode }
NODE_CLASS_MAPPINGS = {
    "xy_Tiling_KSampler": xy_Tiling_KSampler,
    "CircularVAEDecode": CircularVAEDecode,
}

#Main titles
# Asymmetric tiling script for ComfyUI
#
# This script allows seamless tiling to be enabled separately for the X and Y axes.

#NODE_DISPLAY_NAME_MAPPINGS = { "my unique name" : "Image inverter" }
NODE_DISPLAY_NAME_MAPPINGS = {
    "xy_Tiling_KSampler": "Jags-XY_tile sampler",
    "CircularVAEDecode": "Jags-CircularVAEDecode",
}
CC_VERSION = 1.0


# web ui feature
WEB_DIRECTORY = "js"

#print confirmation

print('--------------')
print('\ComfyUI_Jags_VectorMagic- nodes_loaded')
print('--------------')
#__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
__ALL__ = [NODE_CLASS_MAPPINGS, CC_VERSION]



