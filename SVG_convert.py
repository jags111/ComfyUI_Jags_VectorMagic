"""
@author: jags111
@title: Jags_VectorMagic
@nickname: Jags_VectorMagic
@description: This extension offers various vector manipulation and  generation tools
"""
import folder_paths
import torch
import os
import sys
import re
import nodes
from typing import Optional
import comfy
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import locale
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), 'comfy'))
original_locale = locale.setlocale(locale.LC_TIME, '')


# Node selections

class color_drop():
    """
    This node provides a simple interface to apply PixelSort blur to the output image.
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        """
        Input Types
        """
        return {
            "required": {
                "images": ("IMAGE",),},
            "optional": {
                "number_of_colors": ("INT", {"default": 2, "min": 1, "max": 4000, "step": 1}),
                },
            }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Image",)
    FUNCTION = "flatten"
"""
    CATEGORY = "Jags_vector/SVG"

    def tensor_to_pil(self, img):
        if img is not None:
            i = 255. * img.cpu().numpy().squeeze()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        return img

    def flatten(self, images, number_of_colors):
        #create empty tensor with the same shape as images
        total_images = []
        for image in images:
            image = self.tensor_to_pil(image)
            image = image.convert('P', palette=Image.ADAPTIVE, colors=number_of_colors)
            
            # convert to tensor
            out_image = np.array(image.convert("RGB")).astype(np.float32) / 255.0
            out_image = torch.from_numpy(out_image).unsqueeze(0)
            total_images.append(out_image)


        total_images = torch.cat(total_images, 0)
        return (total_images,)

class SVG ():
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = 'output'
        self.prefix_append = ''

    @classmethod
    def INPUT_TYPES(s):
        return {
			'required': {
				'images': ('IMAGE', ),
				'filename_prefix': ('STRING', {'default': 'myFile'}),
				'image_preview': (['disabled', 'enabled'], {'default': 'enabled'}),
			},
			"optional": {
                    ""
                    },
			'hidden': {''},
		}

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("SVG",)
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "Jags_vector/SVG"

      
    def LoadSvg(ImagesPath):
        if isinstance(ImagesPath, str):
            ImagesPath = [ImagesPath]

        images = []
        image_count = 0
        for path in ImagesPath:
            try:
                svg_data = open(path, "rb").read()
                images.append(svg_data)
                image_count += 1
            except Exception as e:
                print(f"Error loading SVG at path {path}: {e}")

        return { "ui": { "images": images } }
 """   

NODE_CLASS_MAPPINGS = {
    "color_drop": color_drop,
    #"SVG": SVG,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "color_drop": "Jags_Color Drop",
    #"SVG": "Jags_SVG",
}