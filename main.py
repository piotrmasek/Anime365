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

import sqlalchemy as db
import sqlalchemy.orm

from classes.image import Image
from util import api_handler
from util import image_file_handling


def is_post_valid(post_to_validate) -> bool:
    url: str = post_to_validate['url']
    extension = url[url.rfind(".")::]
    allowed_extensions = ['.jpg', '.jpeg', '.png']

    if 'v.redd.it' in url:
        return False
    if extension not in allowed_extensions:
        return False
    return True


def save_post(post_to_save, db_session):
    url: str = post_to_save['url']
    timestamp: int = post_to_save['created_utc']
    extension = url[url.rfind(".")::]
    name_with_extension = f'{str(timestamp) + extension}'
    image_file_handling.save_image(name_with_extension, url)
    img = Image(file_name=name_with_extension, timestamp=timestamp, anime='test')
    db_session.add(img)


start_time = datetime.datetime(2021, 12, 31, 0, 0, 0, 0)
end_time = datetime.datetime(2021, 11, 1, 0, 0, 0, 0)

fetched_posts = api_handler.get_posts(int(start_time.timestamp()), int(end_time.timestamp()))

engine = db.create_engine('sqlite:///anime365.sqlite')
session_maker = db.orm.sessionmaker()
session_maker.configure(bind=engine)
Image.metadata.create_all(engine)
session = session_maker()

for post in fetched_posts:
    if not is_post_valid(post):
        continue
    save_post(post, session)
session.commit()
