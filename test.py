# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/ray/Desktop/Auto_labelimg/build_gui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import sys
import os
import filetype
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QListWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import QImageReader, QImage, QColor

from PyQt5.QtWidgets import QAction
app_name = "Auto labelimg"
FREE_STATE = 1
BUILDING_SQUARE = 2
BEGIN_SIDE_EDIT = 3
END_SIDE_EDIT = 4

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.setWindowTitle(app_name)
        self.file_checked = False
        self.save_checked = False
        self.annotation_save_path = ''
        self.begin = QPoint()
        self.end = QPoint()
        self.state = FREE_STATE

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1100, 1000))
        # problem unsolve:image does show on the center
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBar.setBaseSize(QtCore.QSize(0, 0))
        self.toolBar.setToolTipDuration(-1)
        self.toolBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toolBar.setAutoFillBackground(False)
        self.toolBar.setMovable(True)
        self.toolBar.setIconSize(QtCore.QSize(40, 40))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("SSD/icons/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen_Dir = QtWidgets.QAction(MainWindow)
        self.actionOpen_Dir.setIcon(icon)
        self.actionOpen_Dir.setObjectName("actionOpen_Dir")
        self.actionChange_Save_Dir = QtWidgets.QAction(MainWindow)
        self.actionChange_Save_Dir.setIcon(icon)
        self.actionChange_Save_Dir.setObjectName("actionChange_Save_Dir")
        self.actionNext = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("SSD/icons/next (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNext.setIcon(icon1)
        self.actionNext.setObjectName("actionNext")
        self.actionPrev = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("SSD/icons/previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrev.setIcon(icon2)
        self.actionPrev.setObjectName("actionPrev")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("SSD/icons/diskette.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon3)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setIcon(icon3)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionClose = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("SSD/icons/cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClose.setIcon(icon4)
        self.actionClose.setObjectName("actionClose")
        self.actionOpen_Annotation = QtWidgets.QAction(MainWindow)
        self.actionOpen_Annotation.setCheckable(False)
        self.actionOpen_Annotation.setChecked(False)
        self.actionOpen_Annotation.setIcon(icon)
        self.actionOpen_Annotation.setObjectName("actionOpen_Annotation")
        self.actionCreate_BounderBox = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("SSD/icons/page.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCreate_BounderBox.setIcon(icon5)
        self.actionCreate_BounderBox.setObjectName("actionCreate_BounderBox")
        self.actionDuplicate_BounderBOx = QtWidgets.QAction(MainWindow)
        self.actionDuplicate_BounderBOx.setObjectName("actionDuplicate_BounderBOx")
        self.actionDelete_BounderBox = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("SSD/icons/bin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete_BounderBox.setIcon(icon6)
        self.actionDelete_BounderBox.setObjectName("actionDelete_BounderBox")
        self.actionBox_Line_Color = QtWidgets.QAction(MainWindow)
        self.actionBox_Line_Color.setObjectName("actionBox_Line_Color")
        self.actionEdit_Label = QtWidgets.QAction(MainWindow)
        self.actionEdit_Label.setObjectName("actionEdit_Label")
        self.actionAute_Label = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("SSD/icons/label.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAute_Label.setIcon(icon7)
        self.actionAute_Label.setObjectName("actionAute_Label")
        self.actionImage_Quality_Estimater = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("SSD/icons/estimation.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionImage_Quality_Estimater.setIcon(icon8)
        self.actionImage_Quality_Estimater.setObjectName("actionImage_Quality_Estimater")
        self.actionAuto_Save_Mode = QtWidgets.QAction(MainWindow)
        self.actionAuto_Save_Mode.setObjectName("actionAuto_Save_Mode")
        self.actionDisplay_Label = QtWidgets.QAction(MainWindow)
        self.actionDisplay_Label.setObjectName("actionDisplay_Label")
        self.actionZoom_in = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("SSD/icons/zoom-in.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_in.setIcon(icon9)
        self.actionZoom_in.setObjectName("actionZoom_in")
        self.actionZoom_out = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("SSD/icons/magnifying-glass.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_out.setIcon(icon10)
        self.actionZoom_out.setObjectName("actionZoom_out")
        self.actionOriginal_Size = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("SSD/icons/expand.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOriginal_Size.setIcon(icon11)
        self.actionOriginal_Size.setObjectName("actionOriginal_Size")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionOpen_Dir)
        self.menuFile.addAction(self.actionChange_Save_Dir)
        self.menuFile.addAction(self.actionOpen_Annotation)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addAction(self.actionClose)
        self.menuEdit.addAction(self.actionCreate_BounderBox)
        self.menuEdit.addAction(self.actionDuplicate_BounderBOx)
        self.menuEdit.addAction(self.actionDelete_BounderBox)
        self.menuEdit.addAction(self.actionBox_Line_Color)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionEdit_Label)
        self.menuEdit.addAction(self.actionAute_Label)
        self.menuEdit.addAction(self.actionImage_Quality_Estimater)
        self.menuView.addAction(self.actionAuto_Save_Mode)
        self.menuView.addAction(self.actionDisplay_Label)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionZoom_in)
        self.menuView.addAction(self.actionZoom_out)
        self.menuView.addAction(self.actionOriginal_Size)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionOpen_Dir)
        self.toolBar.addAction(self.actionChange_Save_Dir)
        self.toolBar.addAction(self.actionPrev)
        self.toolBar.addAction(self.actionNext)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionCreate_BounderBox)
        self.toolBar.addAction(self.actionDelete_BounderBox)
        self.toolBar.addAction(self.actionClose)
        self.toolBar.addAction(self.actionZoom_in)
        self.toolBar.addAction(self.actionZoom_out)
        self.toolBar.addAction(self.actionOriginal_Size)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionAute_Label)
        self.toolBar.addAction(self.actionImage_Quality_Estimater)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        self.actionOpen.triggered.connect(lambda: self.open_file())
        self.actionOpen_Dir.triggered.connect(lambda: self.open_directory())
        self.actionChange_Save_Dir.triggered.connect(lambda: self.change_annotation_save_path())
        self.actionOpen_Annotation.triggered.connect(lambda: self.open_file())
        self.actionSave.triggered.connect(lambda: self.open_file())
        self.actionSave_as.triggered.connect(lambda: self.open_file())
        self.actionClose.triggered.connect(lambda: self.open_file())
        self.actionCreate_BounderBox.triggered.connect(lambda: self.open_file())
        self.actionDuplicate_BounderBOx.triggered.connect(lambda: self.open_file())
        self.actionDelete_BounderBox.triggered.connect(lambda: self.open_file())
        self.actionBox_Line_Color.triggered.connect(lambda: self.open_file())
        self.actionEdit_Label.triggered.connect(lambda: self.open_file())
        self.actionAute_Label.triggered.connect(lambda: self.open_file())
        self.actionImage_Quality_Estimater.triggered.connect(lambda: self.open_file())
        self.actionAuto_Save_Mode.triggered.connect(lambda: self.open_file())
        self.actionDisplay_Label.triggered.connect(lambda: self.open_file())
        self.actionZoom_in.triggered.connect(lambda: self.zoom_in())
        self.actionZoom_out.triggered.connect(lambda: self.zoom_out())
        self.actionOriginal_Size.triggered.connect(lambda: self.fit_window())
        self.actionPrev.triggered.connect(lambda: self.prev_image())
        self.actionNext.triggered.connect(lambda: self.next_image())





    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen_Dir.setText(_translate("MainWindow", "Open Dir"))
        self.actionChange_Save_Dir.setText(_translate("MainWindow", "Change Save Dir"))
        self.actionNext.setText(_translate("MainWindow", "Next"))
        self.actionPrev.setText(_translate("MainWindow", "Prev"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionOpen_Annotation.setText(_translate("MainWindow", "Open Annotation"))
        self.actionCreate_BounderBox.setText(_translate("MainWindow", "Create BounderBox"))
        self.actionDuplicate_BounderBOx.setText(_translate("MainWindow", "Duplicate BounderBox"))
        self.actionDelete_BounderBox.setText(_translate("MainWindow", "Delete BounderBox"))
        self.actionBox_Line_Color.setText(_translate("MainWindow", "Box Line Color"))
        self.actionEdit_Label.setText(_translate("MainWindow", "Edit Label"))
        self.actionAute_Label.setText(_translate("MainWindow", "Auto Label"))
        self.actionImage_Quality_Estimater.setText(_translate("MainWindow", "Image Quality Estimater"))
        self.actionAuto_Save_Mode.setText(_translate("MainWindow", "Auto Save Mode"))
        self.actionDisplay_Label.setText(_translate("MainWindow", "Display Label"))
        self.actionZoom_in.setText(_translate("MainWindow", "Zoom in"))
        self.actionZoom_out.setText(_translate("MainWindow", "Zoom out"))
        self.actionOriginal_Size.setText(_translate("MainWindow", "Original Size"))

    def open_file(self):
        self.file_checked = False
        filename = QFileDialog.getOpenFileName(self, 'Choose Image or Label file', "", "Jpg Files(*.jpg)")
        if filename:
            self.show_image(filename[0])

    def open_directory(self, dir_path=None):
        self.file_checked = True
        # Proceeding next image without dialog if having any label
        default_open_dir_path = dir_path if dir_path else ''
        self.chose_dir_path = QFileDialog.getExistingDirectory(self, 'Open Directory', default_open_dir_path, QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.images_list = []
        self.list_index = 0
        files = os.listdir(self.chose_dir_path)
        for file in files:
            if not os.path.isdir(file):
                kind = filetype.guess(self.chose_dir_path + '/' + file)
                if kind != None:
                    if kind.mime == 'image/jpeg':
                        print(file)
                        alert = True
                        self.images_list.append(file)
                    else:
                        alert = False
                        break
            else:
                alert = False
                break
        if alert == True:
            self.show_image(self.chose_dir_path +'/' + self.images_list[self.list_index])
            self.last_open_dir = dir_path
        else:
            self.show_image("SSD/icons/bin.png")

    def zoom_in(self):
        self.width *= 1.25
        self.resize_image()

    def zoom_out(self):
        self.width *= 0.75
        self.resize_image()
    def fit_window(self):
        self.width = 1100
        self.resize_image()

    def resize_image(self):
        scaled_pixmap = self.pixmap.scaledToWidth(self.width)
        self.label.setPixmap(scaled_pixmap)

    def show_image(self, path):
        self.pixmap = QPixmap(path)
        self.width = self.pixmap.width()
        self.label.setPixmap(self.pixmap.scaledToWidth(1100))

    def next_image(self):
        if self.file_checked:
            self.list_index += 1
            self.show_image(self.chose_dir_path +'/' + self.images_list[self.list_index])
        else:
            return

    def prev_image(self):
        if self.file_checked:
            if (self.list_index-1) >= 0:
                self.list_index -= 1
                self.show_image(self.chose_dir_path +'/' + self.images_list[self.list_index])
            else:
                return
        else:
            return

    def change_annotation_save_path(self, annotation_dir_path=None):
        default_annotation_dir_path = annotation_dir_path if annotation_dir_path else ''
        self.annotation_save_path = QFileDialog.getExistingDirectory(self, 'Open Directory', default_annotation_dir_path, QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.annotation_save_path = annotation_dir_path

    def save_annotation(self):
        return

    def paintEvent(self, event):
        painter = QPainter(self)
        brush_color = QBrush(QColor(100, 10, 10, 40))
        painter.setBrush(brush_color)
        painter.drawPixmap(QPoint(), self.pixmap)
        if not self.begin.isNull() and not self.end.isNull():
            painter.drawRect(QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        if not self.begin.isNull() and not self.end.isNull():
            Pos = event.pos()
            y1, y2 = sorted([self.begin.y(), self.end.y()])
            if y1 <= Pos.y() <= y2:
                if abs(self.begin.x() - Pos.x()) <= 10:
                    self.state = BEGIN_SIDE_EDIT
                elif abs(self.end.x() - Pos.x()) <= 10:
                    self.state = END_SIDE_EDIT
        self.state = BUILDING_SQUARE

        self.begin = event.pos()
        self.end = event.pos()
        self.update()

    def applye_event(self, event):
        if self.state == BUILDING_SQUARE:
            self.end = event.pos()
        elif self.state == BEGIN_SIDE_EDIT:
            self.begin.setX(event.x())
        elif self.state == END_SIDE_EDIT:
            self.end.setX(event.x())

    def mouseMoveEvent(self, event):
        self.applye_event(event)
        self.update()

    def mouseReleaseEvent(self, event):
        self.applye_event(event)
        self.state = FREE_STATE








if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

