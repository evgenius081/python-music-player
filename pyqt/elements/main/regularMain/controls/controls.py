from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSlider

import config
from common.utils.formatter import number_to_mins_and_secs

CURRENT_SONG_COVER_SIZE = 50
CURRENT_SONG_TITLE_LABEL = 17
CURRENT_SONG_AUTHOR_LABEL_HEIGHT = 17
CURRENT_SONG_LAYOUT_SPACING = 10
CONTROLS_LAYOUT_SPACING = 16
TITLE_AUTHOR_LAYOUT_SPACING = 2
TITLE_AUTHOR_WIDGET_HEIGHT = 36
CURRENT_SONG_WIDGET_HEIGHT = 50
CONTROL_BUTTONS_WIDGET_HEIGHT = 36
CONTROL_BUTTONS_LAYOUT_SPACING = 22
CONTROL_BUTTON_SIZE = 20
PLAY_BUTTON_SIZE = 36
CONTROL_SLIDER_WIDGET_HEIGHT = 17
CONTROL_SLIDER_LAYOUT_SPACING = 13
SOUND_CONTROLS_LAYOUT_SPACING = 15
SOUND_ICON_SIZE = 24
SOUND_RANGE_MIN = 0
SOUND_RANGE_MAX = 100
SOUND_SLIDER_WIDTH = 100
INIT_VOLUME = 0


