#  Copyright (c) 2023 Piotr Masek
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
from pathlib import Path

import sqlalchemy as db
import sqlalchemy.orm as orm
from PyQt6 import QtWidgets
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap, QFont, QColor, QShortcut, QKeySequence

from backend.classes.image import Image
from graphics_view import GraphicsView

DEFAULT_TIMEOUT = 30
DATA_DIR = Path('data')


# TODO: create an independent class
def _create_db_session() -> orm.Session:
    db_path = DATA_DIR / 'anime365.sqlite'
    engine = db.create_engine('sqlite:///' + str(db_path), echo=True)
    session_maker = db.orm.sessionmaker(engine)
    Image.metadata.create_all(engine)
    db_session = session_maker()
    return db_session


class Quiz:
    def __init__(self, data_source: orm.Session, data_dir: Path):
        self._db_session = data_source
        self._data_dir = data_dir

        self._images: list[Image] = []
        self._shown_images: list[Image] = []
        self._current_image_index = -1
        self._app = QtWidgets.QApplication(sys.argv)
        self._window = QtWidgets.QWidget()
        self._graphics_view = GraphicsView(self._window)

        self._timer = QTimer()
        self._timeout_seconds = DEFAULT_TIMEOUT
        self._timer_text = None

    def _start_gui(self):
        vertical_layout = QtWidgets.QVBoxLayout(self._window)
        self.show_random_image()
        vertical_layout.addWidget(self._graphics_view)

        buttons_layout = QtWidgets.QHBoxLayout(self._window)
        vertical_layout.addLayout(buttons_layout)

        button_previous = QtWidgets.QPushButton(self._window)
        button_previous.setText('Previous')
        button_previous.setShortcut(Qt.Key.Key_Left)
        button_previous.clicked.connect(lambda: self._on_click_previous())
        buttons_layout.addWidget(button_previous)

        button_answer = QtWidgets.QPushButton(self._window)
        button_answer.setText('Answer')
        button_answer.setShortcut(Qt.Key.Key_Return)
        button_answer.clicked.connect(lambda: self._on_click_answer())
        buttons_layout.addWidget(button_answer)

        button_next = QtWidgets.QPushButton(self._window)
        button_next.setText('Next')
        button_next.setShortcut(Qt.Key.Key_Right)
        button_next.clicked.connect(lambda: self._on_click_next())
        buttons_layout.addWidget(button_next)

        delete_shortcut = QShortcut(QKeySequence.StandardKey.Delete, self._window)
        # noinspection PyUnresolvedReferences
        delete_shortcut.activated.connect(self.delete_current_image)

        self._window.setMinimumSize(800, 600)
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
        img_path = str(self._data_dir / 'img' / img.file_name)
        if not os.path.exists(img_path):
            print(f"File doesn't exists: {img_path}. Skipping.")
            return

        date = datetime.fromtimestamp(img.timestamp).date()
        self._window.setWindowTitle(f'Date: {date.day}/{date.month}'
                                    + f' | Question #{str(len(self._shown_images))} | {str(len(self._images))} left')

        pix = QPixmap(str(self._data_dir / 'img' / img.file_name))
        self._graphics_view.setPixmap(pix)
        self.start_timer()

    def show_random_image(self):
        img = random.choice(self._images)
        self._current_image_index += 1
        self.show_image(img)

        self._shown_images.append(img)
        self._images.remove(img)

        img.used = True
        self._db_session.commit()

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

    def delete_current_image(self):
        self._db_session.delete(self._shown_images[self._current_image_index])
        self._db_session.commit()

    def on_timeout(self):
        if self._timeout_seconds > 0:
            self._timeout_seconds -= 1
            self._update_timer_text()

    def _update_timer_text(self):
        scene = self._graphics_view.scene()
        font = QFont()
        font.setPointSize(48)
        scene.removeItem(self._timer_text)
        self._timer_text = scene.addText(f"{self._timeout_seconds}", font)
        self._timer_text.setDefaultTextColor(QColor('yellow'))

    def start_timer(self):
        self._timeout_seconds = DEFAULT_TIMEOUT
        self._update_timer_text()

        self._timer = QTimer()
        # noinspection PyUnresolvedReferences
        self._timer.timeout.connect(self.on_timeout)
        self._timer.start(1000)

    def run(self):
        self._images = self._db_session.query(Image).filter_by(used=False).all()
        if len(self._images) == 0:
            raise Exception('No valid images loaded. Maybe all are used up?')
        self._start_gui()
        sys.exit(self._app.exec())


if __name__ == "__main__":
    with _create_db_session() as session:
        Quiz(data_source=session, data_dir=DATA_DIR).run()
