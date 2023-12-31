# sd-comparison-sheets
Uses the API of the Automatic1111 webui to produce comparison sheets.  
Intended to be an improvement over the standard X/Y/Z plot script.  
This is not an extension, it is a standalone script.

### Comparison Features
* Provide the base image generation parameters, then override them per: image, row, column, sheet.
  * This is 4 dimensions as opposed to the standard 3 dimensions with 1 dimension exclusively for seed changes.
* Each dimension can have multiple overrides.
  * e.g. choosing a different seed per image as well as changing prompt.
  * This can allow you to create even more ad-hoc dimensions to compare.
* Custom image/row/column/sheet titles.
* Each sheet is produced as a separate image for more convenient comparison in an image viewer / multiple browser tabs.
* Can define the image block grid size (e.g. 3x2 or 2x3).
* Can place extra information at the bottom.
  * e.g. image parameters that were static across all generations, why you were comparing, etc.
* Can generate images at higher resolution, but crop them if not interested in the entire image.
  * e.g. if you want a headshot, but the model generates these more reliably as a whole upper-body picture.
  
### Convenience Features
* Each image generated is cached at full resolution and uncropped as a PNG.
  * This is saves time when you've made a slight mistake in sheet settings, or want to make a change to only one or some of the dimension settings.
* The script will confirm the SD checkpoints exists (but not VAE, hypernetworks, etc) before starting. 
* Can disable image/row/column/sheet titles if not wanted.
* Can save as PNG, JPEG or WEBP with quality set for smaller file size.
* Can save sheets at a lower resolution scale for smaller file size.
* Can change font size and padding.

### Example
Output of "example_comparison.py":
| SD 1.4 | SD 1.5 | SD 2.1 |
| --- | --- | --- |
| ![1_Stable Diffusion 1 4](https://github.com/toomanydev/sd-comparison-sheets/assets/69650390/f276c841-9a17-44aa-b55d-d0bfefa74186) | ![2_Stable Diffusion 1 5](https://github.com/toomanydev/sd-comparison-sheets/assets/69650390/848b7302-fe74-4cfd-8e46-c4798cf2bc06) | ![3_Stable Diffusion 2 1 Base](https://github.com/toomanydev/sd-comparison-sheets/assets/69650390/8d3f5628-be78-4fe9-8163-36b35bf5896d) |

### How-To
* Have Python and pip installed, etc.
* Have the Automatic1111 webui running with API enabled by using `--api` in your "webui-user.bat" file's `COMMANDLINE_ARGS` section.
* Download the repo and place "example_comparison.py" and "comparison_producer.py" in a folder where you want the comparison images to be produced.
* You can run `pip install -r requirements.txt` if you do not already have Pillow (PIL) and Requests installed.
* Make a copy of the "example_comparison.py" script called "your_comparison.py" and make changes.  
  Keeping the example comparison script as-is will let you reference it later.
* Go to http://127.0.0.1:7860/docs to find the webui API (substitute for your IP/port combination if different).  
  Here, you will find the parameters you can change under `POST /sdapi/v1/txt2img`.  
  You may not need to go find parameters if the ones in the example are sufficient.
  * As you can see in the example, some settings are under `override_settings`.  
    These can be found under `GET /sdapi/v1/options`.
* Run "your_comparison.py".

#### Notes
* You will need to change the seed manually if that is desired, by default it will use the seed in `base_params`.
* You can see the images being generated in "/cache".
* If you generate an image with a random seed using -1, it will still be obtained from cache when the script is re-run.  
  You can re-generate it with another random seed by deleting it in "/cache".
* "comparison_producer.py" is just the internals and is not intended to be ran directly.
* The first entry in an overrides list is usually empty, as it is intended that all of the base parameters are being used.  
  However, you could place settings here if you find it easier to read.
* `override_settings_restore_afterwards` is set to true by default, so the settings in `override_settings` shouldn't be retained, but the webui may display them in the browser while generating those images.  
  You may need to change this to false to save time if switching hypernetworks, VAEs, etc, as it may switch back and forth each image. But check first to make sure that it will save time - the function of the API may have changed since I observed this.
* You can read more about the A1111 webui's API here: https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API.

### TODO
* Change font size and padding per title (image, row, column, sheet), as currently they are pre-set scales on the specified font size.
* Allow multiple lines on the image titles.
* Add params to image data. 
* Maybe fancy borders to better indicate image groups where images also have a white background, other nice things, etc.
