import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


FREE_STATE = 1
BUILDING_SQUARE = 2
BEGIN_SIDE_EDIT = 3
BEGIN_SIDE_EDIT_x = 31
END_SIDE_EDIT = 4
END_SIDE_EDIT_x = 41
FREE_STATE_rt = 12
FREE_STATE_rb = 22
FREE_STATE_lt = 32
FREE_STATE_lb = 42


CURSOR_ON_BEGIN_SIDE = 1
CURSOR_ON_END_SIDE = 2
CURSOR_ON_BEGIN_SIDE_x = 11
CURSOR_ON_END_SIDE_x = 21
CURSOR_ON_BEGIN_SIDE_rt = 3
CURSOR_ON_BEGIN_SIDE_rb = 31
CURSOR_ON_BEGIN_SIDE_lt = 4
CURSOR_ON_BEGIN_SIDE_lb = 41


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(30, 30, 600, 400)
        self.begin = QPoint()
        self.end = QPoint()
        self.delta = QPoint()
        self.canvas = True
        self.state = FREE_STATE
        self._initial_pos = QPoint()
        self.setMouseTracking(True)
        self.free_cursor_on_side = 0
        self._initial_flag = False
        self.flag = False

    def paintEvent(self, event):
        if self.canvas or not self.canvas:
            qp = QPainter(self)
            if self.flag:
                br = QBrush(QColor(135, 206, 250, 40))
                qp.setBrush(br)
            self._rect = QRect(self.begin, self.end)
            print(self._rect.topLeft(), self.begin, self._rect.bottomRight(), self.end)
            qp.drawRect(self._rect)
            qp.setPen(QPen(QColor(135, 206, 250), 6))

            qp.drawPoint(self.begin)
            qp.drawPoint(self.end)
            qp.drawPoint(self.begin.x(), self.end.y())
            qp.drawPoint(self.end.x(), self.begin.y())

            end_right = QPoint(self.end)
            end_right.setX(self.begin.x())
            end_right.setY(self.begin.y() + (self.end.y() - self.begin.y())/2 + 2.5)
            begin_right = QPoint(self.begin)
            begin_right.setY(self.begin.y() + (self.end.y() - self.begin.y())/2 - 2.5)
            qp.drawLine(begin_right, end_right)

            end_left = QPoint(self.end)
            end_left.setY(self.begin.y() + (self.end.y() - self.begin.y())/2 + 2.5)
            begin_left = QPoint(self.begin)
            begin_left.setX(self.end.x())
            begin_left.setY(self.begin.y() + (self.end.y() - self.begin.y())/2 - 2.5)
            qp.drawLine(begin_left, end_left)

            end_top = QPoint(self.end)
            end_top.setY(self.begin.y())
            end_top.setX(self.begin.x() + (self.end.x() - self.begin.x())/2 + 2.5)
            begin_top = QPoint(self.begin)
            begin_top.setX(self.begin.x() + (self.end.x() - self.begin.x())/2 + 2.5)
            qp.drawLine(begin_top, end_top)

            end_button = QPoint(self.end)
            end_button.setX(self.begin.x() + (self.end.x() - self.begin.x())/2 + 2.5)
            begin_button = QPoint(self.begin)
            begin_button.setY(self.end.y())
            begin_button.setX(self.begin.x() + (self.end.x() - self.begin.x())/2 + 2.5)
            qp.drawLine(begin_button, end_button)


    def cursor_on_side(self, e_pos) -> int:
        if not self.begin.isNull() and not self.end.isNull():
            y1, y2 = sorted([self.begin.y(), self.end.y()])
            if y1 <= e_pos.y() <= y2:

                # 5 resolution, more easy to pick than 1px
                if abs(self.begin.x() - e_pos.x()) <= 9 and abs((self.begin.y() + (self.end.y() - self.begin.y())/2)- e_pos.y()) <= 9:
                    return CURSOR_ON_BEGIN_SIDE
                elif abs(self.end.x() - e_pos.x()) <= 9 and abs((self.begin.y() + (self.end.y() - self.begin.y())/2)- e_pos.y()) <= 9:
                    return CURSOR_ON_END_SIDE
            x1, x2 = sorted([self.begin.x(), self.end.x()])
            if x1 <= e_pos.x() <= x2:
                # 3 resolution, more easy to pick than 1px
                if abs(self.begin.y() - e_pos.y()) <= 9 and abs((self.begin.x() + (self.end.x() - self.begin.x())/2) - e_pos.x()) <= 9:
                    return CURSOR_ON_BEGIN_SIDE_x
                elif abs(self.end.y() - e_pos.y()) <= 9 and abs((self.begin.x() + (self.end.x() - self.begin.x())/2) - e_pos.x()) <= 9:
                    return CURSOR_ON_END_SIDE_x
            if abs(self.begin.y() - e_pos.y()) <= 9 and abs(self.begin.x() - e_pos.x()) <= 9:
                return CURSOR_ON_BEGIN_SIDE_rt
            elif abs(self.begin.y() - e_pos.y()) <= 9 and abs(self.end.x() - e_pos.x()) <= 9:
                return CURSOR_ON_BEGIN_SIDE_lt
            elif abs(self.end.y() - e_pos.y()) <= 9 and abs(self.begin.x() - e_pos.x()) <= 9:
                return CURSOR_ON_BEGIN_SIDE_rb
            elif abs(self.end.y() - e_pos.y()) <= 9 and abs(self.end.x() - e_pos.x()) <= 9:
                return CURSOR_ON_BEGIN_SIDE_lb

        return 0

    def mousePressEvent(self, event):
        if self.canvas or not self.canvas:
            side = self.cursor_on_side(event.pos())
            if side == CURSOR_ON_BEGIN_SIDE:
                self.state = BEGIN_SIDE_EDIT
            elif side == CURSOR_ON_END_SIDE:
                self.state = END_SIDE_EDIT
            elif side == CURSOR_ON_BEGIN_SIDE_x:
                self.state = BEGIN_SIDE_EDIT_x
            elif side == CURSOR_ON_END_SIDE_x:
                self.state = END_SIDE_EDIT_x
            elif side == CURSOR_ON_BEGIN_SIDE_rt:
                self.state = FREE_STATE_rt
            elif side == CURSOR_ON_BEGIN_SIDE_rb:
                self.state = FREE_STATE_rb
            elif side == CURSOR_ON_BEGIN_SIDE_lt:
                self.state = FREE_STATE_lt
            elif side == CURSOR_ON_BEGIN_SIDE_lb:
                self.state = FREE_STATE_lb
            else:
                self.state = BUILDING_SQUARE
                self.begin = event.pos()
                self.end = event.pos()
                self.update()
        if not self.canvas and self._rect.contains(event.pos()):

            self.setCursor(QCursor(Qt.OpenHandCursor))
            self._initial_flag = True
            self._initial_pos = event.pos()
        if self._rect.contains(event.pos()):
            self.flag = True
        else:
            self.flag = False
        super(MyWidget, self).mousePressEvent(event)

    def applye_event(self, event):

        if self.state == BUILDING_SQUARE:
            self.end = event.pos()
        elif self.state == BEGIN_SIDE_EDIT:
            self.begin.setX(event.x())
        elif self.state == END_SIDE_EDIT:
            self.end.setX(event.x())
        elif self.state == BEGIN_SIDE_EDIT_x:
            self.begin.setY(event.y())
        elif self.state == END_SIDE_EDIT_x:
            self.end.setY(event.y())
        elif self.state == FREE_STATE_rt:
            self.begin.setY(event.y())
            self.begin.setX(event.x())
        elif self.state == FREE_STATE_rb:
            self.end.setY(event.y())
            self.begin.setX(event.x())
        elif self.state == FREE_STATE_lt:
            self.end.setX(event.x())
            self.begin.setY(event.y())
        elif self.state == FREE_STATE_lb:
            self.end.setY(event.y())
            self.end.setX(event.x())

    def mouseMoveEvent(self, event):
        if self._initial_flag:
            self.delta = event.pos() - self._initial_pos
            self.begin += self.delta
            self.end += self.delta
            self._initial_pos = event.pos()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            self.update()

        if self.state == FREE_STATE:
            self.free_cursor_on_side = self.cursor_on_side(event.pos())
            if self.free_cursor_on_side==CURSOR_ON_BEGIN_SIDE or self.free_cursor_on_side==CURSOR_ON_END_SIDE:
                self.setCursor(Qt.SizeHorCursor)
            elif self.free_cursor_on_side==CURSOR_ON_BEGIN_SIDE_x or self.free_cursor_on_side==CURSOR_ON_END_SIDE_x:
                self.setCursor(Qt.SizeVerCursor)
            elif self.free_cursor_on_side==CURSOR_ON_BEGIN_SIDE_rt or self.free_cursor_on_side==CURSOR_ON_BEGIN_SIDE_lb:
                if self.end.x()<self.begin.x():
                    if self.end.y()<self.begin.y():
                        self.setCursor(Qt.SizeFDiagCursor)
                    else:
                        self.setCursor(Qt.SizeBDiagCursor)
                elif self.end.y()<self.begin.y():
                    self.setCursor(Qt.SizeBDiagCursor)
                else:
                    self.setCursor(Qt.SizeFDiagCursor)
            elif self.free_cursor_on_side==CURSOR_ON_BEGIN_SIDE_lt or self.free_cursor_on_side==CURSOR_ON_BEGIN_SIDE_rb:
                if self.end.x()<self.begin.x():
                    if self.end.y()<self.begin.y():
                        self.setCursor(Qt.SizeBDiagCursor)
                    else:
                        self.setCursor(Qt.SizeFDiagCursor)
                elif self.end.y()<self.begin.y():
                    self.setCursor(Qt.SizeFDiagCursor)
                else:
                    self.setCursor(Qt.SizeBDiagCursor)
            else:
                self.unsetCursor()
            self.update()
        else:
            self.applye_event(event)
            self.update()
        if self._rect.contains(event.pos()):
            self.flag = True
        else:
            self.flag = False

        super(MyWidget, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        #self.applye_event(event)
        self.state = FREE_STATE
        self.canvas = False
        self._initial_flag = False
        QApplication.restoreOverrideCursor()
        super(MyWidget, self).mouseReleaseEvent(event)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())
