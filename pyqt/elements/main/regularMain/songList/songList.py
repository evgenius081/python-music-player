from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QScrollBar

import config
from common.utils.files import get_all_audio_files
from pyqt.elements.main.regularMain.songList.song.song import Song


class MusicList(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(config.WINDOW_HEIGHT - 150)
        self.setFixedWidth(config.WINDOW_WIDTH)
        self._styles = ""
        self.setObjectName("music_list")
        with open("./pyqt/elements/main/regularMain/songList/songList.css", "r") as file:
            self._styles = file.read()
        self.setStyleSheet(self._styles)
        self._layout = None
        self._header_layout = None
        self._list_layout = None
        self._songs = get_all_audio_files(config.MUSIC_ABSOLUTE_PATH)
        self._song_widgets = []
        self._create_UI()

    def _create_UI(self):
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(85, 22, 0, 0)
        self._layout.setSpacing(0)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._create_header()
        self._create_list()

    def _create_header(self):
        self._header_layout = QHBoxLayout()
        self._header_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        self._header_layout.setContentsMargins(20, 0, 0, 15)
        self._layout.addLayout(self._header_layout)
        number_label = QLabel("#")
        number_label.setObjectName("number_label")
        title_label = QLabel("Tytuł")
        title_label.setObjectName("title_label")
        album_label = QLabel("Album")
        album_label.setObjectName("album_label")
        duration_icon = QSvgWidget("pyqt/assets/duration.svg")
        duration_icon.setObjectName("duration_icon")
        duration_icon.setFixedSize(18, 18)
        self._header_layout.addWidget(number_label)
        self._header_layout.addWidget(title_label)
        self._header_layout.addWidget(album_label)
        self._header_layout.addWidget(duration_icon)

    def _create_list(self):
        self._scroll_bar = QScrollBar()
        self._scroll_bar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(self._styles)

        self._scroll_area = QScrollArea()
        self._scroll_area.setObjectName("song_scroll")
        self._scroll_area.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._scroll_area.setContentsMargins(0, 0, 0, 0)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll_area.setVerticalScrollBar(self._scroll_bar)

        self._list_widget = QWidget()
        self._list_widget.setObjectName("song_list_widget")
        self._list_widget.setStyleSheet(self._styles)
        self._list_widget.setContentsMargins(0, 0, 0, 0)

        self._list_layout = QVBoxLayout()
        self._list_layout.setSpacing(15)
        self._list_layout.setContentsMargins(0, 0, 0, 0)
        self._list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for index, song in enumerate(self._songs):
            song_widget = Song(song, index)
            self._song_widgets.append(song_widget)
            self._list_layout.addWidget(song_widget)

        self._list_widget.setLayout(self._list_layout)
        self._scroll_area.setWidget(self._list_widget)
        self._layout.addWidget(self._scroll_area)

