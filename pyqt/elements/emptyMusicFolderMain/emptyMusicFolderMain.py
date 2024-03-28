from PyQt6 import QtCore
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout

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
        addMusicButton = QPushButton("Dodaj piosenki")
        addMusicButton.setObjectName("add_music_button")
        addMusicButton.setStyleSheet(self.styles)
        addMusicButton.setFixedWidth(257)
        addMusicButton.setFixedHeight(33)
        addMusicButton.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        return addMusicButton

