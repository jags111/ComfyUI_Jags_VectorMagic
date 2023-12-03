import comfy.diffusers_convert
import comfy.samplers
import comfy.sd
import comfy.utils
import comfy.clip_vision
import torch
import nodes
from typing import Optional
import comfy

try:
    import folder_paths
    application_root_directory = os.path.dirname(folder_paths.__file__)
    application_web_extensions_directory = os.path.join(application_root_directory, "web", "extensions", "ComfyUI_jags_Vectormagic", "utilities")
except:
    pass # not in a ComfyUI environment

class BaseNode:
    def __init__(self):
        pass
    FUNCTION = "func"
    REQUIRED = {}
    OPTIONAL = None
    HIDDEN = None
    @classmethod    
    def INPUT_TYPES(s):
        types = {"required": s.REQUIRED}
        if s.OPTIONAL:
            types["optional"] = s.OPTIONAL
        if s.HIDDEN:
            types["hidden"] = s.HIDDEN
        return types
    RETURN_TYPES = ()
    RETURN_NAMES = ()

class classproperty(object):
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, owner):
        return self.f(owner)
    
class SeedContext():
    """
    Context Manager to allow one or more random numbers to be generated, optionally using a specified seed, 
    without changing the random number sequence for other code.
    """
    def __init__(self, seed=None):
        self.seed = seed
    def __enter__(self):
        self.state = random.getstate()
        if self.seed:
            random.seed(self.seed)
    def __exit__(self, exc_type, exc_val, exc_tb):
        random.setstate(self.state)


# import comfy.model_base as BaseModel

#  Node groups------------------------------
class xy_Tiling_KSampler:
    def __init__(self):
        pass

    @classmethod

    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),

                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
                "cfg": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 100.0}),
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS, ),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS, ),
                "positive": ("CONDITIONING", ),
                "negative": ("CONDITIONING", ),
                "latent_image": ("LATENT", ),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "tileX": ("INT", {"default": 1, "min": 0, "max": 2}),
                "tileY": ("INT", {"default": 1, "min": 0, "max": 2}),
            },
        }

    RETURN_TYPES = ("LATENT", "LATENT")
    RETURN_NAMES = ("latent", "progress_latent")
    FUNCTION = "sample"

    CATEGORY = "Jags_vector/xy_tile_sampler"

    def apply_asymmetric_tiling(self, model, tileX, tileY):
        for layer in [layer for layer in model.modules() if isinstance(layer, torch.nn.Conv2d)]:
            layer.padding_modeX = 'circular' if tileX else 'constant'
            layer.padding_modeY = 'circular' if tileY else 'constant'
            layer.paddingX = (layer._reversed_padding_repeated_twice[0], layer._reversed_padding_repeated_twice[1], 0, 0)
            layer.paddingY = (0, 0, layer._reversed_padding_repeated_twice[2], layer._reversed_padding_repeated_twice[3])
            print(layer.paddingX, layer.paddingY)

    def __hijackConv2DMethods(self, model, tileX: bool, tileY: bool):
        for layer in [l for l in model.modules() if isinstance(l, torch.nn.Conv2d)]:
            layer.padding_modeX = 'circular' if tileX else 'constant'
            layer.padding_modeY = 'circular' if tileY else 'constant'
            layer.paddingX = (layer._reversed_padding_repeated_twice[0], layer._reversed_padding_repeated_twice[1], 0, 0)
            layer.paddingY = (0, 0, layer._reversed_padding_repeated_twice[2], layer._reversed_padding_repeated_twice[3])
            
            def make_bound_method(method, current_layer):
                def bound_method(self, *args, **kwargs):  # Add 'self' here
                    return method(current_layer, *args, **kwargs)
                return bound_method
                
            bound_method = make_bound_method(self.__replacementConv2DConvForward, layer)
            layer._conv_forward = bound_method.__get__(layer, type(layer))

    def __replacementConv2DConvForward(self, layer, input: torch.Tensor, weight: torch.Tensor, bias: Optional[torch.Tensor]):
        working = torch.nn.functional.pad(input, layer.paddingX, mode=layer.padding_modeX)
        working = torch.nn.functional.pad(working, layer.paddingY, mode=layer.padding_modeY)
        return torch.nn.functional.conv2d(working, weight, bias, layer.stride, (0, 0), layer.dilation, layer.groups)

    def __restoreConv2DMethods(self, model):
        for layer in [l for l in model.modules() if isinstance(l, torch.nn.Conv2d)]:
            layer._conv_forward = torch.nn.Conv2d._conv_forward.__get__(layer, torch.nn.Conv2d)
      
    def sample(self, model, seed, tileX, tileY, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=1.0):
        self.__hijackConv2DMethods(model.model, tileX == 1, tileY == 1)
        result = nodes.common_ksampler(model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise)
        self.__restoreConv2DMethods(model.model)
        return result

      # ========================== Custom code ==========================
"""
    def my_function(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
                    denoise=denoise, disable_noise=disable_noise, start_step=start_step, last_step=last_step,
                    force_full_denoise=force_full_denoise, noise_mask=noise_mask, callback=callback, seed=seed):
        samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
                                      denoise=denoise, disable_noise=disable_noise, start_step=start_step, last_step=last_step,
                                      force_full_denoise=force_full_denoise, noise_mask=noise_mask, callback=callback, seed=seed)
        out = latent.copy()
        out["samples"] = samples
        return (out, )

    def print_object_info(self, obj):
        print("Type:", type(obj))
        print("Attributes and methods:", end=" ")
        for item in dir(obj):
            print(item, end=" ")/ 
"""

class CircularVAEDecode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "samples": ("LATENT", ), "vae": ("VAE", )}}
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "decode"

    CATEGORY = "Jags_vector/latent"

    def decode(self, vae, samples):
        for layer in [layer for layer in vae.first_stage_model.modules() if isinstance(layer, torch.nn.Conv2d)]:
            layer.padding_mode = 'circular'
        return (vae.decode(samples["samples"]), )
    
NODE_CLASS_MAPPINGS = {
        "xy_Tiling_KSampler": xy_Tiling_KSampler,
        "CircularVAEDecode": CircularVAEDecode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "xy_Tiling_KSampler": 'Jags-XY_tile sampler',
    "CircularVAEDecode": 'Jags-CircularVAEDecode'
}

    


