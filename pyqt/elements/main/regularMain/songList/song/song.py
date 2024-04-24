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
        with open("./pyqt/elements/main/regularMain/songList/song/song.css", "r") as file:
            self.__styles = file.read()
        self.setFixedWidth(config.TILE_WIDTH + LAYOUT_SPACING + config.NUMBER_LABEL_WIDTH)
        self.setFixedHeight(TILE_HEIGHT)
        self.setContentsMargins(0, 0, 0, 0)
        self.__media_player = media_player
        self.__chosen = False
        self.__song = song
        self.__song_number = number
        self.__create_UI()

    def __create_UI(self):
        self.__layout = QHBoxLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(LAYOUT_SPACING)
        self.setLayout(self.__layout)

        self.__number_label = QLabel(str(self.__song_number))
        self.__number_label.setObjectName("song_number_label")
        self.__number_label.setStyleSheet(self.__styles)
        self.__number_label.setContentsMargins(0, 0, 0, 0)
        self.__number_label.setFixedWidth(config.NUMBER_LABEL_WIDTH)
        self.__number_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.__layout.addWidget(self.__number_label)

        self.__song_frame = QFrame()
        self.__song_frame.setObjectName("song_frame")
        self.__song_frame.setStyleSheet(self.__styles)
        self.__song_frame.setFixedSize(config.TILE_WIDTH, TILE_HEIGHT)
        self.__song_frame.setContentsMargins(0, 0, 0, 0)
        self.__layout.addWidget(self.__song_frame)

        self.__song_layout = QHBoxLayout()
        self.__song_layout.setSpacing(0)
        self.__song_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.__song_layout.setContentsMargins(
            SONG_LAYOUT_MARGIN,
            SONG_LAYOUT_MARGIN,
            SONG_LAYOUT_MARGIN,
            SONG_LAYOUT_MARGIN
        )
        self.__create__title_layout()
        self.__song_frame.setLayout(self.__song_layout)

        self.__album_label = QLabel(self.__song.song_album)
        self.__album_label.setObjectName("song_album_label")
        self.__album_label.setStyleSheet(self.__styles)
        self.__album_label.setContentsMargins(0, 0, 0, 0)
        self.__album_label.setFixedSize(int(config.TILE_WIDTH * ALBUM_WIDGET_WIDTH_RATIO), LABEL_HEIGHT)
        self.__song_layout.addWidget(self.__album_label)

        self.__duration_label = QLabel(self.__song.song_duration)
        self.__duration_label.setObjectName("song_duration_label")
        self.__duration_label.setStyleSheet(self.__styles)
        self.__duration_label.setIndent(0)
        self.__duration_label.setFixedWidth(DURATION_LABEL_WIDTH)
        self.__duration_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.__duration_label.setContentsMargins(0, 0, 0, 0)
        self.__song_layout.addWidget(self.__duration_label)

        self.__margin_label = QLabel("")
        self.__margin_label.setFixedWidth(MARGIN_LABEL_WIDTH)
        self.__song_layout.addWidget(self.__margin_label)

        self.__delete_song_button = QPushButton(QIcon("common/assets/delete.svg"), "")
        self.__delete_song_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__delete_song_button.setObjectName("delete_song_button")
        self.__delete_song_button.setStyleSheet(self.__styles)
        self.__delete_song_button.clicked.connect(self.__remove_song)
        self.__song_layout.addWidget(self.__delete_song_button)

    def __create__title_layout(self):
        self.__title_layout = QHBoxLayout()
        self.__title_layout.setContentsMargins(0, 0, 0, 0)
        self.__title_layout.setSpacing(TITLE_LAYOUT_SPACING)
        self.__title_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.__song_layout.addLayout(self.__title_layout)

        self.__cover_label = QLabel()
        self.__cover_pixmap = None
        if self.__song.song_cover_image_stream is not None:
            cover_image = QImage.fromData(self.__song.song_cover_image_stream)
            self._cover_pixmap = QPixmap.fromImage(cover_image)
        else:
            self._cover_pixmap = QPixmap("common/assets/placeholder.png")
        self._cover_pixmap = self._cover_pixmap.scaled(
            SONG_COVER_SIZE,
            SONG_COVER_SIZE,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio
        )
        self.__cover_label.setPixmap(self._cover_pixmap)
        self.__cover_label.setObjectName("cover_label")
        self.__cover_label.setStyleSheet(self.__styles)
        self.__cover_label.setFixedWidth(SONG_COVER_SIZE)
        self.__cover_label.setFixedHeight(SONG_COVER_SIZE)
        self.__title_layout.addWidget(self.__cover_label)

        self.__play_button = QPushButton(QIcon("common/assets/play_light.svg"), "")
        self.__play_button.setFixedSize(SONG_COVER_SIZE, SONG_COVER_SIZE)
        self.__play_button.setObjectName("song_play_button")
        self.__play_button.setStyleSheet(self.__styles)
        self.__play_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__play_button.setVisible(False)
        self.__play_button.clicked.connect(self.__play_song)
        self.__title_layout.addWidget(self.__play_button)

        self.__title_author_widget = QWidget()
        self.__title_author_widget.setFixedSize(int(config.TILE_WIDTH * TITLE_WIDGET_WIDTH_RATIO), SONG_COVER_SIZE)
        self.__title_author_widget.setContentsMargins(0, 0, 0, 0)
        self.__title_layout.addWidget(self.__title_author_widget)

        self.__title_author_layout = QVBoxLayout()
        self.__title_author_layout.setSpacing(TITLE_AUTHOR_LAYOUT_SPACING)
        self.__title_author_layout.setContentsMargins(0, 0, 0, 0)
        self.__title_author_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__title_author_widget.setLayout(self.__title_author_layout)

        self.__title_label = QLabel(self.__song.song_title if self.__song.song_title != "" else self.__song.file_name)
        self.__title_label.setObjectName("song_title_label")
        self.__title_label.setStyleSheet(self.__styles)
        self.__title_label.setIndent(0)
        self.__title_label.setFixedSize(int(config.TILE_WIDTH * TITLE_WIDGET_WIDTH_RATIO), LABEL_HEIGHT)
        self.__title_label.setContentsMargins(0, 0, 0, 0)
        self.__title_author_layout.addWidget(self.__title_label)

        if self.__song.song_author != "":
            self.__author_label = QLabel(self.__song.song_author)
            self.__author_label.setObjectName("song_author_label")
            self.__author_label.setStyleSheet(self.__styles)
            self.__author_label.setContentsMargins(0, 0, 0, 0)
            self.__author_label.setFixedSize(int(config.TILE_WIDTH * TITLE_WIDGET_WIDTH_RATIO), LABEL_HEIGHT)
            self.__author_label.setIndent(0)
            self.__title_author_layout.addWidget(self.__author_label)

    def enterEvent(self, event):
        if not self.__chosen:
            self.__play_button.setVisible(True)
            self.__cover_label.setVisible(False)
            super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.__chosen:
            self.__play_button.setVisible(False)
            self.__cover_label.setVisible(True)

    def __play_song(self):
        if not self.__chosen:
            print(f"play '{self.__song.full_path}'")
            self.__media_player.play_song(self.__song)

    def choose(self):
        self.__song_frame.setStyleSheet(
            """QFrame#song_frame {
                border: 2px solid #76ABAE;
                background-color: #31363F;
                border-radius: 5px;
            }"""
        )
        self.__play_button.setVisible(True)
        self.__play_button.setCursor(Qt.CursorShape.ArrowCursor)
        self.__play_button.setIcon(QIcon("common/assets/play_active.svg"))
        self.__cover_label.setVisible(False)
        self.__delete_song_button.setVisible(False)
        self.__chosen = True

    def unchoose(self):
        self.__song_frame.setStyleSheet(
            """QFrame#song_frame {
                background-color: #31363F;
                border-radius: 5px;
                border: 2px solid #31363F;
            }"""
        )
        self.__play_button.setVisible(False)
        self.__play_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__play_button.setIcon(QIcon("common/assets/play_light.svg"))
        self.__cover_label.setVisible(True)
        self.__delete_song_button.setVisible(True)
        self.__chosen = False

    def __remove_song(self):
        self.__media_player.delete_song(self.__song)

    def set_song_number(self, number):
        self.__song_number = number
        self.__number_label.setText(str(number))

