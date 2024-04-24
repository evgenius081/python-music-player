from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QScrollBar

import config
from pyqt.elements.main.regularMain.songList.song.Song import Song

LAYOUT_VERTICAL_MARGIN = 22
LAYOUT_RIGHT_MARGIN = 3
HEADER_LEFT_MARGIN = 20
HEADER_BOTTOM_MARGIN = 15
DURATION_ICON_SIZE = 18
LIST_LAYOUT_SPACING = 15


class SongList(QWidget):
    def __init__(self, media_player):
        super().__init__()
        self.setFixedHeight(config.WINDOW_HEIGHT - config.MENU_BAR_HEIGHT - config.CONTROL_BLOCK_HEIGHT)
        self.setFixedWidth(config.WINDOW_WIDTH)
        self.setObjectName("music_list")
        with open("./pyqt/elements/main/regularMain/songList/SongList.css", "r") as file:
            self._styles = file.read()
        self.setStyleSheet(self._styles)
        self._media_player = media_player
        self._media_player.sourceChanged.connect(self._current_song_updated)
        self._media_player.song_deleted.connect(self._song_deleted)
        self._media_player.songs_added.connect(self._songs_added)
        self._songs = self._media_player.songs[:]
        self._current_song_index = 0
        self._song_widgets = []
        self._create_UI()

    def _create_UI(self):
        self._layout = QVBoxLayout()
        side_margin = int((config.WINDOW_WIDTH - config.TILE_WIDTH) / 2) - config.NUMBER_LABEL_WIDTH
        self._layout.setContentsMargins(
            side_margin,
            LAYOUT_VERTICAL_MARGIN,
            LAYOUT_RIGHT_MARGIN,
            LAYOUT_VERTICAL_MARGIN
        )
        self._layout.setSpacing(0)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)

        self._create_header()
        self._create_list()

    def _create_header(self):
        self._header_layout = QHBoxLayout()
        self._header_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        self._header_layout.setContentsMargins(HEADER_LEFT_MARGIN, 0, 0, HEADER_BOTTOM_MARGIN)
        self._layout.addLayout(self._header_layout)

        self._number_label = QLabel("#")
        self._number_label.setObjectName("header_number_label")
        self._header_layout.addWidget(self._number_label)

        self._title_label = QLabel("Tytuł")
        self._title_label.setObjectName("header_title_label")
        self._header_layout.addWidget(self._title_label)

        self._album_label = QLabel("Album")
        self._album_label.setObjectName("header_album_label")
        self._header_layout.addWidget(self._album_label)

        self._duration_icon = QSvgWidget("common/assets/duration.svg")
        self._duration_icon.setObjectName("header_duration_icon")
        self._duration_icon.setFixedSize(DURATION_ICON_SIZE, DURATION_ICON_SIZE)
        self._header_layout.addWidget(self._duration_icon)

    def _create_list(self):
        self._scroll_bar = QScrollBar()
        self._scroll_bar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(self._styles)

        self._scroll_area = QScrollArea()
        self._scroll_area.setObjectName("song_scroll")
        self._scroll_area.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._scroll_area.setContentsMargins(0, 0, 0, 0)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setVerticalScrollBar(self._scroll_bar)

        self._list_widget = QWidget()
        self._list_widget.setObjectName("song_list_widget")
        self._list_widget.setStyleSheet(self._styles)
        self._list_widget.setContentsMargins(0, 0, 0, 0)

        self._list_layout = QVBoxLayout()
        self._list_layout.setSpacing(LIST_LAYOUT_SPACING)
        self._list_layout.setContentsMargins(0, 0, 0, 0)
        self._list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for index, song in enumerate(self._songs):
            song_widget = Song(song, index + 1, self._media_player)
            if index == 0:
                song_widget.choose()
            self._song_widgets.append(song_widget)
            self._list_layout.addWidget(song_widget)

        self._list_widget.setLayout(self._list_layout)
        self._scroll_area.setWidget(self._list_widget)
        self._layout.addWidget(self._scroll_area)

    def _current_song_updated(self):
        chosen_song_index = self._songs.index(self._media_player.get_current_song())
        if chosen_song_index != self._current_song_index:
            self._song_widgets[self._current_song_index].unchoose()
            self._song_widgets[chosen_song_index].choose()
            self._current_song_index = chosen_song_index

    def _song_deleted(self, song):
        song_to_remove = \
            [self._songs[i] for i in range(len(self._songs)) if self._songs[i].file_name == song.file_name][0]
        song_to_remove_index = self._songs.index(song_to_remove)
        self._songs.remove(song_to_remove)
        song_widget_to_remove = self._song_widgets[song_to_remove_index]
        self._list_layout.removeWidget(song_widget_to_remove)
        song_widget_to_remove.setParent(None)
        self._song_widgets.remove(song_widget_to_remove)
        self._current_song_index = self._media_player.get_current_song()
        for index, song_widget in enumerate(self._song_widgets):
            song_widget.set_song_number(index + 1)

    def _songs_added(self, new_songs):
        for index, song in enumerate(new_songs):
            song_widget = Song(song, len(self._songs) + index + 1, self._media_player)
            self._song_widgets.append(song_widget)
            self._list_layout.addWidget(song_widget)
        self._songs.extend(new_songs)

