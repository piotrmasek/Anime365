import json

import requests


def get_posts(max_timestamp: int):
    all_posts = []
    current_max_timestamp = max_timestamp
    while True:
        request_url = f'https://api.pushshift.io/reddit/search/submission/' \
              f'?subreddit=animecalendar' \
              f'&sort=desc' \
              f'&sort_type=created_utc' \
              f'&before={current_max_timestamp}'

        response = requests.get(request_url)
        posts = json.loads(response.text)
        if len(posts['data']) == 0:
            break
        all_posts += posts['data']
        current_max_timestamp = posts['data'][-1]['created_utc']
        break
    return all_posts