class Controls(QWidget):
    def __init__(self, media_player):
        super().__init__()
        self.setFixedHeight(config.CONTROL_BLOCK_HEIGHT)
        self.setFixedWidth(config.WINDOW_WIDTH)
        self.setContentsMargins(18, 18, 18, 18)
        with open("pyqt/elements/main/regularMain/controls/controls.css", "r") as file:
            self.__styles = file.read()
        self.__media_player = media_player
        self.__current_song = self.__media_player.get_current_song()
        self.__set_source(self.__current_song.full_path)
        self.__media_player.positionChanged.connect(self.__position_changed)
        self.__media_player.durationChanged.connect(self.__set_duration)
        self.__media_player.playbackStateChanged.connect(self.__playback_state_changed)
        self.__media_player.sourceChanged.connect(self.__source_changed)
        self.__media_player.audioOutput().volumeChanged.connect(self.__sound_position_changed)
        self.__current_song_second = 0
        self.__skip_play_next = False
        self.setObjectName("controls")
        self.setStyleSheet(self.__styles)
        self.__current_song_and_sound_width = int((config.WINDOW_WIDTH - config.SLIDER_BLOCK_WIDTH - 10) / 2)
        self.__create_UI()

    def __create_UI(self):
        self.__layout = QHBoxLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(self.__layout)

        self.__create_current_song_widget()
        self.__create_controls_widget()
        self.__create_sound_controls_widget()

    def __create_current_song_widget(self):
        self.__current_song_widget = QWidget()
        self.__current_song_widget.setFixedSize(self.__current_song_and_sound_width, CURRENT_SONG_WIDGET_HEIGHT)
        self.__current_song_widget.setContentsMargins(0, 0, 0, 0)
        p = self.__current_song_widget.palette()
        p.setColor(self.__current_song_widget.backgroundRole(), Qt.GlobalColor.red)
        self.__current_song_widget.setPalette(p)
        self.__layout.addWidget(self.__current_song_widget)

        self.__current_song_layout = QHBoxLayout()
        self.__current_song_layout.setSpacing(CURRENT_SONG_LAYOUT_SPACING)
        self.__current_song_layout.setContentsMargins(0, 0, 0, 0)
        self.__current_song_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        self.__current_song_widget.setLayout(self.__current_song_layout)

        self.__cover_label = QLabel()
        self.__set_cover()
        self.__cover_label.setObjectName("current_cover_label")
        self.__cover_label.setStyleSheet(self.__styles)
        self.__cover_label.setFixedWidth(CURRENT_SONG_COVER_SIZE)
        self.__cover_label.setFixedHeight(CURRENT_SONG_COVER_SIZE)
        self.__current_song_layout.addWidget(self.__cover_label)

        self.__title_author_widget = QWidget()
        self.__title_author_widget.setFixedSize(
            self.__current_song_and_sound_width - CURRENT_SONG_COVER_SIZE - CURRENT_SONG_LAYOUT_SPACING,
            TITLE_AUTHOR_WIDGET_HEIGHT
        )
        self.__title_author_widget.setContentsMargins(0, 0, 0, 0)
        self.__current_song_layout.addWidget(self.__title_author_widget)

        self.__title_author_layout = QVBoxLayout()
        self.__title_author_layout.setSpacing(TITLE_AUTHOR_LAYOUT_SPACING)
        self.__title_author_layout.setContentsMargins(0, 0, 0, 0)
        self.__title_author_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__title_author_widget.setLayout(self.__title_author_layout)

        self.__title_label = QLabel(
            self.__current_song.song_title if self.__current_song.song_title != "" else
            self.__current_song.file_name
        )
        self.__title_label.setObjectName("current_song_title_label")
        self.__title_label.setStyleSheet(self.__styles)
        self.__title_label.setIndent(0)
        self.__title_label.setFixedSize(
            self.__current_song_and_sound_width - CURRENT_SONG_COVER_SIZE - CURRENT_SONG_LAYOUT_SPACING,
            CURRENT_SONG_TITLE_LABEL
        )
        self.__title_label.setContentsMargins(0, 0, 0, 0)
        self.__title_author_layout.addWidget(self.__title_label)

        if self.__current_song.song_author != "":
            self.__author_label = QLabel(self.__current_song.song_author)
            self.__author_label.setObjectName("current_song_author_label")
            self.__author_label.setStyleSheet(self.__styles)
            self.__author_label.setContentsMargins(0, 0, 0, 0)
            self.__author_label.setFixedSize(
                self.__current_song_and_sound_width - CURRENT_SONG_COVER_SIZE - CURRENT_SONG_LAYOUT_SPACING,
                CURRENT_SONG_TITLE_LABEL)
            self.__author_label.setIndent(0)
            self.__title_author_layout.addWidget(self.__author_label)

    def __create_controls_widget(self):
        self.__controls_widget = QWidget()
        self.__controls_widget.setContentsMargins(0, 0, 0, 0)
        self.__controls_widget.setFixedWidth(config.SLIDER_BLOCK_WIDTH)
        self.__layout.addWidget(self.__controls_widget)

        self.__controls_layout = QVBoxLayout()
        self.__controls_layout.setSpacing(CONTROLS_LAYOUT_SPACING)
        self.__controls_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__controls_layout.setContentsMargins(0, 0, 0, 0)
        self.__controls_widget.setLayout(self.__controls_layout)
        self.__create_buttons()
        self.__create_slider()

    def __create_buttons(self):
        self.__control_buttons_widget = QWidget()
        self.__control_buttons_widget.setContentsMargins(0, 0, 0, 0)
        self.__control_buttons_widget.setFixedSize(config.SLIDER_BLOCK_WIDTH, CONTROL_BUTTONS_WIDGET_HEIGHT)
        self.__controls_layout.addWidget(self.__control_buttons_widget)

        self.__control_buttons_layout = QHBoxLayout()
        self.__control_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.__control_buttons_layout.setSpacing(CONTROL_BUTTONS_LAYOUT_SPACING)
        self.__control_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__control_buttons_widget.setLayout(self.__control_buttons_layout)

        self.__shuffle_button = QPushButton(QIcon("pyqt/assets/shuffle_inactive.svg"), "")
        self.__shuffle_button.setObjectName("shuffle_button")
        self.__shuffle_button.setStyleSheet(self.__styles)
        self.__shuffle_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__shuffle_button.setFixedSize(CONTROL_BUTTON_SIZE, CONTROL_BUTTON_SIZE)
        self.__shuffle_button.clicked.connect(self.__shuffle_songs)
        self.__control_buttons_layout.addWidget(self.__shuffle_button)

        self.__play_prev_button = QPushButton("")
        self.__play_prev_button.setObjectName("play_prev_button")
        self.__play_prev_button.setStyleSheet(self.__styles)
        self.__play_prev_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__play_prev_button.setFixedSize(CONTROL_BUTTON_SIZE, CONTROL_BUTTON_SIZE)
        self.__play_prev_button.clicked.connect(self.__play_prev)
        self.__set_prev_button_disabled()
        self.__control_buttons_layout.addWidget(self.__play_prev_button)

        self.__play_button = QPushButton(QIcon("pyqt/assets/play_active.svg"), "")
        self.__play_button.setObjectName("play_button")
        self.__play_button.setStyleSheet(self.__styles)
        self.__play_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__play_button.setFixedSize(PLAY_BUTTON_SIZE, PLAY_BUTTON_SIZE)
        self.__play_button.clicked.connect(self.__play_song)
        self.__control_buttons_layout.addWidget(self.__play_button)

        self.__play_next_button = QPushButton(QIcon("pyqt/assets/play_next_active.svg"), "")
        self.__play_next_button.setObjectName("play_next_button")
        self.__play_next_button.setStyleSheet(self.__styles)
        self.__play_next_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__play_next_button.setFixedSize(CONTROL_BUTTON_SIZE, CONTROL_BUTTON_SIZE)
        self.__play_next_button.clicked.connect(self.__play_next)
        self.__control_buttons_layout.addWidget(self.__play_next_button)

        self.__cycle_button = QPushButton(QIcon("pyqt/assets/cycle.svg"), "")
        self.__cycle_button.setObjectName("cycle_button")
        self.__cycle_button.setStyleSheet(self.__styles)
        self.__cycle_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__cycle_button.setFixedSize(CONTROL_BUTTON_SIZE, CONTROL_BUTTON_SIZE)
        self.__cycle_button.clicked.connect(self.__cycle)
        self.__control_buttons_layout.addWidget(self.__cycle_button)

    def __create_slider(self):
        self.__control_slider_widget = QWidget()
        self.__control_slider_widget.setContentsMargins(0, 0, 0, 0)
        self.__control_slider_widget.setFixedSize(config.SLIDER_BLOCK_WIDTH, CONTROL_SLIDER_WIDGET_HEIGHT)
        self.__controls_layout.addWidget(self.__control_slider_widget)

        self.__control_slider_layout = QHBoxLayout()
        self.__control_slider_layout.setContentsMargins(0, 0, 0, 0)
        self.__control_slider_layout.setSpacing(CONTROL_SLIDER_LAYOUT_SPACING)
        self.__control_slider_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__control_slider_widget.setLayout(self.__control_slider_layout)

        self.__current_time_label = QLabel(" 0:00")
        self.__current_time_label.setObjectName("current_playback_time_label")
        self.__current_time_label.setStyleSheet(self.__styles)
        self.__control_slider_layout.addWidget(self.__current_time_label)

        self.__playback_slider = QSlider(Qt.Orientation.Horizontal)
        self.__playback_slider.setStyleSheet(self.__styles)
        self.__playback_slider.sliderMoved.connect(self.__set_position)
        self.__control_slider_layout.addWidget(self.__playback_slider)

        self.__total_time_label = QLabel(self.__current_song.song_duration)
        self.__total_time_label.setObjectName("total_playback_time_label")
        self.__total_time_label.setStyleSheet(self.__styles)
        self.__control_slider_layout.addWidget(self.__total_time_label)

    def __create_sound_controls_widget(self):
        self.__sound_controls_widget = QWidget()
        self.__sound_controls_widget.setContentsMargins(
            self.__current_song_and_sound_width -
            SOUND_SLIDER_WIDTH -
            SOUND_CONTROLS_LAYOUT_SPACING -
            SOUND_ICON_SIZE,
            0,
            0,
            0
        )
        self.__sound_controls_widget.setFixedWidth(self.__current_song_and_sound_width)
        self.__layout.addWidget(self.__sound_controls_widget)

        self.__sound_controls_layout = QHBoxLayout()
        self.__sound_controls_layout.setContentsMargins(0, 0, 0, 0)
        self.__sound_controls_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.__sound_controls_layout.setSpacing(SOUND_CONTROLS_LAYOUT_SPACING)
        self.__sound_controls_widget.setLayout(self.__sound_controls_layout)

        self.__sound_icon = QSvgWidget("pyqt/assets/sound.svg")
        self.__sound_icon.setFixedSize(SOUND_ICON_SIZE, SOUND_ICON_SIZE)
        self.__sound_controls_layout.addWidget(self.__sound_icon)

        self.__sound_slider = QSlider(Qt.Orientation.Horizontal)
        self.__sound_slider.setStyleSheet(self.__styles)
        self.__sound_slider.setRange(SOUND_RANGE_MIN, SOUND_RANGE_MAX)
        self.__sound_slider.sliderMoved.connect(self.__set_volume)
        self.__sound_slider.setValue(INIT_VOLUME)
        self.__set_volume(INIT_VOLUME)
        self.__sound_controls_layout.addWidget(self.__sound_slider)

    def __set_cover(self):
        if self.__current_song.song_cover_image_stream is not None:
            cover_image = QImage.fromData(self.__current_song.song_cover_image_stream)
            cover_pixmap = QPixmap.fromImage(cover_image)
        else:
            cover_pixmap = QPixmap("pyqt/assets/placeholder.png")
        cover_pixmap_scaled = cover_pixmap.scaled(
            CURRENT_SONG_COVER_SIZE,
            CURRENT_SONG_COVER_SIZE,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio
        )
        self.__cover_label.setPixmap(cover_pixmap_scaled)

    def __set_current_song(self, song):
        self.__current_song = song
        self.__title_label.setText(song.song_title)
        self.__author_label.setText(song.song_author)
        self.__set_cover()

    def __set_source(self, file_path):
        self.__media_player.setSource(QUrl.fromLocalFile(file_path))

    def __position_changed(self, position):
        self.__playback_slider.setValue(position)
        self.__refresh_current_time_label(position)

    def __source_changed(self):
        if self.__media_player.is_current_song_first() and not self.__media_player.get_cycled_playlist():
            self.__set_prev_button_disabled()
        else:
            self.__set_prev_button_active()

        if self.__media_player.is_current_song_last() and not self.__media_player.get_cycled_playlist():
            self.__set_next_button_disabled()
        else:
            self.__set_next_button_active()

        current_song = self.__media_player.get_current_song()
        self.__set_current_song(current_song)
        self.__media_player.uncycle()
        self.__cycle_button.setIcon(QIcon("pyqt/assets/cycle.svg"))

    def __set_position(self, position):
        self.__media_player.setPosition(position)
        self.__refresh_current_time_label(position)

    def __refresh_current_time_label(self, position):
        current_second, _ = divmod(position, 1000)
        if self.__current_song_second < current_second or self.__current_song_second > current_second:
            self.__current_time_label.setText(str(number_to_mins_and_secs(current_second)))
            self.__current_song_second = current_second

    def __play_song(self):
        if self.__media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.__media_player.pause()
            self.__play_button.setIcon(QIcon("pyqt/assets/play_active.svg"))
        else:
            self.__media_player.play()
            self.__play_button.setIcon(QIcon("pyqt/assets/pause_active.svg"))

    def __set_duration(self, duration):
        self.__playback_slider.setRange(0, duration)
        self.__total_time_label.setText(self.__current_song.song_duration)

    def __set_prev_button_disabled(self):
        self.__play_prev_button.setDisabled(True)
        self.__play_prev_button.setIcon(QIcon("pyqt/assets/play_prev_inactive.svg"))

    def __set_prev_button_active(self):
        self.__play_prev_button.setDisabled(False)
        self.__play_prev_button.setIcon(QIcon("pyqt/assets/play_prev_active.svg"))

    def __set_next_button_disabled(self):
        self.__play_next_button.setDisabled(True)
        self.__play_next_button.setIcon(QIcon("pyqt/assets/play_next_inactive.svg"))

    def __set_next_button_active(self):
        self.__play_next_button.setDisabled(False)
        self.__play_next_button.setIcon(QIcon("pyqt/assets/play_next_active.svg"))

    def __set_volume(self, volume):
        self.__media_player.set_volume(volume)

    def __play_next(self):
        self.__current_time_label.setText(" 0:00")
        self.__playback_slider.setValue(0)
        self.__current_song_second = 0
        self.__set_prev_button_active()
        self.__skip_play_next = True
        self.__media_player.play_next()
        current_song = self.__media_player.get_current_song()
        self.__set_current_song(current_song)

        if self.__media_player.is_current_song_last() and not self.__media_player.get_cycled_playlist():
            self.__set_next_button_disabled()

        if self.__media_player.get_cycled_one_song():
            self.__media_player.uncycle()
            self.__cycle_button.setIcon(QIcon("pyqt/assets/cycle.svg"))

    def __play_prev(self):
        self.__current_time_label.setText(" 0:00")
        self.__playback_slider.setValue(0)
        self.__current_song_second = 0
        self.__set_next_button_active()
        self.__skip_play_next = True
        self.__media_player.play_prev()
        current_song = self.__media_player.get_current_song()
        self.__set_current_song(current_song)
        if self.__media_player.is_current_song_first() and not self.__media_player.get_cycled_playlist():
            self.__set_prev_button_disabled()

    def __cycle(self):
        if self.__media_player.get_cycled_playlist():
            self.__media_player.uncycle()
            self.__cycle_button.setIcon(QIcon("pyqt/assets/cycle.svg"))
            if self.__media_player.is_current_song_first() and not self.__media_player.get_cycled_playlist():
                self.__set_prev_button_disabled()
            else:
                self.__set_prev_button_active()

            if self.__media_player.is_current_song_last() and not self.__media_player.get_cycled_playlist():
                self.__set_next_button_disabled()
            else:
                self.__set_next_button_active()
        elif self.__media_player.get_cycled_one_song():
            self.__media_player.cycle_playlist()
            self.__cycle_button.setIcon(QIcon("pyqt/assets/cycle_list.svg"))
            self.__set_prev_button_active()
            self.__set_next_button_active()
        else:
            self.__media_player.cycle_one_song()
            self.__cycle_button.setIcon(QIcon("pyqt/assets/cycle_one.svg"))

    def __playback_state_changed(self):
        if self.__media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.__play_button.setIcon(QIcon("pyqt/assets/pause_active.svg"))
        else:
            self.__skip_play_next = False
            self.__play_button.setIcon(QIcon("pyqt/assets/play_active.svg"))

    def __shuffle_songs(self):
        if self.__media_player.get_shuffled():
            self.__media_player.unshuffle()
            self.__shuffle_button.setIcon(QIcon("pyqt/assets/shuffle_inactive.svg"))
        else:
            self.__media_player.shuffle()
            self.__shuffle_button.setIcon(QIcon("pyqt/assets/shuffle_active.svg"))

        if self.__media_player.is_current_song_first() and not self.__media_player.get_cycled_playlist():
            self.__set_prev_button_disabled()
        else:
            self.__set_prev_button_active()

        if self.__media_player.is_current_song_last() and not self.__media_player.get_cycled_playlist():
            self.__set_next_button_disabled()
        else:
            self.__set_next_button_active()

    def __sound_position_changed(self, position):
        self.__sound_slider.setValue(int(position * 100))

