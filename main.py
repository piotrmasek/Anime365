import datetime

import requests
import json
import os

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

print(len(all_posts))
path = 'img/'

try:
    os.mkdir(path)
except FileExistsError:
    print('img/ already exists')

for post in all_posts:
    url: str = post['url']
    if 'v.redd.it' in url:
        continue
    ext = url[url.rfind(".")::]
    img = requests.get(post['url'])
    title = post['title']
    file = open(path + f'{title + ext}', 'wb')  # other extensions
    file.write(img.content)

