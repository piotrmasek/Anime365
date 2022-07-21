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
import random
import sys

import sqlalchemy as db
import sqlalchemy.orm
from PyQt6 import QtWidgets
from PyQt6.QtGui import QPixmap

from backend.classes.image import Image


def show_random_image(graphics_view: QtWidgets.QGraphicsView, images_pool: list[Image]) -> Image:
    images_dir: os.path = 'img/'
    img = random.choice(images_pool)
    pix = QPixmap(os.path.join(images_dir, img.file_name))
    item = QtWidgets.QGraphicsPixmapItem(pix)
    scene = QtWidgets.QGraphicsScene(graphics_view)
    scene.addItem(item)
    graphics_view.setScene(scene)
    return img


def run_quiz(argv):
    engine = db.create_engine('sqlite:///anime365.sqlite')
    session_maker = db.orm.sessionmaker(engine)
    Image.metadata.create_all(engine)
    db_session = session_maker()

    images = db_session.query(Image).all()

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()

    window.setWindowTitle('Anime365')

    layout = QtWidgets.QVBoxLayout(window)

    gfv = QtWidgets.QGraphicsView(window)
    show_random_image(gfv, images)
    layout.addWidget(gfv)

    button = QtWidgets.QPushButton(window)
    button.setText('次')
    button.clicked.connect(lambda: on_click(button, gfv, images))
    layout.addWidget(button)

    window.showMaximized()

    sys.exit(app.exec())


def on_click(button, gfv, images):
    i = show_random_image(gfv, images)
    button.setText(i.anime)


if __name__ == "__main__":
    run_quiz(sys.argv[1:])
