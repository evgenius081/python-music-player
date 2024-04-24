from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QVBoxLayout
import config
from pyqt.elements.main.regularMain.controls.Controls import Controls
from pyqt.elements.main.regularMain.songList.SongList import SongList

LAYOUT_SPACING = 15


class RegularMain(QWidget):
    def __init__(self, media_player):
        super().__init__()
        self._styles = ""
        with open("./pyqt/elements/main/regularMain/RegularMain.css", "r") as file:
            self._styles = file.read()
        self.setFixedWidth(config.WINDOW_WIDTH)
        self.setFixedHeight(config.WINDOW_HEIGHT - config.MENU_BAR_HEIGHT)
        self.setContentsMargins(0, 0, 0, 0)
        self._media_player = media_player
        self.setObjectName("regular_main")
        self._create_UI()

    def _create_UI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)
        self._layout.setSpacing(LAYOUT_SPACING)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._music_list = SongList(self._media_player)
        self._layout.addWidget(self._music_list)

        self._controls = Controls(self._media_player)
        self._layout.addWidget(self._controls)

