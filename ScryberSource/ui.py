from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QImage
from PyQt5.QtCore import Qt, QPoint
import cv2
import pytesseract
import numpy as np

import os
import sys

if getattr(sys, 'frozen', False):
    _path = os.path.join(sys._MEIPASS, r'Tesseract-OCR\tesseract.exe')
    print(_path)
    pytesseract.pytesseract.tesseract_cmd =_path
    # the .exe will look here
else:
    pytesseract.pytesseract.tesseract_cmd = r'' # Absolute path to tesseract.exe goes here.


class NotePad(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.img_counter = 0
        self.img_list = []

        self.setWindowTitle("MLaTeX")  # Window title
        self.setGeometry(100, 100, 800, 600)  # Window size
        self.image = QImage(self.size(), QImage.Format_RGB32)  # creating image object
        self.image.fill(Qt.white)  # making image color to white
        self.drawing = False  # flag
        self.brushSize = 5
        self.brushColor = Qt.black
        self.lastPoint = QPoint()  # track point

        self.xscale = 800
        self.yscale = 600

    def mousePressEvent (self, event): # check mouse clicks
        self.drawing = True # if left button is clicked, make drawing flag due
        x = self.size().width()
        y = self.size().height()
        self.lastPoint = QPoint(event.pos().x() * self.xscale // x, event.pos().y() * self.yscale // y)

    def mouseMoveEvent(self, event): # check mouse activity
        x = self.size().width()
        y = self.size().height()
        if self.drawing: # if left button is down and drawing flag = true
            if  event.buttons() & Qt.LeftButton:
                self.brushSize = 5
                self.brushColor = Qt.black
            elif event.buttons() & Qt.RightButton:
                self.brushSize = 10
                self.brushColor = Qt.white

            painter = QPainter(self.image) # painter object creation

            painter.setPen(QPen(self.brushColor, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)) # pen painter set-up

            painter.drawLine(self.lastPoint, QPoint(event.pos().x() * self.xscale // x, event.pos().y() * self.yscale // y)) # draw line from the last point of cursor to the current point

            self.lastPoint = QPoint(event.pos().x() * self.xscale // x, event.pos().y() * self.yscale // y)   # change the last point
            self.update()

    def mouseReleaseEvent(self, event): # if left button is released, make drawing flag false and stop drawing
        self.drawing = False

    def paintEvent(self, event): #painting event
        canvasPainter = QPainter(self) #make painter
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())  # draw rectangle  on the canvas

    def clear(self):  # clearing method
        self.image.fill(Qt.white)
        self.update()

    def save(self):
        img = self.convert_qimage(self.image)
        kernel = np.ones((2, 1), np.uint8)
        img = cv2.erode(img, kernel, iterations=1)
        img = cv2.dilate(img, kernel, iterations=1)
        return pytesseract.image_to_string(img)

    @staticmethod
    def convert_qimage(incomingImage):
        '''  Converts a QImage into an opencv MAT format  '''

        incomingImage = incomingImage.convertToFormat(4)

        width = incomingImage.width()
        height = incomingImage.height()

        ptr = incomingImage.bits()
        ptr.setsize(incomingImage.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)  # Copies the data
        return arr


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(633, 478)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.img_label = QtWidgets.QLabel()
        img = QtGui.QImage(f'resources/Title.png')
        img = img.scaled(400, 100)
        pixmap = QtGui.QPixmap(img)
        self.img_label.setPixmap(pixmap)
        self.img_label.minimumSize()

        self.hbox_title = QtWidgets.QHBoxLayout()
        self.hbox_title.addWidget(self.img_label)

        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setMinimumSize(QtCore.QSize(300, 300))
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_4.addLayout(self.hbox_title)

        self.notepad = NotePad(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.notepad.sizePolicy().hasHeightForWidth())
        self.notepad.setSizePolicy(sizePolicy)
        self.notepad.setMinimumSize(QtCore.QSize(300, 300))
        self.notepad.setObjectName("notepad")
        self.verticalLayout_2.addWidget(self.notepad)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_3.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_3.addWidget(self.pushButton_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        from style import style_string

        QtGui.QFontDatabase.addApplicationFont(r'resources/fonts/Odin Rounded - Regular.otf')
        QtGui.QFontDatabase.addApplicationFont(r'resources/fonts/raleway/Raleway-Regular.ttf')

        self.centralwidget.setStyleSheet(style_string)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", " "))
        self.pushButton.setText(_translate("MainWindow", "Publish"))
        self.pushButton_2.setText(_translate("MainWindow", "Render"))
        self.pushButton_3.setText(_translate("MainWindow", "Clear"))
