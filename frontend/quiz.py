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

from PyQt6 import QtWidgets
from PyQt6.QtGui import QPixmap


def show_random_image(graphics_view: QtWidgets.QGraphicsView, images_dir: os.path):
    img = random.choice(os.listdir(images_dir))
    pix = QPixmap(os.path.join(images_dir, img))
    item = QtWidgets.QGraphicsPixmapItem(pix)
    scene = QtWidgets.QGraphicsScene(gfv)
    scene.addItem(item)
    graphics_view.setScene(scene)


images_dir: os.path = '../backend/img/'
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()

window.setWindowTitle('Anime365')

layout = QtWidgets.QVBoxLayout(window)

gfv = QtWidgets.QGraphicsView(window)
show_random_image(gfv, images_dir)
layout.addWidget(gfv)

button = QtWidgets.QPushButton(window)
button.setText('次')
button.clicked.connect(lambda: show_random_image(gfv, images_dir))
layout.addWidget(button)

window.showMaximized()
sys.exit(app.exec())
