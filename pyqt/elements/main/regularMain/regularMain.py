from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QVBoxLayout
import config
from pyqt.elements.main.regularMain.controls.controls import Controls
from pyqt.elements.main.regularMain.songList.songList import SongList

LAYOUT_SPACING = 15


class RegularMain(QWidget):
    def __init__(self, media_player):
        super().__init__()
        self._styles = ""
        with open("./pyqt/elements/main/regularMain/regularMain.css", "r") as file:
            self._styles = file.read()
        self.setFixedWidth(config.WINDOW_WIDTH)
        self.setFixedHeight(config.WINDOW_HEIGHT - config.MENU_BAR_HEIGHT)
        self.setContentsMargins(0, 0, 0, 0)
        self.__media_player = media_player
        self.setObjectName("regular_main")
        self.__create_UI()

    def __create_UI(self):
        self.__layout = QVBoxLayout()
        self.__layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)
        self.__layout.setSpacing(LAYOUT_SPACING)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.__layout)

        self.__music_list = SongList(self.__media_player)
        self.__layout.addWidget(self.__music_list)

        self.__controls = Controls(self.__media_player)
        self.__layout.addWidget(self.__controls)

