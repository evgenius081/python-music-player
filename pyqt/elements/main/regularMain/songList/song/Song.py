from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QImage, QIcon, QAction
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame, QVBoxLayout, QPushButton, QMenu

import config

TILE_HEIGHT = 52
TITLE_WIDGET_WIDTH_RATIO = 0.4
ALBUM_WIDGET_WIDTH_RATIO = 0.39
LAYOUT_SPACING = 14
SONG_LAYOUT_MARGIN = 7
LABEL_HEIGHT = 17
DURATION_LABEL_WIDTH = 30
MARGIN_LABEL_WIDTH = 35
TITLE_LAYOUT_SPACING = 9
SONG_COVER_SIZE = 34
TITLE_AUTHOR_LAYOUT_SPACING = 2


class Song(QWidget):
    def __init__(self, song, number, media_player):
        super().__init__()
        self.setObjectName("song")
        with open("./pyqt/elements/main/regularMain/songList/song/Song.css", "r") as file:
            self._styles = file.read()
        self.setFixedWidth(config.TILE_WIDTH + LAYOUT_SPACING + config.NUMBER_LABEL_WIDTH)
        self.setFixedHeight(TILE_HEIGHT)
        self.setContentsMargins(0, 0, 0, 0)
        self._media_player = media_player
        self._chosen = False
        self._song = song
        self._song_number = number
        self._create_UI()

    def _create_UI(self):
        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(LAYOUT_SPACING)
        self.setLayout(self._layout)

        self._number_label = QLabel(str(self._song_number))
        self._number_label.setObjectName("song_number_label")
        self._number_label.setStyleSheet(self._styles)
        self._number_label.setContentsMargins(0, 0, 0, 0)
        self._number_label.setFixedWidth(config.NUMBER_LABEL_WIDTH)
        self._number_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self._layout.addWidget(self._number_label)

        self._song_frame = QFrame()
        self._song_frame.setObjectName("song_frame")
        self._song_frame.setStyleSheet(self._styles)
        self._song_frame.setFixedSize(config.TILE_WIDTH, TILE_HEIGHT)
        self._song_frame.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._song_frame)

        self._song_layout = QHBoxLayout()
        self._song_layout.setSpacing(0)
        self._song_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self._song_layout.setContentsMargins(
            SONG_LAYOUT_MARGIN,
            SONG_LAYOUT_MARGIN,
            SONG_LAYOUT_MARGIN,
            SONG_LAYOUT_MARGIN
        )
        self._create_title_layout()
        self._song_frame.setLayout(self._song_layout)

        self._album_label = QLabel(self._song.song_album)
        self._album_label.setObjectName("song_album_label")
        self._album_label.setStyleSheet(self._styles)
        self._album_label.setContentsMargins(0, 0, 0, 0)
        self._album_label.setFixedSize(int(config.TILE_WIDTH * ALBUM_WIDGET_WIDTH_RATIO), LABEL_HEIGHT)
        self._song_layout.addWidget(self._album_label)

        self._duration_label = QLabel(self._song.song_duration)
        self._duration_label.setObjectName("song_duration_label")
        self._duration_label.setStyleSheet(self._styles)
        self._duration_label.setIndent(0)
        self._duration_label.setFixedWidth(DURATION_LABEL_WIDTH)
        self._duration_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self._duration_label.setContentsMargins(0, 0, 0, 0)
        self._song_layout.addWidget(self._duration_label)

        self._margin_label = QLabel("")
        self._margin_label.setFixedWidth(MARGIN_LABEL_WIDTH)
        self._song_layout.addWidget(self._margin_label)

        self._delete_song_button = QPushButton(QIcon("common/assets/delete.svg"), "")
        self._delete_song_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._delete_song_button.setObjectName("delete_song_button")
        self._delete_song_button.setStyleSheet(self._styles)
        self._delete_song_button.clicked.connect(self._remove_song)
        self._song_layout.addWidget(self._delete_song_button)

    def _create_title_layout(self):
        self._title_layout = QHBoxLayout()
        self._title_layout.setContentsMargins(0, 0, 0, 0)
        self._title_layout.setSpacing(TITLE_LAYOUT_SPACING)
        self._title_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self._song_layout.addLayout(self._title_layout)

        self._cover_label = QLabel()
        self._cover_pixmap = None
        if self._song.song_cover_bytes is not None:
            cover_image = QImage.fromData(self._song.song_cover_bytes)
            self._cover_pixmap = QPixmap.fromImage(cover_image)
        else:
            self._cover_pixmap = QPixmap("common/assets/placeholder.png")
        self._cover_pixmap = self._cover_pixmap.scaled(
            SONG_COVER_SIZE,
            SONG_COVER_SIZE,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio
        )
        self._cover_label.setPixmap(self._cover_pixmap)
        self._cover_label.setObjectName("cover_label")
        self._cover_label.setStyleSheet(self._styles)
        self._cover_label.setFixedWidth(SONG_COVER_SIZE)
        self._cover_label.setFixedHeight(SONG_COVER_SIZE)
        self._title_layout.addWidget(self._cover_label)

        self._play_button = QPushButton(QIcon("common/assets/play_light.svg"), "")
        self._play_button.setFixedSize(SONG_COVER_SIZE, SONG_COVER_SIZE)
        self._play_button.setObjectName("song_play_button")
        self._play_button.setStyleSheet(self._styles)
        self._play_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._play_button.setVisible(False)
        self._play_button.clicked.connect(self._play_song)
        self._title_layout.addWidget(self._play_button)

        self._title_author_widget = QWidget()
        self._title_author_widget.setFixedSize(int(config.TILE_WIDTH * TITLE_WIDGET_WIDTH_RATIO), SONG_COVER_SIZE)
        self._title_author_widget.setContentsMargins(0, 0, 0, 0)
        self._title_layout.addWidget(self._title_author_widget)

        self._title_author_layout = QVBoxLayout()
        self._title_author_layout.setSpacing(TITLE_AUTHOR_LAYOUT_SPACING)
        self._title_author_layout.setContentsMargins(0, 0, 0, 0)
        self._title_author_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._title_author_widget.setLayout(self._title_author_layout)

        self._title_label = QLabel(self._song.song_title if self._song.song_title != "" else self._song.file_name)
        self._title_label.setObjectName("song_title_label")
        self._title_label.setStyleSheet(self._styles)
        self._title_label.setIndent(0)
        self._title_label.setFixedSize(int(config.TILE_WIDTH * TITLE_WIDGET_WIDTH_RATIO), LABEL_HEIGHT)
        self._title_label.setContentsMargins(0, 0, 0, 0)
        self._title_author_layout.addWidget(self._title_label)

        if self._song.song_author != "":
            self._author_label = QLabel(self._song.song_author)
            self._author_label.setObjectName("song_author_label")
            self._author_label.setStyleSheet(self._styles)
            self._author_label.setContentsMargins(0, 0, 0, 0)
            self._author_label.setFixedSize(int(config.TILE_WIDTH * TITLE_WIDGET_WIDTH_RATIO), LABEL_HEIGHT)
            self._author_label.setIndent(0)
            self._title_author_layout.addWidget(self._author_label)

    def enterEvent(self, event):
        if not self._chosen:
            self._play_button.setVisible(True)
            self._cover_label.setVisible(False)
            super().enterEvent(event)

    def leaveEvent(self, _):
        if not self._chosen:
            self._play_button.setVisible(False)
            self._cover_label.setVisible(True)

    def _play_song(self):
        if not self._chosen:
            self._media_player.play_song(self._song)

    def choose(self):
        self._song_frame.setStyleSheet(
            """QFrame#song_frame {
                border: 2px solid #76ABAE;
                background-color: #31363F;
                border-radius: 5px;
            }"""
        )
        self._play_button.setVisible(True)
        self._play_button.setCursor(Qt.CursorShape.ArrowCursor)
        self._play_button.setIcon(QIcon("common/assets/play_active.svg"))
        self._cover_label.setVisible(False)
        self._delete_song_button.setVisible(False)
        self._chosen = True

    def unchoose(self):
        self._song_frame.setStyleSheet(
            """QFrame#song_frame {
                background-color: #31363F;
                border-radius: 5px;
                border: 2px solid #31363F;
            }"""
        )
        self._play_button.setVisible(False)
        self._play_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._play_button.setIcon(QIcon("common/assets/play_light.svg"))
        self._cover_label.setVisible(True)
        self._delete_song_button.setVisible(True)
        self._chosen = False

    def _remove_song(self):
        self._media_player.delete_song(self._song)

    def set_song_number(self, number):
        self._song_number = number
        self._number_label.setText(str(number))

