import sys

from PyQt5.QtCore import Qt, QRectF, QPointF, QPoint, QRect
from PyQt5.QtGui import QBrush, QPainterPath, QPainter, QColor, QPen, QPixmap, QMouseEvent, QFont
from PyQt5.QtWidgets import QGraphicsRectItem, QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QLabel, \
    QMainWindow, QWidget, QInputDialog


class GraphicsRectItem(QGraphicsRectItem):

    handleTopLeft = 1
    handleTopMiddle = 2
    handleTopRight = 3
    handleMiddleLeft = 4
    handleMiddleRight = 5
    handleBottomLeft = 6
    handleBottomMiddle = 7
    handleBottomRight = 8

    handleCursors = {
        handleTopLeft: Qt.SizeFDiagCursor,
        handleTopMiddle: Qt.SizeVerCursor,
        handleTopRight: Qt.SizeBDiagCursor,
        handleMiddleLeft: Qt.SizeHorCursor,
        handleMiddleRight: Qt.SizeHorCursor,
        handleBottomLeft: Qt.SizeBDiagCursor,
        handleBottomMiddle: Qt.SizeVerCursor,
        handleBottomRight: Qt.SizeFDiagCursor,
    }

    def __init__(self, *args):
        """
        Initialize the shape.
        """
        super().__init__(*args)
        self.handles = {}
        self.handleSize = +10.0
        self.handleSpace = -5.0
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.updateHandlesPos()
        self.enter = False
        self.begin = QPointF()
        self.end = QPointF()
        self.text = ""
        self.bblist = []

    def handleAt(self, point):
        """
        Returns the resize handle below the given point.
        """
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None

    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        self.enter = True
        if self.isSelected():
            handle = self.handleAt(moveEvent.pos())
            self.handleSelected = handle
            cursor = Qt.ArrowCursor if handle is None else self.handleCursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        self.enter = False
        self.handleSelected = None
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """
        self.begin = self.mapToScene(mouseEvent.pos())
        self.handleSelected = self.handleAt(mouseEvent.pos())
        if self.handleSelected:
            self.mousePressPos = mouseEvent.pos()
            self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)

    def mouseDoubleClickEvent(self, event):
        text, ok = QInputDialog().getText(QWidget(), '添加Label', '输入label:')
        if text != "":
            self.text = text
        print(self.save_box())

    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        self.end = self.mapToScene(mouseEvent.pos())
        if self.handleSelected is not None:
            self.interactiveResize(mouseEvent.pos())
        else:
            super().mouseMoveEvent(mouseEvent)


    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is released from the item.
        """
        self.end = self.mapToScene(mouseEvent.pos())
        super().mouseReleaseEvent(mouseEvent)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.update()

    def boundingRect(self):
        """
        Returns the bounding rect of the shape (including the resize handles).
        """
        o = self.handleSize + self.handleSpace
        return self.rect().adjusted(-o, -o, o, o)

    def getBeginpos(self):
        return self.begin

    def getEndpos(self):
        return self.end

    def updateHandlesPos(self):
        """
        Update current resize handles according to the shape size and position.
        """
        s = self.handleSize
        b = self.boundingRect()
        self.handles[self.handleTopLeft] = QRectF(b.left(), b.top(), s, s)
        self.handles[self.handleTopMiddle] = QRectF(b.center().x() - s / 2, b.top(), s, s)
        self.handles[self.handleTopRight] = QRectF(b.right() - s, b.top(), s, s)
        self.handles[self.handleMiddleLeft] = QRectF(b.left(), b.center().y() - s / 2, s, s)
        self.handles[self.handleMiddleRight] = QRectF(b.right() - s, b.center().y() - s / 2, s, s)
        self.handles[self.handleBottomLeft] = QRectF(b.left(), b.bottom() - s, s, s)
        self.handles[self.handleBottomMiddle] = QRectF(b.center().x() - s / 2, b.bottom() - s, s, s)
        self.handles[self.handleBottomRight] = QRectF(b.right() - s, b.bottom() - s, s, s)

    def interactiveResize(self, mousePos):
        """
        Perform shape interactive resize.
        """
        offset = self.handleSize + self.handleSpace
        boundingRect = self.boundingRect()
        rect = self.rect()
        diff = QPointF(0, 0)

        self.prepareGeometryChange()

        if self.handleSelected == self.handleTopLeft:

            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setTop(toY)
            rect.setLeft(boundingRect.left() + offset)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopMiddle:

            fromY = self.mousePressRect.top()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setTop(toY)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setTop(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleLeft:

            fromX = self.mousePressRect.left()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setLeft(toX)
            rect.setLeft(boundingRect.left() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleRight:
            print("MR")
            fromX = self.mousePressRect.right()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setRight(toX)
            rect.setRight(boundingRect.right() - offset)
            self.setRect(rect)


        elif self.handleSelected == self.handleBottomLeft:

            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setBottom(toY)
            rect.setLeft(boundingRect.left() + offset)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomMiddle:

            fromY = self.mousePressRect.bottom()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setBottom(toY)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setBottom(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        self.updateHandlesPos()

    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        """
        path = QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.handles.values():
                path.addEllipse(shape)
        return path

    def savw_box(self, text):
        self.text = text
        self.save_box()
        print(self.save_box())

    def save_box(self):
        bb = [int(self.mapToScene(self.rect().topLeft()).x()), int(self.mapToScene(self.rect().topLeft()).y()), int(self.mapToScene(self.rect().bottomRight()).x()), int(self.mapToScene(self.rect().bottomRight()).y()), self.text]
        #bb = [int((self.rect().topLeft()).x()), int((self.rect().topLeft()).y()), int((self.rect().bottomRight()).x()), int((self.rect().bottomRight()).y()), self.text]
        return bb

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """
        if self.isSelected() or self.enter:
            painter.setBrush(QBrush(QColor(135, 206, 250, 40)))
        painter.setPen(QPen(QColor(0, 255, 0), 1.0, Qt.SolidLine))
        painter.drawRect(self.rect())
        painter.setPen(QPen(QColor(255, 0, 0), 1.0, Qt.SolidLine))
        font = QFont()
        font.setPointSize(15)
        painter.setFont(font)
        painter.drawText(self.rect().topLeft().x()+5, self.rect().topLeft().y()+15, self.text)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
        painter.setPen(QPen(QColor(0, 255, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        if self.handleSelected is None:
            for handle, rect in self.handles.items():
                    painter.drawEllipse(rect)
        elif self.handleSelected is not None:
            for handle, rect in self.handles.items():
                if handle == self.handleSelected:
                    painter.setBrush(QBrush(QColor(0, 255, 0, 255)))
                    painter.drawRect(rect)
                else:
                    painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
                    painter.drawEllipse(rect)







'''
    def mousePressEvent(self, event):
        if self.create:
            self.begin = event.scenePos()
            self.end = event.scenePos()
            self._current_rect = QGraphicsRectItem()
            self._current_rect.setBrush(QColor(0, 255, 0, 100))
            self.addItem(self._current_rect)
            r = QRectF(self.begin, self.end)
            self._current_rect.setRect(r)
            print(self.begin, self.end)
            self.i = True
            self.update()

        #super(GraphicScene, self).mousePressEvent()

    def mouseMoveEvent(self, event):
        if self.i:
            self.end = event.scenePos()
            #print(self.begin, self.end)
            r = QRectF(self.begin, self.end)
            self._current_rect.setRect(r)
            self.update()

        #super(GraphicScene, self).mouseMoveEvent()

    def mouseReleaseEvent(self, event):
        if self._current_rect is not None:
            self.removeItem(self._current_rect)
            self._current_rect = None
        #print(self.begin, self.end)
        self.create = False
        self.update()
        #self.shape(self.begin.x(),self.begin.y(), self.end.x(), self.end.y())
        #super(GraphicScene, self).mouseReleaseEvent()
'''

'''
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        #self.resize(1100, 850)
        self.list = []
        self.c_list = []
        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene()
        self.view.setGeometry(QRect(0, 0, 1100, 850))
        self.setCentralWidget(self.view)
        self.view.setScene(self.scene)
        self.scene.addPixmap(QPixmap("/Users/ray/Desktop/robot-vision_final_porject/image/1.jpg").scaledToWidth(500))
        item1 = GraphicsRectItem(0, 0, 300, 150)
        #item1.savw_box("xx")
        self.scene.addItem(item1)
        self.list.append(item1)
        self.c_list.append(item1.save_box())
        item2 = GraphicsRectItem(100, 100, 300, 150)
        item2.savw_box("yy1")
        self.scene.addItem(item2)
        self.list.append(item2)
        self.c_list.append(item2.save_box())
        self.show()
        for item in self.list:
            if item.save_box() in self.c_list:
                print(2)
            else:
                print(1)



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(640, 480)
    sys.exit(app.exec_())
'''

