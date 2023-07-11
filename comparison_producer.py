"""
Module for producing Stable Diffusion comparison sheets with the
Automatic1111 WebUI API. This is the main script, nothing to change here.
"""

import base64
import copy
import io
import hashlib
import os
import re
import time
import requests
from PIL import Image, ImageDraw, ImageFont

# TODO: assert that no overrides conflict/use same things.
# TODO: add params in exif on a per-image asis.


def override_params(base_params: dict, override: dict) -> dict:
    new_params = copy.deepcopy(base_params)

    if override is not None:
        for key in override:
            if key != "override_settings":
                new_params[key] = override[key]

        if "override_settings" not in base_params:
            new_params["override_settings"] = {}

        if "override_settings" in override:
            for key in override["override_settings"]:
                new_params["override_settings"][key] = \
                    override["override_settings"][key]

    return new_params


def params_model_exists(params: dict, server: str, timeout: int) -> bool:
    # TODO: confirm VAE exists (API not implemented).

    if params is not None:
        response = requests.get(url=f'{server}/sdapi/v1/sd-models',
                                timeout=timeout)
        sd_models = []

        for model in response.json():
            if model["title"][len(model["title"]
                                  )-1:len(model["title"])] == "]":
                sd_models.append(model["title"][0:len(model["title"])-13])
            else:
                sd_models.append(model["title"])

        if "override_settings" in params:
            if "sd_model_checkpoint" in params["override_settings"]:
                if params["override_settings"]["sd_model_checkpoint"] not \
                      in sd_models:
                    print(
                        f'{params["override_settings"]["sd_model_checkpoint"]}'
                        ' does not exist.')
                    return False

    return True


def produce_image(
        params: dict,
        image_crop_size: tuple[int, int],
        image_crop_coords: tuple[int, int],
        timeout: int,
        server: str,
        skip_images: bool
        ) -> Image.Image:
    if skip_images:
        image = Image.new("RGB", (image_crop_size[0], image_crop_size[1]),
                          "white")
        return image

    try:
        os.mkdir("cache")
    except FileExistsError:
        pass

    try:
        image = Image.open(f"./cache/{hashlib.md5(str(params).encode('utf-8')).hexdigest()}.png")
    except FileNotFoundError:
        response = requests.post(url=f'{server}/sdapi/v1/txt2img',
                                 json=params, timeout=timeout)

        try:
            image = Image.open(io.BytesIO(base64.b64decode(
                response.json()["images"][0].split(",", 1)[0])))
        except Exception:
            print(response.json())

        image.save(f"./cache/{hashlib.md5(str(params).encode('utf-8')).hexdigest()}.png")

    image = image.crop((image_crop_coords[0], image_crop_coords[1],
                        image_crop_coords[0] + image_crop_size[0],
                        image_crop_coords[1] + image_crop_size[1]))

    return image


