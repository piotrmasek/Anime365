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
import getopt
import sys

import sqlalchemy as db
import sqlalchemy.orm

from backend.classes.image import Image
from backend.util import api_handler, db_handler
from backend.util.api_handler import is_post_valid


# import sqlalchemy.sql.functions as func


def update_image_collection(start_time, end_time):
    engine = db.create_engine('sqlite:///anime365.sqlite')
    session_maker = db.orm.sessionmaker()
    session_maker.configure(bind=engine)
    Image.metadata.create_all(engine)
    db_session = session_maker()

    # TODO limit post range
    # min_timestamp = db_session.query(func.min(Image.timestamp)).scalar()
    # max_timestamp = db_session.query(func.max(Image.timestamp)).scalar()

    fetched_posts = api_handler.get_posts(int(start_time.timestamp()), int(end_time.timestamp()))
    for post in fetched_posts:
        if not is_post_valid(post):
            continue
        db_handler.save_post(post, db_session)
    db_session.commit()


def main(argv):
    start_time = datetime.datetime(2021, 12, 31, 0, 0, 0, 0)
    end_time = datetime.datetime(2021, 12, 14, 0, 0, 0, 0)

    help_string = "image_collection_updater.py -b <begin timestamp> -e <end timestamp>"

    try:
        opts, args = getopt.getopt(argv, "hb:e:", ["begin=", "end="])
    except getopt.GetoptError:
        print(help_string)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_string)
            sys.exit()
        elif opt in ("-b", "begin="):
            start_time = datetime.datetime.fromisoformat(arg)
        elif opt in ("-e", "end="):
            end_time = datetime.datetime.fromisoformat(arg)

    print(f"Running update with begin={start_time.isoformat()}, end={end_time.isoformat()}")
    update_image_collection(start_time, end_time)


if __name__ == "__main__":
    main(sys.argv[1:])
