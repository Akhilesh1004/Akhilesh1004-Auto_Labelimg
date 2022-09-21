import sys
import os
import filetype
import xml.sax
import cv2
from bounderbox import GraphicsRectItem
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QListWidget, QMessageBox, QDialog
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5 import QtTest
from pascal import PascalVOC, PascalObject, BndBox, size_block
from pathlib import Path
from image_detect import detect


app_name = "Auto labelimg"
FREE_STATE = 1
BUILDING_SQUARE = 2
BEGIN_SIDE_EDIT = 3
BEGIN_SIDE_EDIT_x = 31
END_SIDE_EDIT = 4
END_SIDE_EDIT_x = 41


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QGraphicsView(self)
        self.scene = QGraphicsScene()
        self.label.setScene(self.scene)
        self.label.setGeometry(QtCore.QRect(0, 0, 1100, 850))
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
        icon.addPixmap(QtGui.QPixmap("/Users/ray/Desktop/Auto_labelimg/SSD/icons/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        icon1.addPixmap(QtGui.QPixmap("/Users/ray/Desktop/Auto_labelimg/SSD/icons/next (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNext.setIcon(icon1)
        self.actionNext.setObjectName("actionNext")
        self.actionPrev = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("/Users/ray/Desktop/Auto_labelimg/SSD/icons/previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrev.setIcon(icon2)
        self.actionPrev.setObjectName("actionPrev")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("/Users/ray/Desktop/Auto_labelimg/SSD/icons/diskette.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon3)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setIcon(icon3)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionClose = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("/Users/ray/Desktop/Auto_labelimg/SSD/icons/cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClose.setIcon(icon4)
        self.actionClose.setObjectName("actionClose")
        self.actionOpen_Annotation = QtWidgets.QAction(MainWindow)
        self.actionOpen_Annotation.setCheckable(False)
        self.actionOpen_Annotation.setChecked(False)
        self.actionOpen_Annotation.setIcon(icon)
        self.actionOpen_Annotation.setObjectName("actionOpen_Annotation")
        self.actionCreate_BounderBox = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("/Users/ray/Desktop/Auto_labelimg/SSD/icons/page.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCreate_BounderBox.setIcon(icon5)
        self.actionCreate_BounderBox.setObjectName("actionCreate_BounderBox")
        self.actionDuplicate_BounderBOx = QtWidgets.QAction(MainWindow)
        self.actionDuplicate_BounderBOx.setObjectName("actionDuplicate_BounderBOx")
        self.actionDelete_BounderBox = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("/Users/ray/Desktop/Auto_labelimg/SSD/icons/bin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete_BounderBox.setIcon(icon6)
        self.actionDelete_BounderBox.setObjectName("actionDelete_BounderBox")
        self.actionBox_Line_Color = QtWidgets.QAction(MainWindow)
        self.actionBox_Line_Color.setObjectName("actionBox_Line_Color")
        self.actionEdit_Label = QtWidgets.QAction(MainWindow)
        self.actionEdit_Label.setObjectName("actionEdit_Label")
        self.actionAute_Label = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("/Users/ray/Desktop/Auto_labelimg/SSD/icons/label.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAute_Label.setIcon(icon7)
        self.actionAute_Label.setObjectName("actionAute_Label")
        self.actionImage_Quality_Estimater = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("/Users/ray/Desktop/Auto_labelimg/SSD/icons/estimation.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionImage_Quality_Estimater.setIcon(icon8)
        self.actionImage_Quality_Estimater.setObjectName("actionImage_Quality_Estimater")
        self.actionAuto_Save_Mode = QtWidgets.QAction(MainWindow)
        self.actionAuto_Save_Mode.setObjectName("actionAuto_Save_Mode")
        self.actionDisplay_Label = QtWidgets.QAction(MainWindow)
        self.actionDisplay_Label.setObjectName("actionDisplay_Label")
        self.actionZoom_in = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("/Users/ray/Desktop/Auto_labelimg/SSD/icons/zoom-in.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_in.setIcon(icon9)
        self.actionZoom_in.setObjectName("actionZoom_in")
        self.actionZoom_out = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("/Users/ray/Desktop/Auto_labelimg/SSD/icons/magnifying-glass.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_out.setIcon(icon10)
        self.actionZoom_out.setObjectName("actionZoom_out")
        self.actionOriginal_Size = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("/Users/ray/Desktop/Auto_labelimg/SSD/icons/expand.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        #self.label.setText(_translate("MainWindow", "TextLabel"))
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
        self.actionAbout.setText(_translate("MainWindow", "About"))



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.run = False
        self.setUpMainUiFunction()
        self.begin = QPoint()
        self.end = QPoint()
        self.state = FREE_STATE
        self.pixmap = QPixmap("/Users/ray/Desktop/Auto_labelimg/SSD/icons/cancel.png")
        self.rects = []
        self.last_open_dir = None
        self.annotation_save_path = None
        self.flag = False
        self.auto_label_check = False
        self.open_annotation_file = False
        self.object_list = []
        self.annotation_list = []
        self.images_list = []
        self.list_index = 0
        self.progress_check_ = False
        self.pb = ProgressBar()
        self.pb.mysignal.connect(lambda: self.auto_label_processing())
        self.pb.mysignal2.connect(lambda: self.auto_label_stop())
        self.pb.mysignal3.connect(lambda: self.auto_label_continue())


    def setUpMainUiFunction(self):
        self.actionOpen.triggered.connect(lambda: self.open_file())
        self.actionOpen_Dir.triggered.connect(lambda: self.open_directory())
        self.actionChange_Save_Dir.triggered.connect(lambda: self.change_annotation_save_path())
        self.actionOpen_Annotation.triggered.connect(lambda: self.open_annotation())
        self.actionSave.triggered.connect(lambda: self.save_annotation())
        self.actionSave_as.triggered.connect(lambda: self.open_file())
        self.actionClose.triggered.connect(QCoreApplication.instance().quit)
        self.actionCreate_BounderBox.triggered.connect(lambda: self.create_bnd())
        self.actionDuplicate_BounderBOx.triggered.connect(lambda: self.open_file())
        self.actionDelete_BounderBox.triggered.connect(lambda: self.remove_boundbox())
        self.actionBox_Line_Color.triggered.connect(lambda: self.open_file())
        self.actionEdit_Label.triggered.connect(lambda: self.open_file())
        self.actionAute_Label.triggered.connect(lambda: self.auto_label())
        self.actionImage_Quality_Estimater.triggered.connect(lambda: self.open_file())
        self.actionAuto_Save_Mode.triggered.connect(lambda: self.open_file())
        self.actionDisplay_Label.triggered.connect(lambda: self.open_file())
        self.actionZoom_in.triggered.connect(lambda: self.zoom_in())
        self.actionZoom_out.triggered.connect(lambda: self.zoom_out())
        self.actionOriginal_Size.triggered.connect(lambda: self.fit_window())
        self.actionPrev.triggered.connect(lambda: self.prev_image())
        self.actionNext.triggered.connect(lambda: self.next_image())

    def open_file(self):
        self.file_checked = False
        alert = False
        self.images_list = []

        self.filename, filetype = QFileDialog.getOpenFileName(self, 'Choose Image or Label file', "", "Jpg Files(*.jpg)")
        if self.filename:
            try:
                self.object_list = []
                self.chek_list = []
                print(self.filename)
                print(os.path.basename(self.filename))
                print(os.path.dirname(self.filename))
                self.scene.clear()
                self.show_image(self.filename)
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'The following error occurred:\n{type(e)}: {e}')
                return
        else:
            return

    def open_annotation(self, annotation_path = None):
        # Proceeding next image without dialog if having any label
        annotation_path = self.annotation_save_path
        default_open_annotation_path = annotation_path if annotation_path else ''
        if len(self.annotation_list)>len(self.images_list):
            QMessageBox.warning(self, 'Warning', 'Object not fit')
        if self.auto_label_check == False:
            self.chose_annotation_path = QFileDialog.getExistingDirectory(self, 'Open Directory', default_open_annotation_path, QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if not self.chose_annotation_path:
            return
        try:
            self.object_list = []
            self.chek_list = []
            self.annotation_list = []
            self.open_annotation_file = True
            files = os.listdir(self.chose_annotation_path)
            files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(self.chose_annotation_path, x)))
            for file in files:
                if not os.path.isdir(file):
                    kind = self.getType(self.chose_annotation_path + '/' + file)
                    if kind != None:
                        if kind == 'xml':
                            print(file)
                            alert = True
                            self.annotation_list.append(file)
                        else:
                            alert = False
                            break
                else:
                    alert = False
                    break
            if alert == True and self.file_checked == True:
                print(self.chose_annotation_path +'/' + self.annotation_list[self.list_index])
                self.load_annotation(self.chose_annotation_path +'/' + self.annotation_list[self.list_index])
                self.annotation_save_path = self.chose_annotation_path

            else:
                self.show_image("icons/bin.png")
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'The following error occurred:\n{type(e)}: {e}')
            return


    def open_directory(self, dir_path = None):
        self.file_checked = True
        dir_path = self.last_open_dir
        # Proceeding next image without dialog if having any label
        default_open_dir_path = dir_path if dir_path else ''
        self.chose_dir_path = QFileDialog.getExistingDirectory(self, 'Open Directory', default_open_dir_path, QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if not self.chose_dir_path:
            return
        try:
            self.object_list = []
            self.chek_list = []
            self.images_list = []
            self.list_index = 0
            files = os.listdir(self.chose_dir_path)
            files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(self.chose_dir_path, x)))
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
                self.scene.clear()
                self.show_image(self.chose_dir_path +'/' + self.images_list[self.list_index])
                self.last_open_dir = self.chose_dir_path
            else:
                self.scene.clear()
                self.show_image("/Users/ray/Desktop/Auto_labelimg/SSD/icons/bin.png")
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'The following error occurred:\n{type(e)}: {e}')
            return


    def zoom_in(self):
        scale_tr = QTransform()
        scale_tr.scale(1.15, 1.15)

        tr = self.label.transform() * scale_tr
        self.label.setTransform(tr)

    def zoom_out(self):
        scale_tr = QTransform()
        scale_tr.scale(0.85, 0.85)

        tr = self.label.transform() * scale_tr
        self.label.setTransform(tr)

    def fit_window(self):
        self.label.setTransform(QTransform())

    def show_image(self, path):
        self.pixmap = QPixmap(path)
        self.scene.addPixmap(self.pixmap)
        img = cv2.imread(path)
        self.h, self.w, self.c = img.shape

    def next_image(self):
        self.object_list = []
        self.chek_list = []
        if self.file_checked:
            if self.annotation_list != []:
                if (self.list_index+1) < len(self.annotation_list) and (self.list_index+1) < len(self.images_list):
                    self.check_annotation()
                    self.scene.clear()
                    self.list_index += 1
                    self.show_image(self.chose_dir_path +'/' + self.images_list[self.list_index])
                    self.load_annotation(self.chose_annotation_path +'/' + self.annotation_list[self.list_index])
                elif (self.list_index+1) < len(self.images_list):
                    self.check_annotation()
                    self.scene.clear()
                    self.list_index += 1
                    self.show_image(self.chose_dir_path +'/' + self.images_list[self.list_index])
                else:
                    return
            else:
                if (self.list_index+1) < len(self.images_list):
                    self.check_annotation()
                    self.scene.clear()
                    self.list_index += 1
                    self.show_image(self.chose_dir_path +'/' + self.images_list[self.list_index])
                else:
                    return
        else:
            return

    def prev_image(self):
        self.object_list = []
        self.chek_list = []
        if self.file_checked:
            if (self.list_index-1) >= 0:
                if self.annotation_list != []:
                    if (self.list_index) < len(self.annotation_list) and (self.list_index) < len(self.images_list):
                        self.check_annotation()
                        self.scene.clear()
                        self.list_index -= 1
                        self.show_image(self.chose_dir_path +'/' + self.images_list[self.list_index])
                        self.load_annotation(self.chose_annotation_path +'/' + self.annotation_list[self.list_index])
                    elif 0 <= (self.list_index-1) < len(self.annotation_list) and 0 <= (self.list_index-1) < len(self.images_list):
                        self.check_annotation()
                        self.scene.clear()
                        self.list_index -= 1
                        self.show_image(self.chose_dir_path +'/' + self.images_list[self.list_index])
                        self.load_annotation(self.chose_annotation_path +'/' + self.annotation_list[self.list_index])
                    elif (self.list_index) < len(self.images_list):
                        self.check_annotation()
                        self.scene.clear()
                        self.list_index -= 1
                        self.show_image(self.chose_dir_path +'/' + self.images_list[self.list_index])
                    else:
                        return
                else:
                    if (self.list_index) < len(self.images_list):
                        self.check_annotation()
                        self.scene.clear()
                        self.list_index -= 1
                        self.show_image(self.chose_dir_path +'/' + self.images_list[self.list_index])
                    else:
                        return
            else:
                return
        else:
            return
    def change_annotation_save_path(self, annotation_dir_path = None):
        annotation_dir_path = self.annotation_save_path
        default_annotation_dir_path = annotation_dir_path if annotation_dir_path else ''
        annotation_save_path = QFileDialog.getExistingDirectory(self, 'Open Directory', default_annotation_dir_path, QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.annotation_save_path = annotation_save_path
        QMessageBox.information(self, 'Info', 'Change Save Path Successfully')


    def getType(self, file):
      with open(file, 'rb') as fh:
        try:
          xml.sax.parse(fh, xml.sax.ContentHandler())
          return 'xml'
        except: # SAX' exceptions are not public
          return None

    def load_annotation(self, annotation_path):
        self.object_list = []
        self.chek_list = []
        ann = PascalVOC.from_xml(annotation_path)
        for obj in ann.objects:
            item = GraphicsRectItem(obj.bndbox.xmin, obj.bndbox.ymin, obj.bndbox.xmax-obj.bndbox.xmin, obj.bndbox.ymax-obj.bndbox.ymin)
            item.savw_box(obj.name)
            self.scene.addItem(item)
            self.object_list.append(item)
            self.chek_list.append(item.save_box())

    def save_annotation(self):
        list_obj = []
        if self.annotation_save_path != None:
            if len(self.object_list)!=0:
                for item in self.object_list:
                    i = item.save_box()
                    obj = PascalObject(i[4], "Unspecified", truncated=False, difficult=False, bndbox=BndBox(i[0], i[1], i[2], i[3]))
                    list_obj.append(obj)
                pascal_ann = PascalVOC(self.images_list[self.list_index], size=size_block(self.w, self.h, self.c), objects=list_obj, path=self.chose_dir_path +'/' + self.images_list[self.list_index], folder=os.path.basename(self.chose_dir_path))
                pascal_ann.save(self.annotation_save_path+'/' + Path(self.images_list[self.list_index]).stem + '.xml')
                if self.auto_label_check == False:
                    QMessageBox.information(self, 'Info', 'Save Successfully')
                self.save_check = True
            else:
                QMessageBox.warning(self, 'Warning', 'No object to save')
        elif self.filename:
            if len(self.object_list)!=0:
                for item in self.object_list:
                    i = item.save_box()
                    obj = PascalObject(i[4], "Unspecified", truncated=False, difficult=False, bndbox=BndBox(i[0], i[1], i[2], i[3]))
                    list_obj.append(obj)
                pascal_ann = PascalVOC(os.path.basename(self.filename), size=size_block(self.w, self.h, self.c), objects=list_obj, path=self.filename, folder=os.path.basename(os.path.dirname(self.filename)))
                pascal_ann.save(os.path.dirname(self.filename)+'/' + Path(os.path.basename(self.filename)).stem + '.xml')
                if self.auto_label_check == False:
                    QMessageBox.information(self, 'Info', 'Save Successfully')
                self.save_check = True
            else:
                QMessageBox.warning(self, 'Warning', 'No object to save')
        else:
            QMessageBox.warning(self, 'Warning', 'Choose path to save annotation')
            self.change_annotation_save_path()

    def check_annotation(self):
        try:
            if len(self.object_list)!=0:
                for item in self.object_list:
                    i = item.save_box()
                    if i in self.chek_list or self.save_check == True:
                        self.save_check = False
                    else:
                        QMessageBox.warning(self, 'Warning', 'Please save before you leave')
            else:
                return
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'The following error occurred:\n{type(e)}: {e}')
            return

    def remove_boundbox(self):
        try:
            item = self.scene.selectedItems()
            print(item[0])
            self.scene.removeItem(item[0])
            self.object_list.remove(item[0])
            self.chek_list.remove(item[0].save_box())
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'The following error occurred:\n{type(e)}: {e}')
            return

    def create_bnd(self):
        x1 = self.h/2 - 25
        y1 = self.w/2 - 25
        item = GraphicsRectItem(x1, y1, 50, 50)
        self.scene.addItem(item)
        self.object_list.append(item)

    def auto_label(self):
        self.auto_label_check = True
        self.list_index = 0
        self.scene.clear()
        self.show_image(self.chose_dir_path +'/' + self.images_list[self.list_index])
        if self.annotation_save_path != None:
            self.pb.pbar.setMaximum(len(self.images_list))
            self.pb.label.setText(str(self.list_index)+"/"+str(len(self.images_list)))
            self.pb.show()
        else:
            QMessageBox.warning(self, 'Warning', 'Choose path to save annotation')
            self.change_annotation_save_path()

    def auto_label_stop(self):
        self.scene.clear()
        self.show_image(self.chose_dir_path +'/' + self.images_list[self.list_index])
        self.chose_annotation_path = self.annotation_save_path
        self.open_annotation()
        self.auto_label_check = False

    def auto_label_continue(self):
        self.auto_label_check = True


    def auto_label_processing(self):
        self.object_list = []
        self.chek_list = []
        img = cv2.imread(self.chose_dir_path +'/' + self.images_list[self.list_index])
        items = detect(img)
        for p in items:
            item = GraphicsRectItem(p[0], p[1], p[2]-p[0], p[3]-p[1])
            item.savw_box(p[4])
            self.scene.addItem(item)
            self.object_list.append(item)
            self.chek_list.append(item.save_box())
        self.save_annotation()
        self.pb.label.setText(str(self.list_index+1)+"/"+str(len(self.images_list)))
        self.pb.pbar.setValue(self.list_index+1)
        QtTest.QTest.qWait(500)
        if len(self.images_list)-1 == self.list_index:
            self.scene.clear()
            self.show_image(self.chose_dir_path +'/' + self.images_list[self.list_index])
            self.pb.timer.stop()
            self.pb.close()
            QMessageBox.information(self, 'Info', 'Auto Labeling Done')
            self.chose_annotation_path = self.annotation_save_path
            self.open_annotation()
            self.auto_label_check = False
        self.next_image()
        QtTest.QTest.qWait(100)

    def progress_check(self):
        if self.progress_check_ == False:
            self.progress_check_ = True
        else:
            self.progress_check_ = False


class ProgressBar(QDialog):
    mysignal = pyqtSignal()
    mysignal2 = pyqtSignal()
    mysignal3 = pyqtSignal()
    def __init__(self, parent= None):
        QDialog.__init__(self)
        self.step = 0
        self.setGeometry(400, 400, 250, 150)
        self.setWindowTitle('ProgressBar')
        self.Layout = QVBoxLayout()
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.Layout.addWidget(self.pbar)
        self.label = QLabel(self)
        self.label.setGeometry(70, 65,100, 100)
        self.label.setAlignment(Qt.AlignHCenter)
        self.Layout.addWidget(self.label)
        #self.label.move(100, 60)

        self.button = QPushButton('  Start  ', self)
        self.button.setFocusPolicy(Qt.NoFocus)
        self.button.move(85, 80)
        #self.Layout.addWidget(self.button)

        self.button.clicked.connect(self.onStart)
        self.timer = QBasicTimer()

    def timerEvent(self, event):
        QtTest.QTest.qWait(100)
        self.mysignal.emit()

    def check(self):
        if self.button.text() == 'Continue' and self.x == 0:
            print(33)
            self.mysignal2.emit()
            self.x = 1
        elif self.button.text() == '  Stop  ' and self.x == 1:
            self.mysignal3.emit()

    def onStart(self):
        if self.timer.isActive():
            self.timer.stop()
            self.button.setText('Continue')
            self.x = 0
            self.check()
        else:
            self.timer.start(100, self)
            self.button.setText('  Stop  ')
            self.check()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())

