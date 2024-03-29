from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog

from common.utils.files import clone_file
from pyqt.actions.files import addMusicFilesAction
import config


class EmptyMusicFolderMain(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        with open("./pyqt/elements/emptyMusicFolderMain/emptyMusicFolderMain.css", "r") as file:
            self.styles = file.read()
        self.setFixedWidth(config.WINDOW_WIDTH)
        self.setFixedHeight(config.WINDOW_HEIGHT-60)
        self.setObjectName("empty_music_folder_main")
        self._createLayout()

    def _createLayout(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self._getLabel())
        layout.addWidget(self._getAddButton(), alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def _getLabel(self):
        empty_folder_label = QLabel('Brak dodanych piosenek')
        empty_folder_label.setObjectName("empty_music_folder_label")
        empty_folder_label.setStyleSheet(self.styles)
        empty_folder_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        empty_folder_label.setFixedHeight(80)
        return empty_folder_label

    def _getAddButton(self):
        add_music_button = QPushButton("Dodaj piosenki")
        add_music_button.setObjectName("add_music_button")
        add_music_button.setStyleSheet(self.styles)
        add_music_button.setFixedWidth(257)
        add_music_button.setFixedHeight(33)
        add_music_button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        add_music_button.clicked.connect(self._addMusicFilesAction)
        return add_music_button

    @pyqtSlot()
    def _addMusicFilesAction(self):
        file_filter = " ".join(map(lambda s: f"*.{s}", config.music_file_formats))
        file_dialog = QFileDialog.getOpenFileNames(self, "Select audio files", "", file_filter)
        filenames = file_dialog[0]
        for filename in filenames:
            clone_file(filename, config.MUSIC_ABSOLUTE_PATH)
