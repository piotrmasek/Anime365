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
import random
import sys
from datetime import datetime
from pathlib import Path

import sqlalchemy as db
import sqlalchemy.orm
from PyQt6 import QtWidgets
from PyQt6.QtGui import QPixmap

from backend.classes.image import Image
from graphics_view import GraphicsView
from PyQt6 import QtWidgets, QtGui, QtCore


# TODO: save shown_images, maybe improve scaling
class Quiz:
    def __init__(self, data_dir: Path = Path('data')):
        self._data_dir = data_dir
        self._db_session = self._create_db_session()

        self._images: list[Image] = []
        self._shown_images: list[Image] = []
        self._current_image_index = -1

        self._app = QtWidgets.QApplication(sys.argv)
        self._window = QtWidgets.QWidget()
        self._graphics_view = GraphicsView(self._window)

    def _create_db_session(self):
        db_path = self._data_dir / 'anime365.sqlite'
        engine = db.create_engine('sqlite:///' + str(db_path))
        session_maker = db.orm.sessionmaker(engine)
        Image.metadata.create_all(engine)
        db_session = session_maker()
        return db_session

    def _start_gui(self):
        vertical_layout = QtWidgets.QVBoxLayout(self._window)
        self.show_random_image()
        vertical_layout.addWidget(self._graphics_view)

        buttons_layout = QtWidgets.QHBoxLayout(self._window)
        vertical_layout.addLayout(buttons_layout)

        button_previous = QtWidgets.QPushButton(self._window)
        button_previous.setText('Previous')
        button_previous.setShortcut(QtGui.QKeySequence.StandardKey.Back)
        button_previous.clicked.connect(lambda: self._on_click_previous())
        buttons_layout.addWidget(button_previous)

        button_answer = QtWidgets.QPushButton(self._window)
        button_answer.setText('Answer')
        button_answer.setShortcut(QtGui.QKeySequence.StandardKey.Delete)
        button_answer.clicked.connect(lambda: self._on_click_answer())
        buttons_layout.addWidget(button_answer)

        button_next = QtWidgets.QPushButton(self._window)
        button_next.setText('Next')
        button_next.setShortcut(QtGui.QKeySequence.StandardKey.Forward)
        button_next.clicked.connect(lambda: self._on_click_next())
        buttons_layout.addWidget(button_next)

        self._window.setMinimumSize(1280, 720)
        self._window.show()

    def _on_click_next(self):
        if self._current_image_index < (len(self._shown_images) - 1):
            self.show_next_image()
        else:
            self.show_random_image()

    def _on_click_answer(self):
        QtWidgets.QMessageBox.information(self._window, 'The answer is', self._shown_images[self._current_image_index]
                                          .anime)

    def _on_click_previous(self):
        if self._current_image_index > 0:
            self.show_previous_image()

    ###################################################################################################
    # Interface
    ###################################################################################################
    def show_image(self, img: Image):
        self._window.setWindowTitle(str(datetime.fromtimestamp(img.timestamp).date()))

        pix = QPixmap(str(self._data_dir / 'img' / img.file_name))
        self._graphics_view.setPixmap(pix)

    def show_random_image(self):
        img = random.choice(self._images)
        self._current_image_index += 1
        self.show_image(img)
        self._shown_images.append(img)
        self._images.remove(img)

    def show_previous_image(self):
        if self._current_image_index < 1:
            return
        self._current_image_index -= 1
        self.show_image(self._shown_images[self._current_image_index])

    def show_next_image(self):
        if self._current_image_index >= len(self._shown_images):
            return
        self._current_image_index += 1
        self.show_image(self._shown_images[self._current_image_index])

    def run(self):
        self._images = self._db_session.query(Image).all()
        self._start_gui()
        sys.exit(self._app.exec())


if __name__ == "__main__":
    Quiz().run()
