"""
Module for producing Stable Diffusion comparison sheets with the
Automatic1111 WebUI API. This is for configuring specific comparisons.
"""

from comparison_producer import produce_sheets

# User Inputs

# Stable Diffusion checkpoints will be checked against the list.
# Keep in mind that the web-ui will need its checkpoint list refreshed in-browser.
# if new ones are created or moved.

# VAE will not be checked against the list.
# Parameters in each override list should not conflict.

base_params = {
    "prompt": "photo of a cat, high resolution, dlsr, highly detailed, very realistic, nikon, 4k",
    "negative_prompt": "lowres, worst quality, blurry, cropped",
    "steps": 15,
    "sampler_name": "Euler a",
    "width": 512,
    "height": 512,
    "seed": 1234567890,  # If this is -1 for random, will need to delete cache files to rerandomise.
    "cfg_scale": 4,
    "n_iter": 1,  # Do not change, use image_grid_size instead.
    "override_settings": {  # These will overwrite settings.
        "CLIP_stop_at_last_layers": 1,
        "sd_vae": "auto",  # Use lower-case "auto", or the filename in the VAE folder.
        "sd_model_checkpoint": "sd_1-4_pruned_emaonly.ckpt",
        "sd_hypernetwork": "None",
        "sd_lora": "None",
    },
    "override_settings_restore_afterwards": True,
}

image_grid_size = (2, 3)  # Batch size, but as the desired grid.
image_crop_size = (0, 0)  # Set to (0, 0) or None to disable cropping.
image_crop_coords = [  # Goes from top-left to bottom-right.
    (0, 0),
    (0, 0),
    (0, 0),
    (0, 0),
]

image_overrides = [  # Blocks do not increment seed automatically.
    ("Cat 1234567890", {

    }),
    ("Cat 1234", {
        "seed": 1234
    }),
    ("Dog 9876543210", {
        "prompt": "photo of a dog, high resolution, dlsr, highly detailed, very realistic, nikon, 4k",
        "seed": 9876543210
    }),
    ("Dog 4444444", {
        "prompt": "photo of a dog, high resolution, dlsr, highly detailed, very realistic, nikon, 4k",
        "seed": 4444444
    }),
    ("Turtle 852456", {
        "prompt": "photo of a turtle, high resolution, dlsr, highly detailed, very realistic, nikon, 4k",
        "seed": 852456
    }),
    ("Bird 45678", {
        "prompt": "photo of a bird, high resolution, dlsr, highly detailed, very realistic, nikon, 4k",
        "seed": 45678
    }),
]

horizontal_overrides = [
    ("Steps: 15", {

    }),
    ("Steps: 30", {
        "steps": 30,
    }),
]

vertical_overrides = [
    ("CFG Scale: 4", {

    }),
    ("CFG Scale: 8", {
        "cfg_scale": 8,
    }),
]

sheet_overrides = [  # Names are used for filenames, make sure they are safe.
    ("Stable Diffusion 1.4", {

    }),
    ("Stable Diffusion 1.5", {
        "override_settings": {
            "sd_model_checkpoint": "sd_1-5_pruned-emaonly.ckpt",
        },
    }),
    ("Stable Diffusion 2.1 Base", {
        "override_settings": {
            "sd_model_checkpoint": "sd_2_512-base-ema.ckpt",
        },
    })
]

extra_info = "Extra information\n"\
             "can go here."

produce_sheets(
    base_params,
    image_grid_size,
    sheet_overrides,
    vertical_overrides,
    horizontal_overrides,
    image_overrides,
    extra_info=extra_info,
    image_crop_size=image_crop_size,
    image_crop_coords=image_crop_coords,
    image_grid_padding=32,
    font_size=32,
    disable_sheet_titles=False,
    disable_horizontal_titles=False,
    disable_vertical_titles=False,
    disable_image_titles=False,
    disable_extra_info=False,
    server="http://127.0.0.1:7860",
    timeout=120,
    save_format="jpg",
    save_quality=95,
    save_scale=0.5,
    skip_images=False
    )
