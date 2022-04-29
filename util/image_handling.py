import requests
import os


def save_image( name_with_extension: str, url: str):
    image_store_dir = 'img/'
    try:
        os.mkdir(image_store_dir)
    except FileExistsError:
        pass

    img = requests.get(url)
    file = open(image_store_dir + name_with_extension, 'wb')  # other extensions
    file.write(img.content)
