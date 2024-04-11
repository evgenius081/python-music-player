from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QScrollBar

import config
from pyqt.elements.main.regularMain.songList.song.song import Song

LAYOUT_VERTICAL_MARGIN = 22
LAYOUT_RIGHT_MARGIN = 3
HEADER_LEFT_MARGIN = 20
HEADER_BOTTOM_MARGIN = 15
DURATION_ICON_SIZE = 18
LIST_LAYOUT_SPACING = 15


class MusicList(QWidget):
    def __init__(self, media_player):
        super().__init__()
        self.setFixedHeight(config.WINDOW_HEIGHT - config.MENU_BAR_HEIGHT - config.CONTROL_BLOCK_HEIGHT)
        self.setFixedWidth(config.WINDOW_WIDTH)
        self.setObjectName("music_list")
        with open("./pyqt/elements/main/regularMain/songList/songList.css", "r") as file:
            self.__styles = file.read()
        self.setStyleSheet(self.__styles)
        self.__media_player = media_player
        self.__media_player.sourceChanged.connect(self.__current_song_updated)
        self.__songs = self.__media_player.get_songs()
        self.__current_song_index = 0
        self.__song_widgets = []
        self.__create_UI()

    def __create_UI(self):
        self.__layout = QVBoxLayout()
        side_margin = int((config.WINDOW_WIDTH - config.TILE_WIDTH) / 2) - config.NUMBER_LABEL_WIDTH
        self.__layout.setContentsMargins(
            side_margin,
            LAYOUT_VERTICAL_MARGIN,
            LAYOUT_RIGHT_MARGIN,
            LAYOUT_VERTICAL_MARGIN
        )
        self.__layout.setSpacing(0)
        self.__layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.__layout)

        self.__create_header()
        self.__create_list()

    def __create_header(self):
        self.__header_layout = QHBoxLayout()
        self.__header_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        self.__header_layout.setContentsMargins(HEADER_LEFT_MARGIN, 0, 0, HEADER_BOTTOM_MARGIN)
        self.__layout.addLayout(self.__header_layout)

        self.__number_label = QLabel("#")
        self.__number_label.setObjectName("header_number_label")
        self.__header_layout.addWidget(self.__number_label)

        self.__title_label = QLabel("Tytuł")
        self.__title_label.setObjectName("header_title_label")
        self.__header_layout.addWidget(self.__title_label)

        self.__album_label = QLabel("Album")
        self.__album_label.setObjectName("header_album_label")
        self.__header_layout.addWidget(self.__album_label)

        self.__duration_icon = QSvgWidget("common/assets/duration.svg")
        self.__duration_icon.setObjectName("header_duration_icon")
        self.__duration_icon.setFixedSize(DURATION_ICON_SIZE, DURATION_ICON_SIZE)
        self.__header_layout.addWidget(self.__duration_icon)

    def __create_list(self):
        self.__scroll_bar = QScrollBar()
        self.__scroll_bar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(self.__styles)

        self.__scroll_area = QScrollArea()
        self.__scroll_area.setObjectName("song_scroll")
        self.__scroll_area.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.__scroll_area.setContentsMargins(0, 0, 0, 0)
        self.__scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.__scroll_area.setVerticalScrollBar(self.__scroll_bar)

        self.__list_widget = QWidget()
        self.__list_widget.setObjectName("song_list_widget")
        self.__list_widget.setStyleSheet(self.__styles)
        self.__list_widget.setContentsMargins(0, 0, 0, 0)

        self.__list_layout = QVBoxLayout()
        self.__list_layout.setSpacing(LIST_LAYOUT_SPACING)
        self.__list_layout.setContentsMargins(0, 0, 0, 0)
        self.__list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for index, song in enumerate(self.__songs):
            song_widget = Song(song, index, self.__media_player)
            if index == 0:
                song_widget.choose()
            self.__song_widgets.append(song_widget)
            self.__list_layout.addWidget(song_widget)

        self.__list_widget.setLayout(self.__list_layout)
        self.__scroll_area.setWidget(self.__list_widget)
        self.__layout.addWidget(self.__scroll_area)

    def __current_song_updated(self):
        chosen_song_index = self.__songs.index(self.__media_player.get_current_song())
        if chosen_song_index != self.__current_song_index:
            self.__song_widgets[self.__current_song_index].unchoose()
            self.__song_widgets[chosen_song_index].choose()
            self.__current_song_index = chosen_song_index
