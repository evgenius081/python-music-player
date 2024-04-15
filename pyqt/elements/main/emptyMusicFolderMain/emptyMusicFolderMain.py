from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog

from common.utils.files import clone_and_rename_file
import config

EMPTY_FOLDER_LABEL_HEIGHT = 80
ADD_MUSIC_BUTTON_WIDTH = 257
ADD_MUSIC_BUTTON_HEIGHT = 33


class EmptyMusicFolderMain(QWidget):
    songs_added = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__styles = None
        with open("./pyqt/elements/main/emptyMusicFolderMain/emptyMusicFolderMain.css", "r") as file:
            self.__styles = file.read()
        self.setFixedWidth(config.WINDOW_WIDTH)
        self.setFixedHeight(config.WINDOW_HEIGHT-config.MENU_BAR_HEIGHT)
        self.setObjectName("empty_music_folder_main")
        self.layout = None
        self.empty_folder_label = None
        self.add_music_button = None
        self.__create_UI()

    def __create_UI(self):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.__create_label()
        self.__create_add_button()

    def __create_label(self):
        self.empty_folder_label = QLabel('Brak dodanych piosenek')
        self.empty_folder_label.setObjectName("empty_music_folder_label")
        self.empty_folder_label.setStyleSheet(self.__styles)
        self.empty_folder_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.empty_folder_label.setFixedHeight(EMPTY_FOLDER_LABEL_HEIGHT)
        self.layout.addWidget(self.empty_folder_label)

    def _create_add_button(self):
        self.add_music_button = QPushButton("Dodaj piosenki")
        self.add_music_button.setObjectName("add_music_button")
        self.add_music_button.setStyleSheet(self.__styles)
        self.add_music_button.setFixedWidth(ADD_MUSIC_BUTTON_WIDTH)
        self.add_music_button.setFixedHeight(ADD_MUSIC_BUTTON_HEIGHT)
        self.add_music_button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.add_music_button.clicked.connect(self._add_music_files_action)
        self.layout.addWidget(self.add_music_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

    def __add_music_files_action(self):
        file_filter = " ".join(map(lambda s: f"*.{s}", config.MUSIC_FILE_FORMATS))
        file_dialog = QFileDialog.getOpenFileNames(self, "Wybierz pliki dźwiękowe", "", file_filter)
        filenames = file_dialog[0]
        for index, filename in enumerate(filenames):
            clone_and_rename_file(filename, config.MUSIC_FOLDER_PATH, index + 1)

        if len(filenames) > 0:
            self.songs_added.emit()
