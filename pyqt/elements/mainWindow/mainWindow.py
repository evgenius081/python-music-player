import time

from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from pyqt.elements.main.regularMain.regularMain import RegularMain
from pyqt.elements.menuBar.menuBar import MenuBar
from common.utils.files import *
from pyqt.elements.main.emptyMusicFolderMain.emptyMusicFolderMain import EmptyMusicFolderMain


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yahul's player")
        self.setFixedWidth(config.WINDOW_WIDTH)
        self.setFixedHeight(config.WINDOW_HEIGHT)
        with open("./pyqt/elements/mainWindow/mainWindow.css", "r") as file:
            self._styles = file.read()
        self.setStyleSheet(self._styles)
        self._layout = None
        self._main_widget = None
        self._empty_music_folder_main = None
        self._regular_main = None
        self._central_widget = None
        self._create_UI()

    def _create_UI(self):
        self._central_widget = QWidget()
        self._layout = QVBoxLayout()
        self._layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._central_widget.setLayout(self._layout)
        self.setCentralWidget(self._central_widget)
        self._create_menu_bar()
        self._create_main_part()

    def _create_menu_bar(self):
        menu_bar = MenuBar(self, self.refresh)
        self.setMenuBar(menu_bar)

    def _create_main_part(self):
        if is_folder_empty(config.MUSIC_ABSOLUTE_PATH):
            self._create_empty_main()
        else:
            self._create_regular_main()

    def _create_empty_main(self):
        self._empty_music_folder_main = EmptyMusicFolderMain(self.refresh)
        self._layout.addWidget(self._empty_music_folder_main)
        self._main_widget = self._empty_music_folder_main
        self.adjustSize()

    def _create_regular_main(self):
        self._regular_main = RegularMain()
        self._layout.addWidget(self._regular_main)
        self._main_widget = self._regular_main
        self.adjustSize()

    @pyqtSlot()
    def refresh(self):
        if not is_folder_empty(config.MUSIC_ABSOLUTE_PATH) and self._main_widget == self._empty_music_folder_main:
            self._regular_main = RegularMain()
            self._layout.removeWidget(self._main_widget)
            self._layout.addWidget(self._regular_main)
            self._main_widget = self._regular_main
            self._empty_music_folder_main = None
        elif is_folder_empty(config.MUSIC_ABSOLUTE_PATH) and self._main_widget == self._regular_main:
            self._empty_music_folder_main = EmptyMusicFolderMain(self.refresh)
            self._layout.removeWidget(self._main_widget)
            self._layout.addWidget(self._empty_music_folder_main)
            self._main_widget = self._empty_music_folder_main
            self._regular_main = None


