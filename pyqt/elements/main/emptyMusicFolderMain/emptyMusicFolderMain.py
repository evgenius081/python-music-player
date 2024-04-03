from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog

from common.utils.files import clone_file
import config


class EmptyMusicFolderMain(QWidget):
    refresh_signal = pyqtSignal()

    def __init__(self, refresh_slot):
        super().__init__()
        self.styles = None
        with open("./pyqt/elements/main/emptyMusicFolderMain/emptyMusicFolderMain.css", "r") as file:
            self.styles = file.read()
        self.setFixedWidth(config.WINDOW_WIDTH)
        self.setFixedHeight(config.WINDOW_HEIGHT-60)
        self.setObjectName("empty_music_folder_main")
        self.refresh_signal.connect(refresh_slot)
        self.layout = None
        self.empty_folder_label = None
        self.add_music_button = None
        self._create_UI()

    def _create_UI(self):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self._create_label()
        self._create_add_button()

    def _create_label(self):
        self.empty_folder_label = QLabel('Brak dodanych piosenek')
        self.empty_folder_label.setObjectName("empty_music_folder_label")
        self.empty_folder_label.setStyleSheet(self.styles)
        self.empty_folder_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.empty_folder_label.setFixedHeight(80)
        self.layout.addWidget(self.empty_folder_label)

    def _create_add_button(self):
        self.add_music_button = QPushButton("Dodaj piosenki")
        self.add_music_button.setObjectName("add_music_button")
        self.add_music_button.setStyleSheet(self.styles)
        self.add_music_button.setFixedWidth(257)
        self.add_music_button.setFixedHeight(33)
        self.add_music_button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.add_music_button.clicked.connect(self._add_music_files_action)
        self.layout.addWidget(self.add_music_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

    def _add_music_files_action(self):
        file_filter = " ".join(map(lambda s: f"*.{s}", config.music_file_formats))
        file_dialog = QFileDialog.getOpenFileNames(self, "Select audio files", "", file_filter)
        filenames = file_dialog[0]
        for filename in filenames:
            clone_file(filename, config.MUSIC_ABSOLUTE_PATH)\

        if len(filenames) > 0:
            self.refresh_signal.emit()
