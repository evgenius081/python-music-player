from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from pyqt.elements.main.regularMain.regularMain import RegularMain
from pyqt.elements.menuBar.menuBar import MenuBar
from common.utils.files import *
from pyqt.elements.main.emptyMusicFolderMain.emptyMusicFolderMain import EmptyMusicFolderMain
from pyqt.mediaPlayer import MediaPlayer


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Odtwarzacz")
        self.setFixedWidth(config.WINDOW_WIDTH)
        self.setFixedHeight(config.WINDOW_HEIGHT)
        self.setContentsMargins(0, 0, 0, 0)
        with open("./pyqt/elements/mainWindow/mainWindow.css", "r") as file:
            self.__styles = file.read()
        self.setStyleSheet(self.__styles)
        self.__main_widget = None
        self.__empty_music_folder_main = None
        self.__regular_main = None
        self.__media_player = None
        self.__create_UI()

    def __create_UI(self):
        self.__central_widget = QWidget()
        self.__central_widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.__central_widget)

        self.__layout = QVBoxLayout()
        self.__layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__central_widget.setLayout(self.__layout)

        self.__create_menu_bar()
        self.__create_main_part()

    def __create_menu_bar(self):
        self.__menu_bar = MenuBar()
        self.__menu_bar.songs_added.connect(self.__songs_added)
        self.setMenuBar(self.__menu_bar)

    def __create_main_part(self):
        if is_folder_empty(config.MUSIC_FOLDER_PATH):
            self.__create_empty_main()
        else:
            self.__create_regular_main()

    def __create_empty_main(self):
        self.__empty_music_folder_main = EmptyMusicFolderMain()
        self.__empty_music_folder_main.songs_added.connect(self.__songs_added)
        self.__layout.addWidget(self.__empty_music_folder_main)
        self.__main_widget = self.__empty_music_folder_main
        self.adjustSize()

    def __create_regular_main(self):
        self.__media_player = MediaPlayer()
        self.__menu_bar.set_media_player(self.__media_player)
        self.__regular_main = RegularMain(self.__media_player)
        self.__layout.addWidget(self.__regular_main)
        self.__main_widget = self.__regular_main
        self.adjustSize()

    def __songs_added(self):
        if not is_folder_empty(config.MUSIC_FOLDER_PATH) and self.__main_widget == self.__empty_music_folder_main:
            self.__layout.removeWidget(self.__main_widget)
            self.__create_regular_main()
            self.__empty_music_folder_main = None
        else:
            self.__media_player.add_new_songs()

