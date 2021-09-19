import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from ui import Ui_MainWindow


class Window(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon("resources/plain.ico"))

        self.pushButton.pressed.connect(self.publish)
        self.pushButton_2.pressed.connect(self.save)
        self.pushButton_3.pressed.connect(self.clear)

        font = QtGui.QFont()
        font.setPointSize(15)
        self.textEdit.setFont(font)

    def save(self):
        text = self.notepad.save()
        self.textEdit.append(text)

    def clear(self):
        self.notepad.clear()

    def publish(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "", "*.txt")

        if file_path:
            with open(file_path, "w") as f:
                f.write(str(self.textEdit.toPlainText()))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.showMaximized()
    sys.exit(app.exec())
