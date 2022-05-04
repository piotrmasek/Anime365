import datetime

from classes.image import Image
from util import image_handling
from util import api_handler

start_time = datetime.datetime(2021, 12, 31, 0, 0, 0, 0)
posts_before_ts = int(start_time.timestamp())

all_posts = api_handler.get_posts(posts_before_ts)
images = []
for post in all_posts:
    url: str = post['url']
    if 'v.redd.it' in url:
        continue
    ext = url[url.rfind(".")::]
    title = post['title']
    name_with_ext = f'{title + ext}'
    image_handling.save_image(title, url)

    obj = Image(post['id'], name_with_ext, datetime.datetime.now().timestamp(), "ONE PIS", 10)
    images.append(obj)

print(*images, sep='\n')


