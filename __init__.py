import os, shutil
import folder_paths

module_js_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js")
application_root_directory = os.path.dirname(folder_paths.__file__)
application_web_extensions_directory = os.path.join(application_root_directory, "web", "extensions", "ComfyUI_jags_Vectormagic")

shutil.copytree(module_js_directory, application_web_extensions_directory, dirs_exist_ok=True)

from .simple_source_file import SIMPLE_CUSTOM_NODE
try:
    from custom_nodes.ComfyUI_jags_Vectormagic import CC_VERSION
    if CC_VERSION < 1:                                    # specify the minimum version you need as a float
        raise Exception()
except: 
    print("ComfyUI_jags_Vectormagic 1.0 not found - will try to install - you may need to restart afterwards")
    from .install import installer
    import os
    import folder_paths
    application_root_directory = os.path.dirname(folder_paths.__file__)
    installer(os.path.join(application_root_directory,"custom_nodes"))

# NODE_CLASS_MAPPINGS = { "my unique name" : SimpleCustomNode }
NODE_CLASS_MAPPINGS = {}
#NODE_DISPLAY_NAME_MAPPINGS = { "my unique name" : "Image inverter" }

CC_VERSION = 1.0

#__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
__ALL__ = [NODE_CLASS_MAPPINGS, CC_VERSION]


