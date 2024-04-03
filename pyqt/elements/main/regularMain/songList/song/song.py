from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame, QVBoxLayout, QPushButton


class Song(QWidget):
    def __init__(self, song, number):
        super().__init__()
        self.setObjectName("song")
        with open("./pyqt/elements/main/regularMain/songList/song/song.css", "r") as file:
            self.__styles = file.read()
        self.setFixedWidth(810)
        self.setFixedHeight(52)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("{ border: 1px solid red; }")
        self.__song = song
        self.__song_number = number
        self.__create_UI()

    def __create_UI(self):
        self.__main_layout = QHBoxLayout()
        self.__main_layout.setContentsMargins(0, 0, 0, 0)
        self.__main_layout.setSpacing(14)
        self.setLayout(self.__main_layout)

        self.__number_label = QLabel(f"{self.__song_number + 1}")
        self.__number_label.setObjectName("song_number_label")
        self.__number_label.setStyleSheet(self.__styles)
        self.__number_label.setContentsMargins(0, 0, 0, 0)
        self.__number_label.setFixedWidth(30)
        self.__number_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.__main_layout.addWidget(self.__number_label)

        self.__song_frame = QFrame()
        self.__song_frame.setObjectName("song_frame")
        self.__song_frame.setStyleSheet(self.__styles)
        self.__song_frame.setFixedHeight(52)
        self.__song_frame.setFixedWidth(765)
        self.__song_frame.setContentsMargins(0, 0, 0, 0)
        self.__main_layout.addWidget(self.__song_frame)

        self.__song_layout = QHBoxLayout()
        self.__song_layout.setSpacing(0)
        self.__song_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.__song_layout.setContentsMargins(9, 9, 9, 9)
        self.__create__title_layout()
        self.__song_frame.setLayout(self.__song_layout)

        self.__album_label = QLabel(self.__song.song_album)
        self.__album_label.setObjectName("song_album_label")
        self.__album_label.setStyleSheet(self.__styles)
        self.__album_label.setContentsMargins(0, 0, 0, 0)
        self.__album_label.setFixedSize(QSize(301, 17))
        self.__song_layout.addWidget(self.__album_label)

        minutes, seconds = divmod(int(self.__song.song_duration_in_sec), 60)
        self.__duration_label = QLabel(f"{minutes:2d}:{seconds:02d}")
        self.__duration_label.setObjectName("song_duration_label")
        self.__duration_label.setStyleSheet(self.__styles)
        self.__duration_label.setIndent(0)
        self.__duration_label.setFixedWidth(30)
        self.__duration_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.__duration_label.setContentsMargins(0, 0, 0, 0)
        self.__song_layout.addWidget(self.__duration_label)

        self.__margin_label = QLabel("")
        self.__margin_label.setFixedWidth(35)
        self.__song_layout.addWidget(self.__margin_label)

        self.__song_options_button = QPushButton(QIcon("pyqt/assets/three_dots.svg"), "")
        self.__song_options_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__song_options_button.setObjectName("song_options_button")
        self.__song_options_button.setStyleSheet(self.__styles)
        self.__song_layout.addWidget(self.__song_options_button)

    def __create__title_layout(self):
        self.__title_layout = QHBoxLayout()
        self.__title_layout.setContentsMargins(0, 0, 0, 0)
        self.__title_layout.setSpacing(9)
        self.__title_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.__song_layout.addLayout(self.__title_layout)

        self.__cover_label = QLabel()
        self.__cover_pixmap = None
        if self.__song.song_cover_image_stream is not None:
            cover_image = QImage.fromData(self.__song.song_cover_image_stream)
            self._cover_pixmap = QPixmap.fromImage(cover_image)
        else:
            self._cover_pixmap = QPixmap("pyqt/assets/placeholder.png")
        self._cover_pixmap = self._cover_pixmap.scaled(34, 34, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.__cover_label.setPixmap(self._cover_pixmap)
        self.__cover_label.setObjectName("cover_label")
        self.__cover_label.setStyleSheet(self.__styles)
        self.__cover_label.setFixedWidth(34)
        self.__cover_label.setFixedHeight(34)
        self.__title_layout.addWidget(self.__cover_label)

        self.__play_button = QPushButton(QIcon("pyqt/assets/play_light.svg"), "")
        self.__play_button.setFixedSize(34, 34)
        self.__play_button.setObjectName("song_play_button")
        self.__play_button.setStyleSheet(self.__styles)
        self.__play_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__play_button.setVisible(False)
        self.__play_button.clicked.connect(self.__play_song)
        self.__title_layout.addWidget(self.__play_button)

        self.__title_author_widget = QWidget()
        self.__title_author_widget.setFixedSize(310, 36)
        self.__title_author_widget.setContentsMargins(0, 0, 0, 0)
        self.__title_layout.addWidget(self.__title_author_widget)

        self.__title_author_layout = QVBoxLayout()
        self.__title_author_layout.setSpacing(2)
        self.__title_author_layout.setContentsMargins(0, 0, 0, 0)
        self.__title_author_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__title_author_widget.setLayout(self.__title_author_layout)

        self.__title_label = QLabel(self.__song.song_name if self.__song.song_name != "" else self.__song.file_name)
        self.__title_label.setObjectName("song_title_label")
        self.__title_label.setStyleSheet(self.__styles)
        self.__title_label.setIndent(0)
        self.__title_label.setFixedSize(QSize(300, 17))
        self.__title_label.setContentsMargins(0, 0, 0, 0)
        self.__title_author_layout.addWidget(self.__title_label)

        if self.__song.song_author != "":
            self.__author_label = QLabel(self.__song.song_author)
            self.__author_label.setObjectName("song_author_label")
            self.__author_label.setStyleSheet(self.__styles)
            self.__author_label.setContentsMargins(0, 0, 0, 0)
            self.__author_label.setFixedSize(QSize(300, 17))
            self.__title_label.setIndent(0)
            self.__title_author_layout.addWidget(self.__author_label)

    def enterEvent(self, event):
        self.__play_button.setVisible(True)
        self.__cover_label.setVisible(False)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.__play_button.setVisible(False)
        self.__cover_label.setVisible(True)
        super().leaveEvent(event)

    def __play_song(self):
        print(f"play '{self.__song.song_name}'")