def produce_sheet(
        base_params: dict,
        image_grid_size: tuple[int, int],
        sheet_name: str,
        vertical_overrides: list[tuple[str, dict]],
        horizontal_overrides: list[tuple[str, dict]],
        image_overrides: list[tuple[str, dict]],
        extra_info: str,
        image_crop_size: tuple[int, int],
        image_crop_coords: list[tuple[int, int]],
        timeout: int,
        image_grid_padding: int,
        font_size: int,
        disable_image_titles: bool,
        disable_horizontal_titles: bool,
        disable_vertical_titles: bool,
        disable_sheet_titles: bool,
        disable_extra_info: bool,
        server: str,
        skip_images: bool
        ) -> Image.Image:

    assert (image_grid_size[0] * image_grid_size[1]) == len(image_overrides),\
        "Grid size does not match the number of image overrides."

    if image_crop_size is None or image_crop_size[0] == 0 or \
            image_crop_size[0] == 0:
        print("Image crop size is None or has a zero: disabling crops.")
        image_crop_size = (base_params["width"], base_params["height"])

        image_crop_coords = []
        length = image_grid_size[0] * image_grid_size[1]
        for i in range(length):
            image_crop_coords.append((0, 0))
    else:
        assert (image_grid_size[0] * image_grid_size[1]) == \
            len(image_crop_coords), \
            "Image crop coordinates quantity does not match the image grid "\
            "size. May set image crop size to None or (0, 0) to disable."

    image_count = (image_grid_size[0] * image_grid_size[1]) * \
        len(horizontal_overrides) * len(vertical_overrides)
    count = 0
    images = []

    for v, v_override in enumerate(vertical_overrides):
        images.append([])
        for h, h_override in enumerate(horizontal_overrides):
            images[v].append([])
            for i, i_override in enumerate(image_overrides):
                images[v][h].append([])
                params = override_params(override_params(override_params(
                    base_params, v_override[1]), h_override[1]), i_override[1])
                image_grid_count = image_grid_size[0] * image_grid_size[1]
                count = count + 1
                print(f"Starting image: image {i+1} of {image_grid_count}, "
                      f"column {h+1} of {len(horizontal_overrides)}, row {v+1}"
                      f" of {len(vertical_overrides)}. {count}/{image_count}, "
                      f"{round((count/image_count)*100,2)}%.")
                images[v][h][i] = produce_image(params, image_crop_size,
                                                image_crop_coords[i], timeout,
                                                server, skip_images)

    image_size = image_crop_size
    block_size = (
        image_size[0] * image_grid_size[0],
        image_size[1] * image_grid_size[1]
    )
    column_title_size = (
        block_size[0],
        font_size * 2 * 2
    )
    if disable_horizontal_titles:
        column_title_size = (0, 0)
    row_title_size = (
        image_size[0],
        block_size[1]
    )
    if disable_vertical_titles:
        row_title_size = (0, 0)
    sheet_title_size = (
        row_title_size[0] + (block_size[0] * len(horizontal_overrides)) +
        (image_grid_padding * (len(horizontal_overrides) - 1)),
        int(font_size * 2.5 * 2)
    )
    if disable_sheet_titles:
        sheet_title_size = (0, 0)
    extra_info_size = (
        (row_title_size[0] + (block_size[0] * len(horizontal_overrides)) +
            (image_grid_padding * (len(horizontal_overrides) - 1))),
        (font_size * 3) + (font_size * max(extra_info.count('\n'), 1))
    )
    if disable_extra_info:
        extra_info_size = (0, 0)
    sheet_size = (
        row_title_size[0] + (block_size[0] * len(horizontal_overrides)) +
        (image_grid_padding * (len(horizontal_overrides) - 1)),
        sheet_title_size[1] + column_title_size[1] +
        (block_size[1] * len(vertical_overrides)) +
        (image_grid_padding * (len(vertical_overrides) - 1)) +
        extra_info_size[1]
    )
    extra_info_coords = (
        sheet_size[0] / 2,
        sheet_size[1] - (extra_info_size[1] / 2)
    )
    initial_block_coords = (
        row_title_size[0],
        sheet_title_size[1] + column_title_size[1]
    )
    block_offset = (
        block_size[0] + image_grid_padding,
        block_size[1] + image_grid_padding,
    )
    initial_column_title_coords = (
        row_title_size[0] + (block_size[0] * 0.5),
        sheet_title_size[1] + (column_title_size[1] * 0.5)
    )
    column_title_offset = (block_offset[0], 0)
    initial_row_title_coords = (
        font_size * 0.25,
        sheet_title_size[1] + column_title_size[1] + (block_size[1] * 0.5)
    )
    row_title_offset = (0, block_offset[1])
    image_title_offset = (font_size * 0.25, image_size[1] - (font_size * 0.25))

    sheet = Image.new("RGB", sheet_size, "white")
    draw = ImageDraw.Draw(sheet)

    if not disable_sheet_titles:
        draw.text((
            sheet_title_size[0] / 2,
            sheet_title_size[1] / 2
            ),
            sheet_name, fill="black", anchor="mm", align="center",
            font=ImageFont.truetype('arial.ttf', int(font_size * 2.5)),
            stroke_width=2, stroke_fill="white")

    if not disable_extra_info:
        draw.text((
            extra_info_coords[0],
            extra_info_coords[1]
            ),
            extra_info, fill="black", anchor="mm", align="center",
            font=ImageFont.truetype('arial.ttf', int(font_size * 1)),
            stroke_width=2, stroke_fill="white")

    for v, v_list in enumerate(images):
        if not disable_vertical_titles:
            draw.text((
                initial_row_title_coords[0],
                initial_row_title_coords[1] + (row_title_offset[1] * v)
                ),
                vertical_overrides[v][0], fill="black", anchor="lm",
                font=ImageFont.truetype('arial.ttf', int(font_size * 1.5)),
                stroke_width=2, stroke_fill="white")
        for h, h_list in enumerate(v_list):
            if not disable_horizontal_titles:
                draw.text((
                    initial_column_title_coords[0] +
                    (column_title_offset[0] * h),
                    initial_column_title_coords[1]
                    ),
                    horizontal_overrides[h][0], fill="black", anchor="mm",
                    align="center",
                    font=ImageFont.truetype('arial.ttf',
                                            int(font_size * 1.5)),
                    stroke_width=2, stroke_fill="white")
            for i, image in enumerate(h_list):
                col = int(i % image_grid_size[0])
                row = int(i / image_grid_size[0])
                sheet.paste(image, (
                    (initial_block_coords[0] + (block_offset[0] * h))
                    + (col * image_size[0]),
                    initial_block_coords[1] + (block_offset[1] * v)
                    + (row * image_size[1]),
                    ))
                if not disable_image_titles:
                    draw.text((
                        (initial_block_coords[0] + (block_offset[0] * h))
                        + (col * image_size[0]) + image_title_offset[0],
                        initial_block_coords[1] + (block_offset[1] * v)
                        + (row * image_size[1]) + image_title_offset[1],
                        ),
                        image_overrides[i][0], fill="black", anchor="lb",
                        font=ImageFont.truetype('arial.ttf',
                                                int(font_size * 1.0)),
                        stroke_width=int(font_size / 16), stroke_fill="white")

    return sheet


