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
from datetime import datetime

import sqlalchemy as db
import sqlalchemy.orm
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6 import QtWidgets
from PyQt6.QtGui import QPixmap

from backend.classes.image import Image


# TODO: just make it a class, divide into more methods, save shown_images
class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)
        scene = QtWidgets.QGraphicsScene(self)
        self.setScene(scene)
        self.m_pixmap_item = self.scene().addPixmap(QtGui.QPixmap())

    def setPixmap(self, pixmap):
        self.m_pixmap_item.setPixmap(pixmap)
        self.fitInView(self.m_pixmap_item, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.scene().setSceneRect(self.m_pixmap_item.boundingRect())

    def resizeEvent(self, event):
        if not self.m_pixmap_item.pixmap().isNull():
            self.fitInView(self.m_pixmap_item, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        super(GraphicsView, self).resizeEvent(event)


images = [Image]
shown_images = [Image]
current_image_index = 0
images_dir: os.path = 'data/img/'
graphics_view: GraphicsView
window: QtWidgets.QWidget


def show_random_image():
    img = random.choice(images)
    global window
    window.setWindowTitle(str(datetime.fromtimestamp(img.timestamp).date()))
    pix = QPixmap(os.path.join(images_dir, img.file_name))

    global graphics_view
    graphics_view.setPixmap(pix)
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
    global window
    window = QtWidgets.QWidget()

    window.setWindowTitle('Anime365')

    vertical_layout = QtWidgets.QVBoxLayout(window)

    global graphics_view
    graphics_view = GraphicsView()
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
    QtWidgets.QMessageBox.information(window, 'The answer is', shown_images[current_image_index].anime)


def on_click_previous():
    global current_image_index
    if current_image_index > 0:
        show_previous_image()


def show_previous_image():
    global current_image_index
    current_image_index -= 1
    img = shown_images[current_image_index]
    window.setWindowTitle(str(datetime.fromtimestamp(img.timestamp).date()))
    pix = QPixmap(os.path.join(images_dir, img.file_name))
    graphics_view.setPixmap(pix)


def show_next_image():
    global current_image_index
    current_image_index += 1
    img = shown_images[current_image_index]
    window.setWindowTitle(str(datetime.fromtimestamp(img.timestamp).date()))
    pix = QPixmap(os.path.join(images_dir, img.file_name))
    graphics_view.setPixmap(pix)


if __name__ == "__main__":
    run_quiz()
