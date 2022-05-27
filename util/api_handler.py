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
#
#
#
#
import datetime
import json
import re
import time

import requests


def get_posts(to_timestamp: int, from_timestamp: int, step_size: int = 20):
    fetched_posts = []
    current_max_timestamp = to_timestamp
    while current_max_timestamp >= from_timestamp:
        request_url = f'https://api.pushshift.io/reddit/search/submission/' \
                      f'?subreddit=animecalendar' \
                      f'&sort=desc' \
                      f'&sort_type=created_utc' \
                      f'&before={current_max_timestamp}' \
                      f'&size={step_size}'
        print(f'Sending request: {request_url}')
        response = requests.get(request_url)
        if not response.ok:
            if response.status_code == 429:
                handle_rate_limit()
                continue
            else:
                raise ConnectionError(f"Bad response. Code: {response.status_code}")
        posts = json.loads(response.text)
        if len(posts['data']) == 0:
            break
        fetched_posts += posts['data']
        print(f"Added {len(posts['data'])} Total {len(fetched_posts)}")
        current_max_timestamp = posts['data'][-1]['created_utc']
        if current_max_timestamp < from_timestamp:
            break
        print(f'posts before: {datetime.datetime.fromtimestamp(current_max_timestamp)}')
    return fetched_posts


def get_anime_name(post: dict) -> str:
    link_id = post['id']
    request_url = f'https://api.pushshift.io/reddit/comment/search/?link_id={link_id}&subreddit=animecalendar'
    print(f'Sending request: {request_url}')
    response = requests.get(request_url)
    if not response.ok:
        if response.status_code == 429:
            handle_rate_limit()
            return get_anime_name(post)
        else:
            raise ConnectionError(f"Bad response. Code: {response.status_code}")

    if len(response.text) == 0:
        print('Empty response text')
        return ''
    comments = json.loads(response.text)['data']
    roboragi = [comment for comment in comments if comment['author'] == 'Roboragi']
    if len(roboragi) == 0:
        print('Roboragi nor found')
        return ''
    comment_body = roboragi[0]['body']
    found = re.match(r'\*\*.*\*\*', comment_body)
    if found is None:
        print(f'Anime title not found in: {comment_body}')
        return ''
    name = comment_body[found.start():found.end()]
    return name.strip('*')


def handle_rate_limit():
    print("Rate limit reached! Waiting 1 min...")
    time.sleep(60)
    print('Wakey, wakey!')
