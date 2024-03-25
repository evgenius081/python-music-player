from PyQt6.QtWidgets import QMainWindow
import config
from pyqt.elements.menuBar.menuBar import MenuBar
import os


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yahul's player")
        self.setFixedWidth(config.WINDOW_WIDTH)
        self.setFixedHeight(config.WINDOW_HEIGHT)
        print(os.getcwd())
        with open("./pyqt/elements/mainWindow/mainWindow.css", "r") as file:
            self.styles = file.read()
        self.setStyleSheet(self.styles)
        self._createMenuBar()
        self._createMainPart()

    def _createMenuBar(self):
        menuBar = MenuBar(self)
        self.setMenuBar(menuBar)

    def _createMainPart(self):
        if self._isMusicFolderEmpty():
            self._createEmptyMain()
        else:
            self._createMainWithControls()

    def _isMusicFolderEmpty(self):
        pass

    def _createEmptyMain(self):
        pass

    def _createMainWithControls(self):
        pass

