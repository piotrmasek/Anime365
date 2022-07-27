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

# TODO: just make it a class, divide into more methods, save shown_images, fit images to window
images = []
shown_images = []
current_image_index = 0
images_dir: os.path = 'data/img/'
graphics_view: QtWidgets.QGraphicsView


def show_random_image():
    img = random.choice(images)

    pix = QPixmap(os.path.join(images_dir, img.file_name))
    item = QtWidgets.QGraphicsPixmapItem(pix)

    global graphics_view
    graphics_view.scene().clear()
    graphics_view.scene().addItem(item)

    global current_image_index
    global shown_images
    current_image_index = len(shown_images)
    shown_images.append(img)
    images.remove(img)


def run_quiz():
    engine = db.create_engine('sqlite:///data/anime365.sqlite')
    session_maker = db.orm.sessionmaker(engine)
    Image.metadata.create_all(engine)
    db_session = session_maker()

    global images
    images = db_session.query(Image).all()

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()

    window.setWindowTitle('Anime365')

    vertical_layout = QtWidgets.QVBoxLayout(window)

    global graphics_view
    graphics_view = QtWidgets.QGraphicsView(window)
    scene = QtWidgets.QGraphicsScene(graphics_view)
    graphics_view.setScene(scene)
    show_random_image()
    vertical_layout.addWidget(graphics_view)

    buttons_layout = QtWidgets.QHBoxLayout(window)
    vertical_layout.addLayout(buttons_layout)

    button_previous = QtWidgets.QPushButton(window)
    button_previous.setText('Previous')
    button_previous.clicked.connect(lambda: on_click_previous())
    buttons_layout.addWidget(button_previous)

    button_answer = QtWidgets.QPushButton(window)
    button_answer.setText('Answer')
    button_answer.clicked.connect(lambda: on_click_answer(window))
    buttons_layout.addWidget(button_answer)

    button_next = QtWidgets.QPushButton(window)
    button_next.setText('Next')
    button_next.clicked.connect(lambda: on_click_next())
    buttons_layout.addWidget(button_next)

    window.showMaximized()

    sys.exit(app.exec())


def on_click_next():
    if current_image_index < (len(shown_images) - 1):
        show_next_image()
    else:
        show_random_image()


def on_click_answer(window):
    QtWidgets.QMessageBox.information(window, 'Answer is', shown_images[current_image_index].anime)


def on_click_previous():
    global current_image_index
    if current_image_index > 0:
        show_previous_image()


def show_previous_image():
    global current_image_index
    current_image_index -= 1
    img = shown_images[current_image_index]
    pix = QPixmap(os.path.join(images_dir, img.file_name))
    item = QtWidgets.QGraphicsPixmapItem(pix)
    graphics_view.scene().clear()
    graphics_view.scene().addItem(item)


def show_next_image():
    global current_image_index
    current_image_index += 1
    img = shown_images[current_image_index]
    pix = QPixmap(os.path.join(images_dir, img.file_name))
    item = QtWidgets.QGraphicsPixmapItem(pix)
    graphics_view.scene().clear()
    graphics_view.scene().addItem(item)


if __name__ == "__main__":
    run_quiz()
