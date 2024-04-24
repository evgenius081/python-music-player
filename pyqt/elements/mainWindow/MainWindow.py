from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from pyqt.elements.main.regularMain.RegularMain import RegularMain
from pyqt.elements.menuBar.MenuBar import MenuBar
from common.utils.files import *
from pyqt.elements.main.emptyMusicFolderMain.EmptyMusicFolderMain import EmptyMusicFolderMain
from pyqt.MediaPlayer import MediaPlayer


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Odtwarzacz")
        self.setFixedWidth(config.WINDOW_WIDTH)
        self.setFixedHeight(config.WINDOW_HEIGHT)
        self.setContentsMargins(0, 0, 0, 0)
        with open("./pyqt/elements/mainWindow/MainWindow.css", "r") as file:
            self._styles = file.read()
        self.setStyleSheet(self._styles)
        self._main_widget = None
        self._empty_music_folder_main = None
        self._regular_main = None
        self._media_player = None
        self._create_UI()

    def _create_UI(self):
        self._central_widget = QWidget()
        self._central_widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self._central_widget)

        self._layout = QVBoxLayout()
        self._layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._central_widget.setLayout(self._layout)

        self._create_menu_bar()
        self._create_main_part()

    def _create_menu_bar(self):
        self._menu_bar = MenuBar()
        self._menu_bar.songs_added.connect(self._songs_added)
        self.setMenuBar(self._menu_bar)

    def _create_main_part(self):
        if is_folder_empty(config.MUSIC_FOLDER_PATH):
            self._create_empty_main()
        else:
            self._create_regular_main()

    def _create_empty_main(self):
        self._empty_music_folder_main = EmptyMusicFolderMain()
        self._empty_music_folder_main.songs_added.connect(self._songs_added)
        self._layout.addWidget(self._empty_music_folder_main)
        self._main_widget = self._empty_music_folder_main
        self.adjustSize()

    def _create_regular_main(self):
        self._media_player = MediaPlayer()
        self._menu_bar.set_media_player(self._media_player)
        self._regular_main = RegularMain(self._media_player)
        self._layout.addWidget(self._regular_main)
        self._main_widget = self._regular_main
        self.adjustSize()

    def _songs_added(self):
        if not is_folder_empty(config.MUSIC_FOLDER_PATH) and self._main_widget == self._empty_music_folder_main:
            self._layout.removeWidget(self._main_widget)
            self._create_regular_main()
            self._empty_music_folder_main = None
        else:
            self._media_player.add_new_songs()

