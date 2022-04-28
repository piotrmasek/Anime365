import requests


def save_image(path: str, name_with_extension: str, url: str):
    img = requests.get(url)
    file = open(path + name_with_extension, 'wb')  # other extensions
    file.write(img.content)