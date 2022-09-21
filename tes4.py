from PyQt5.QtWidgets import QApplication, QProgressBar, QPushButton, QLabel, QVBoxLayout, QMessageBox, QDialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5 import QtTest

class ProgressBar(QDialog):
    def __init__(self,parent= None):
        QDialog.__init__(self)
        self.step = 0
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('ProgressBar')
        self.Layout = QVBoxLayout()
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.Layout.addWidget(self.pbar)
        self.label = QLabel(self)
        self.label.setGeometry(70, 65,100, 100)
        self.label.setAlignment(Qt.AlignHCenter)
        self.label.setText(str(0)+"/"+str(100))
        self.Layout.addWidget(self.label)
        #self.label.move(100, 60)

        self.button = QPushButton('Start', self)
        self.button.setFocusPolicy(Qt.NoFocus)
        self.button.move(85, 80)
        #self.Layout.addWidget(self.button)

        self.button.clicked.connect(self.onStart)
        self.timer = QBasicTimer()

    def timerEvent(self, event):
        if self.step >=100:
            self.timer.stop()
            self.close()
        self.step = self.step+1
        QtTest.QTest.qWait(500)
        self.label.setText(str(self.step)+"/"+str(1000))
        self.pbar.setValue(self.step)

    def onStart(self):
        if self.timer.isActive():
            self.timer.stop()
            self.button.setText('Start')
        else:
            self.timer.start(100, self)
            self.button.setText('Stop')


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    qb = ProgressBar()
    qb.show()
    qb.onStart()
    sys.exit(app.exec_())

