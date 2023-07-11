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
* Each image generated is cached at full resolution and uncropped as a PNG.
  * This is saves time when you've made a slight mistake in sheet settings, or want to make a change to only one or some of the dimension settings.
* Will confirm the SD checkpoints exists (but not VAE, hypernetworks, etc). 
* Can disable image/row/column/sheet titles if not wanted.
* Can save as PNG, JPEG or WEBP with quality set for smaller file size.
* Can save sheets at a lower resolution scale for smaller file size.
* Can change font size and padding.

### How-To
Download the repo and place "example_comparison.py" and "comparison_producer.py" in a folder where you want the comparison images to be produced.\
You can run "pip install -r requirements.txt" if you do not already have Pillow (PIL) and Requests installed.\
Make a copy of the "example_comparison.py" script and make changes, then run that script. "comparison_producer.py" is just the internals and is not intended to be ran directly.

Go to http://127.0.0.1:7860/docs to find the webui API (substitute for your IP/port combination if different).\
You can find the parameter names under "POST /sdapi/v1/txt2img".\
As you can see in base_params, some settings are under "override_settings". These can be found under "GET /sdapi/v1/options".

"override_settings_restore_afterwards" is set to true by default, so the settings in "override_settings" shouldn't be retained, but the webui may display them while generating those images.\
You may need to change this to false to save time if switching hypernetworks, VAEs, etc, as it may switch back and forth each image. But check first to make sure that it will save time.

You can read more about the A1111 webui's API here: https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API.

### TODO
* Change font size and padding per title (image, row, column, sheet), as currently they are pre-set scales on the specified font size.
* Add params to image data. 
* Maybe fancy borders to better indicate image groups where images also have a white background.  