def produce_sheets(
        base_params: dict,
        image_grid_size: tuple[int, int],
        sheet_overrides: list[tuple[str, dict]],
        vertical_overrides: list[tuple[str, dict]],
        horizontal_overrides: list[tuple[str, dict]],
        image_overrides: list[tuple[str, dict]],
        extra_info: str = None,
        image_crop_size: tuple[int, int] = None,
        image_crop_coords: list[tuple[int, int]] = None,
        timeout: int = 120,
        image_grid_padding: int = 0,
        font_size: int = 32,
        disable_image_titles: bool = False,
        disable_horizontal_titles: bool = False,
        disable_vertical_titles: bool = False,
        disable_sheet_titles: bool = False,
        disable_extra_info: bool = False,
        server: str = "http://127.0.0.1:7860",
        save_format: str = "png",
        save_quality: int = 95,
        save_scale: int = 1,
        skip_images: bool = False
        ):

    start_time = time.time()

    assert params_model_exists(base_params, server, timeout), \
        "SD checkpoint provided does not exist."
    for override in sheet_overrides:
        assert params_model_exists(override[1], server, timeout), \
            "SD checkpoint provided does not exist."
    for override in vertical_overrides:
        assert params_model_exists(override[1], server, timeout), \
            "SD checkpoint provided does not exist."
    for override in horizontal_overrides:
        assert params_model_exists(override[1], server, timeout), \
            "SD checkpoint provided does not exist."
    for override in image_overrides:
        assert params_model_exists(override[1], server, timeout), \
            "SD checkpoint provided does not exist."

    for i, override in enumerate(sheet_overrides):
        print(f"Starting sheet {i+1} of {len(sheet_overrides)}")
        filename = re.sub('[<>:"/\\|?*]{1}', '',
                          f"{i+1}_{override[0]}.{save_format}")
        sheet = produce_sheet(
            base_params=override_params(base_params, override[1]),
            image_grid_size=image_grid_size,
            sheet_name=override[0],
            vertical_overrides=vertical_overrides,
            horizontal_overrides=horizontal_overrides,
            image_overrides=image_overrides,
            extra_info=extra_info,
            image_crop_size=image_crop_size,
            image_crop_coords=image_crop_coords,
            timeout=timeout,
            image_grid_padding=image_grid_padding,
            font_size=font_size,
            disable_image_titles=disable_image_titles,
            disable_horizontal_titles=disable_horizontal_titles,
            disable_vertical_titles=disable_vertical_titles,
            disable_sheet_titles=disable_sheet_titles,
            disable_extra_info=disable_extra_info,
            server=server,
            skip_images=skip_images
        )
        sheet = sheet.resize([int(sheet.size[0]*save_scale),
                             int(sheet.size[1]*save_scale)],
                             Image.Resampling.LANCZOS)
        if save_format == "png":
            sheet.save(filename)
        elif save_format == "jpg" or save_format == "jpeg":
            sheet.save(filename, quality=save_quality)
        elif save_format == "webp":
            sheet.save(filename, "WEBP", quality=save_quality)

        print(f"Sheet {filename} saved.")

    end_time = time.time()
    print(f"Took {round(end_time-start_time,2)} seconds.")
