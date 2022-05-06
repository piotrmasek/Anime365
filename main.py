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
import datetime

from classes.image import Image
from util import api_handler
from util import image_file_handling

start_time = datetime.datetime(2021, 12, 31, 0, 0, 0, 0)
end_time = datetime.datetime(2020, 12, 31, 0, 0, 0, 0)

all_posts = api_handler.get_posts(int(start_time.timestamp()), int(end_time.timestamp()))

images = []


def is_post_valid(post):
    extension = post['url'][post['url'].rfind(".")::]
    allowed_extensions = ['.jpg', '.jpeg', '.png']
    if extension not in allowed_extensions:
        return False
    return True


for post in all_posts:
    url: str = post['url']
    timestamp: int = post['created_utc']
    if 'v.redd.it' in url:
        continue
    ext = url[url.rfind(".")::]
    name_with_ext = f'{str(timestamp) + ext}'

    if is_post_valid(post):
        image_file_handling.save_image(name_with_ext, url)
        obj = Image(file_name=name_with_ext, timestamp=timestamp, anime='test')
        images.append(obj)
        # TODO: save to db

print(*images, sep='\n')
