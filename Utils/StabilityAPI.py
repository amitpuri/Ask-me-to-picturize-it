import base64
import io
import os
import re
from os import listdir
from os.path import isfile, join
from io import BytesIO
import requests
from PIL import Image
import tempfile

class StabilityAPI:
    def __init__(self, api_key):
        self.tmpdir = "cloudinary_images"
        self.engine_id = "stable-diffusion-v1-5"
        self.api_host = os.getenv('API_HOST', 'https://api.stability.ai')
        self.api_key = api_key

        if self.api_key is None:
            raise Exception("Stability API key is required.")

    def text_to_image(self, text_prompts, style_preset = "photographic", cfg_scale=7, clip_guidance_preset="FAST_BLUE", height=512, width=512, samples=1, steps=30):
        if self.api_key:                 
            prompt_list = [{"text": text} for text in text_prompts]   
            response = requests.post(
                f"{self.api_host}/v1/generation/{self.engine_id}/text-to-image",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },                
                json={
                    "text_prompts": prompt_list,
                    "cfg_scale": cfg_scale,
                    "clip_guidance_preset": clip_guidance_preset,
                    "height": height,
                    "width": width,
                    "samples": samples,
                    "steps": steps,
                    "style_preset": style_preset
                },
            )

            if response.status_code != 200:
                raise Exception("Non-200 response: " + str(response.text))

            data = response.json()
            image_data = base64.b64decode(data["artifacts"][0]["base64"])
            file_name = "Generated-image.png"
            img = Image.open(io.BytesIO(image_data))
            img.save(os.path.join(self.tmpdir, file_name), quality=85)
            return os.path.join(self.tmpdir, file_name)

    def image_to_image(self, init_image, text_prompts, style_preset = "photographic", image_strength=0.35, cfg_scale=7, clip_guidance_preset="FAST_BLUE", samples=1, steps=30):
        if self.api_key:
            if not text_prompts:
                text_prompts = "image to image"                
                prompt_weight = 0.1
            else:                            
                prompt_weight = 0.5
            try:
                try:
                    with open(init_image, "rb") as file_path:
                        image = Image.open(file_path)
                        width, height = 512, 512
                        image = image.resize((width, height))
                        byte_stream = BytesIO()
                        image.save(byte_stream, format='PNG')
                        image_byte_array = byte_stream.getvalue()
                except Exception as err:
                    print(f"StabilityAPI image_to_image {err}")

                if image_byte_array:
                    response = requests.post(
                        f"{self.api_host}/v1/generation/{self.engine_id}/image-to-image",
                        headers={
                            "Accept": "application/json",
                            "Authorization": f"Bearer {self.api_key}"
                        },
                        files={
                            "init_image": image_byte_array
                        },
                        data={
                            "image_strength": image_strength,
                            "init_image_mode": "IMAGE_STRENGTH",
                            "text_prompts[0][text]": text_prompts,
                            "text_prompts[0][weight]": prompt_weight,
                            "cfg_scale": cfg_scale,
                            "clip_guidance_preset": clip_guidance_preset,
                            "samples": samples,
                            "steps": steps,
                            "style_preset": style_preset
                        }
                    )
                    if response.status_code != 200:
                        raise Exception("Non-200 response: " + str(response.text))
            except Exception as error:
                raise Exception(f"Exception {error}")
            
            data = response.json()
            image_data = base64.b64decode(data["artifacts"][0]["base64"])
            file_name = "Generated-image.png"
            img = Image.open(io.BytesIO(image_data))
            img.save(os.path.join(self.tmpdir, file_name), quality=85)
            return os.path.join(self.tmpdir, file_name)            