#  Copyright (c) 2022 Piotr Masek
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the “Software”), to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of
#  the Software.
#
#  THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND  NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
#  CONTRACT, TORT OR OTHERWISE, ARISING FROM,  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
#  IN THE SOFTWARE.

#
#
import os

import requests


def save_image(name_with_extension: str, url: str):
    image_store_dir = 'data/img/'
    try:
        os.mkdir(image_store_dir)
    except FileExistsError:
        pass
    file_path = image_store_dir + name_with_extension
    if os.path.exists(file_path):
        print(f"File exists: {file_path}. Skipping.")
        return

    print(f'Downloading {name_with_extension}...')
    img = requests.get(url)

    try:
        file = open(file_path, 'wb')  # other extensions
    except OSError:
        print(f"Can't create file: {file_path}. Skipping.")
        return
    file.write(img.content)
