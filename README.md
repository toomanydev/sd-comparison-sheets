# sd-comparison-sheets
Uses the API of the Automatic1111 webui to produce comparison sheets.\
Intended to be an improvement over the standard X/Y/Z plot script.

### Generation Features
* Override image generation parameters per: image, row, column, sheet.
  * This is 4 custom dimensions as opposed to the standard 3 custom dimensions with 1 dimension exclusively for seed changes.
* Each dimension can have multiple overrides
  * e.g. choosing a different seed per image as well as changing prompt.
* Each sheet is produced as a separate image for more convenient comparison.
* Can place extra information at the bottom.
  * e.g. image parameters that were static across all generations.
* Can generate images at higher resolution, but crop them if not interested in the entire image.
  
### Convenience Features
* Each image generated is cached at full resolution and uncropped as a PNG, so that you can change the sheet settings and rerun the script quickly without having to regenerate all the images.
* Can disable image/row/column/sheet titles if not wanted.
* Can save as PNG, JPEG or WEBP with quality set for smaller file size.
* Can save at a lower resolution scale for smaller file size.
* Can change font size and padding.

### Info
You can read about the A1111 webui's API here: https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API \

Go to http://127.0.0.1:7860/docs to find the webui API (substitute for your IP/port combination if different).\
You can find the parameter names under "POST /sdapi/v1/txt2img".\
As you can see in base_params, some settings are under "override_settings". These can be found under "GET /sdapi/v1/options".\
For consistency, "override_settings_restore_afterwards" is set to false, so your settings will be saved.

Make a copy of "example_comparison.py" and make changes to match your desired comparisons, then run that script. "comparison_producer.py" is just the internals and is not intended to be ran directly.

### TODO
* Change font size and padding per title (image, row, column, sheet), as currently they are pre-set scales on the specified font size.
* Add params to image data. 
* Maybe fancy borders to better indicate image groups where images also have a white background.  
