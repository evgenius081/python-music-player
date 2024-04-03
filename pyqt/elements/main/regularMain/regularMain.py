from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QVBoxLayout
import config
from pyqt.elements.main.regularMain.songList.songList import MusicList


class RegularMain(QWidget):
    def __init__(self):
        super().__init__()
        self._styles = ""
        with open("./pyqt/elements/main/regularMain/regularMain.css", "r") as file:
            self._styles = file.read()
        self.setFixedWidth(config.WINDOW_WIDTH)
        self.setFixedHeight(config.WINDOW_HEIGHT-60)
        self.setObjectName("regular_main")
        self._layout = None
        self._controls = None
        self._music_list = None
        self._create_UI()

    def _create_UI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)
        # self._controls = Controls(self)
        self._music_list = MusicList(self)
        # self._layout.addWidget(self._controls)
        self._layout.addWidget(self._music_list)


