import os, random

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


class xy_Tiling_KSampler:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),

                "seed": ("SEED", ),
                "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
                "cfg": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 100.0}),
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS, ),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS, ),
                "positive": ("CONDITIONING", ),
                "negative": ("CONDITIONING", ),
                "latent_image": ("LATENT", ),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),

                # here is custom config
                "step_range": ("INT", {
                    "startStep": 0,  # Start tiling from step N
                    "stopStep": -1  # Stop tiling after step N (-1: Don't stop)
                }),
                "tileX": (["enable", "disable"],),
                "tileY": (["enable", "disable"],)
            },
        }

    RETURN_TYPES = ("LATENT",)

    FUNCTION = "sample"

    CATEGORY = "Alsritter/Sampling"

    def sample(self, model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
               step_range, tileX, tileY, denoise=1.0):

        if tileX != "enable" and tileY != "enable":
            return nodes.common_ksampler(model, seed['seed'], steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise)
        else:
            return self.tile_ksampler(model, seed['seed'], steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise)

    # Self-determined 
    def tile_ksampler(self, model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent, denoise=1.0, disable_noise=False, start_step=None, last_step=None, force_full_denoise=False):

        # ========================== Base code ==========================
        device = comfy.model_management.get_torch_device()
        latent_image = latent["samples"]

        if disable_noise:
            noise = torch.zeros(latent_image.size(
            ), dtype=latent_image.dtype, layout=latent_image.layout, device="cpu")
        else:
            batch_inds = latent["batch_index"] if "batch_index" in latent else None
            noise = comfy.sample.prepare_noise(latent_image, seed, batch_inds)

        noise_mask = None
        if "noise_mask" in latent:
            noise_mask = latent["noise_mask"]

        preview_format = "JPEG"
        if preview_format not in ["JPEG", "PNG"]:
            preview_format = "JPEG"

        previewer = latent_preview.get_previewer(
            device, model.model.latent_format)

        # Arrangement progress clause
        pbar = comfy.utils.ProgressBar(steps)

        def callback(step, x0, x, total_steps):
            preview_bytes = None

            self.print_object_info(step)
            self.print_object_info(x0)
            self.print_object_info(x)
            self.print_object_info(total_steps)

            #Generation guide
            if previewer:
                preview_bytes = previewer.decode_latent_to_preview_image(
                    preview_format, x0)
            # Update progress clause
            pbar.update_absolute(step + 1, total_steps, preview_bytes)

      # ========================== Custom code ==========================

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
            print(item, end=" ")


