import cloudinary
import cloudinary.uploader
from Utils.ImageUtils import *

class CloudinaryClient:
    def __init__(self, cloud_name: str, api_key: str, api_secret: str):
        self.cloudinary_api_version = "v1682190709"
        self.cloud_name = cloud_name
        self.api_key = api_key
        self.api_secret = api_secret
        self.folder_name = ""
        cloudinary.config(
            cloud_name=f"{self.cloud_name}",
            api_key=f"{self.api_key}",
            api_secret=f"{self.api_secret}",
            secure=True,
        )
    
    def set_folder_name(self, folder_name: str):
        self.folder_name = folder_name

    def upload_image(self, input_celeb_picture: str, celebrity_name: str):
        if not self.cloud_name or not self.api_key or not self.api_secret or not self.folder_name:
            return None
            
        print(celebrity_name)
        print(input_celeb_picture)
        print(self.folder_name)
        try:
            response = cloudinary.uploader.upload(input_celeb_picture, public_id=celebrity_name, folder=self.folder_name)
            return response["url"]
        except cloudinary.exceptions.Error: 
            raise Exception(result["error"]["message"])

    def search_images(self):
        if not self.cloud_name or not self.api_key or not self.api_secret or not self.folder_name:
            return None
        try:         
            result = cloudinary.Search().expression(f"folder={self.folder_name}").execute()
        except cloudinary.exceptions.Error: 
            raise Exception(result["error"]["message"])
        base_url = f"http://res.cloudinary.com/{self.cloud_name}/image/upload/{self.cloudinary_api_version}/{self.folder_name}"
        image_utils = ImageUtils()
        celebs_pictures = [image_utils.write_image(pic["url"], pic["url"][len(base_url)+1:]) for pic in result["resources"]]
        return celebs_pictures