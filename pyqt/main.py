from PyQt6.QtWidgets import QApplication
import config
import os
import sys
from pyqt.elements.mainWindow.mainWindow import MainWindow

app = QApplication(sys.argv)
with open("pyqt/main.css", "r") as file:
    styles = file.read()

app.setStyleSheet(styles)

if not os.path.exists(config.MUSIC_ABSOLUTE_PATH):
    os.makedirs(config.MUSIC_ABSOLUTE_PATH)

window = MainWindow()
window.show()
app.exec()
