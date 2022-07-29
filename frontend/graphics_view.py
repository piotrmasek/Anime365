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
from PyQt6 import QtWidgets, QtGui, QtCore


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
