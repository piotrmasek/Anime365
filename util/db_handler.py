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
import sqlalchemy as db
import sqlalchemy.orm

from classes.image import Image
from util import api_handler, image_file_handling


def save_post(post_to_save, db_session: db.orm.session):
    url: str = post_to_save['url']
    timestamp: int = post_to_save['created_utc']
    extension = url[url.rfind(".")::]
    name_with_extension = f'{str(timestamp) + extension}'
    anime_title = api_handler.get_anime_name(post_to_save)
    img = Image(file_name=name_with_extension, timestamp=timestamp, anime=anime_title)

    if not is_image_in_db(db_session, img):
        image_file_handling.save_image(name_with_extension, url)
        db_session.add(img)
    else:
        print(f"Skipping existing image: {img}")


def is_image_in_db(db_session: db.orm.session, image: Image):
    return db_session.query(Image).filter(Image.timestamp == image.timestamp).count() > 0
