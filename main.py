import datetime

import requests
import json
import os

import image_handling

from image import Image

start_time = datetime.datetime(2021, 12, 31, 0, 0, 0, 0)
posts_before_ts = int(start_time.timestamp())
all_posts = []

while True:
    url = f'https://api.pushshift.io/reddit/search/submission/' \
          f'?subreddit=animecalendar&sort=desc&sort_type=created_utc&before={posts_before_ts}'

    response = requests.get(url)
    posts = json.loads(response.text)
    if len(posts['data']) == 0:
        break
    all_posts += posts['data']
    posts_before_ts = posts['data'][-1]['created_utc']
    break

image_store_dir = 'img/'

try:
    os.mkdir(image_store_dir)
except FileExistsError:
    print('img/ already exists')

images = []


for post in all_posts:
    url: str = post['url']
    if 'v.redd.it' in url:
        continue
    ext = url[url.rfind(".")::]

    title = post['title']
    name_with_ext = f'{title + ext}'
    image_handling.save_image(image_store_dir, title, url)

    obj = Image(post['id'], name_with_ext, datetime.datetime.now().timestamp(), "ONE PIS", 10)
    images.append(obj)

print(*images, sep='\n')


