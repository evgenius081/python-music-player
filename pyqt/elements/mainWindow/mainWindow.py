from PyQt6.QtWidgets import QMainWindow

from pyqt.elements.menuBar.menuBar import MenuBar
from common.utils.files import *
from pyqt.elements.emptyMusicFolderMain.emptyMusicFolderMain import EmptyMusicFolderMain


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yahul's player")
        self.setFixedWidth(config.WINDOW_WIDTH)
        self.setFixedHeight(config.WINDOW_HEIGHT)
        with open("./pyqt/elements/mainWindow/mainWindow.css", "r") as file:
            self.styles = file.read()
        self.setStyleSheet(self.styles)
        self.mainWidget = None
        self._createMainPart()
        self._createMenuBar()

    def _createMenuBar(self):
        menuBar = MenuBar(self)
        self.setMenuBar(menuBar)

    def _createMainPart(self):
        if self._isMusicFolderEmpty():
            self._createEmptyMain()
        else:
            self._createMainWithControls()

    def _isMusicFolderEmpty(self):
        return is_folder_empty(config.MUSIC_ABSOLUTE_PATH)

    def _createEmptyMain(self):
        self.mainWidget = EmptyMusicFolderMain(self)
        self.adjustSize()

    def _createMainWithControls(self):
        pass

