import os
import subprocess
import importlib.util
import sys

python = sys.executable
module_js_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js")
application_root_directory = os.path.dirname(folder_paths.__file__)
application_web_extensions_directory = os.path.join(application_root_directory, "web", "extensions", "ComfyUI_jags_Vectormagic")

shutil.copytree(module_js_directory, application_web_extensions_directory, dirs_exist_ok=True)
# call classes used
from .simple_source_file import SIMPLE_CUSTOM_NODE
try:
    from custom_nodes.ComfyUI_jags_Vectormagic import CC_VERSION
    if CC_VERSION < 1:                                    # specify the minimum version you need as a float
        raise Exception()
except: 
    print("ComfyUI_Jags_VectorMagic 1.0 not found - will try to install - you may need to restart afterwards")
    from .install import installer
    import os
    import folder_paths
    application_root_directory = os.path.dirname(folder_paths.__file__)
    installer(os.path.join(application_root_directory,"custom_nodes"))

# Node Names from the beginning
# Note: Name: Unique to all node classes
# NODE_CLASS_MAPPINGS = { "my unique name" : SimpleCustomNode }
NODE_CLASS_MAPPINGS = {
    "xy_Tiling_KSampler": xy_KSampler
}

#Main titles
# Asymmetric tiling script for ComfyUI
#
# This script allows seamless tiling to be enabled separately for the X and Y axes.

#NODE_DISPLAY_NAME_MAPPINGS = { "my unique name" : "Image inverter" }
NODE_DISPLAY_NAME_MAPPINGS = {
    "xy_Tiling_KSampler": "This script allows seamless tiling to be enabled separately for the X and Y axes."
    
}
CC_VERSION = 1.0


# web ui feature
WEB_DIRECTORY = "./js"

#print confirmation

print('--------------')
print('\ComfyUI_Jags_VectorMagic- nodes_loaded')
print('--------------')
#__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
__ALL__ = [NODE_CLASS_MAPPINGS, CC_VERSION]



