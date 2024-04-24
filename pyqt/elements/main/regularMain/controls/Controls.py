from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSlider

import config
from common.classes.Cycling import Cycling
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
        with open("pyqt/elements/main/regularMain/controls/Controls.css", "r") as file:
            self._styles = file.read()
        self._media_player = media_player
        self._current_song = self._media_player.get_current_song()
        self._set_source(self._current_song.full_path)
        self._media_player.cycling_changed.connect(self._cycling_changed)
        self._media_player.shuffling_changed.connect(self._shuffling_changed)
        self._media_player.song_deleted.connect(self._song_deleted)
        self._media_player.positionChanged.connect(self._position_changed)
        self._media_player.durationChanged.connect(self._set_duration)
        self._media_player.playbackStateChanged.connect(self._playback_state_changed)
        self._media_player.sourceChanged.connect(self._source_changed)
        self._media_player.audioOutput().volumeChanged.connect(self._sound_position_changed)
        self._media_player.songs_added.connect(self._songs_added)
        self._current_song_second = 0
        self.setObjectName("controls")
        self.setStyleSheet(self._styles)
        self._current_song_and_sound_width = int((config.WINDOW_WIDTH - config.SLIDER_BLOCK_WIDTH - 10) / 2)
        self._create_UI()

    def _create_UI(self):
        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(self._layout)

        self._create_current_song_widget()
        self._create_controls_widget()
        self._create_sound_controls_widget()

    def _create_current_song_widget(self):
        self._current_song_widget = QWidget()
        self._current_song_widget.setFixedSize(self._current_song_and_sound_width, CURRENT_SONG_WIDGET_HEIGHT)
        self._current_song_widget.setContentsMargins(0, 0, 0, 0)
        p = self._current_song_widget.palette()
        p.setColor(self._current_song_widget.backgroundRole(), Qt.GlobalColor.red)
        self._current_song_widget.setPalette(p)
        self._layout.addWidget(self._current_song_widget)

        self._current_song_layout = QHBoxLayout()
        self._current_song_layout.setSpacing(CURRENT_SONG_LAYOUT_SPACING)
        self._current_song_layout.setContentsMargins(0, 0, 0, 0)
        self._current_song_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        self._current_song_widget.setLayout(self._current_song_layout)

        self._cover_label = QLabel()
        self._set_cover()
        self._cover_label.setObjectName("current_cover_label")
        self._cover_label.setStyleSheet(self._styles)
        self._cover_label.setFixedWidth(CURRENT_SONG_COVER_SIZE)
        self._cover_label.setFixedHeight(CURRENT_SONG_COVER_SIZE)
        self._current_song_layout.addWidget(self._cover_label)

        self._title_author_widget = QWidget()
        self._title_author_widget.setFixedSize(
            self._current_song_and_sound_width - CURRENT_SONG_COVER_SIZE - CURRENT_SONG_LAYOUT_SPACING,
            TITLE_AUTHOR_WIDGET_HEIGHT
        )
        self._title_author_widget.setContentsMargins(0, 0, 0, 0)
        self._current_song_layout.addWidget(self._title_author_widget)

        self._title_author_layout = QVBoxLayout()
        self._title_author_layout.setSpacing(TITLE_AUTHOR_LAYOUT_SPACING)
        self._title_author_layout.setContentsMargins(0, 0, 0, 0)
        self._title_author_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._title_author_widget.setLayout(self._title_author_layout)

        self._title_label = QLabel(
            self._current_song.song_title if self._current_song.song_title != "" else
            self._current_song.file_name
        )
        self._title_label.setObjectName("current_song_title_label")
        self._title_label.setStyleSheet(self._styles)
        self._title_label.setIndent(0)
        self._title_label.setFixedSize(
            self._current_song_and_sound_width - CURRENT_SONG_COVER_SIZE - CURRENT_SONG_LAYOUT_SPACING,
            CURRENT_SONG_TITLE_LABEL
        )
        self._title_label.setContentsMargins(0, 0, 0, 0)
        self._title_author_layout.addWidget(self._title_label)

        if self._current_song.song_author != "":
            self._author_label = QLabel(self._current_song.song_author)
            self._author_label.setObjectName("current_song_author_label")
            self._author_label.setStyleSheet(self._styles)
            self._author_label.setContentsMargins(0, 0, 0, 0)
            self._author_label.setFixedSize(
                self._current_song_and_sound_width - CURRENT_SONG_COVER_SIZE - CURRENT_SONG_LAYOUT_SPACING,
                CURRENT_SONG_TITLE_LABEL)
            self._author_label.setIndent(0)
            self._title_author_layout.addWidget(self._author_label)

    def _create_controls_widget(self):
        self._controls_widget = QWidget()
        self._controls_widget.setContentsMargins(0, 0, 0, 0)
        self._controls_widget.setFixedWidth(config.SLIDER_BLOCK_WIDTH)
        self._layout.addWidget(self._controls_widget)

        self._controls_layout = QVBoxLayout()
        self._controls_layout.setSpacing(CONTROLS_LAYOUT_SPACING)
        self._controls_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._controls_layout.setContentsMargins(0, 0, 0, 0)
        self._controls_widget.setLayout(self._controls_layout)
        self._create_buttons()
        self._create_slider()

    def _create_buttons(self):
        self._control_buttons_widget = QWidget()
        self._control_buttons_widget.setContentsMargins(0, 0, 0, 0)
        self._control_buttons_widget.setFixedSize(config.SLIDER_BLOCK_WIDTH, CONTROL_BUTTONS_WIDGET_HEIGHT)
        self._controls_layout.addWidget(self._control_buttons_widget)

        self._control_buttons_layout = QHBoxLayout()
        self._control_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self._control_buttons_layout.setSpacing(CONTROL_BUTTONS_LAYOUT_SPACING)
        self._control_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._control_buttons_widget.setLayout(self._control_buttons_layout)

        self._shuffle_button = QPushButton(QIcon("common/assets/shuffle_inactive.svg"), "")
        self._shuffle_button.setObjectName("shuffle_button")
        self._shuffle_button.setStyleSheet(self._styles)
        self._shuffle_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._shuffle_button.setFixedSize(CONTROL_BUTTON_SIZE, CONTROL_BUTTON_SIZE)
        self._shuffle_button.clicked.connect(self._shuffle_songs)
        self._control_buttons_layout.addWidget(self._shuffle_button)

        self._play_prev_button = QPushButton("")
        self._play_prev_button.setObjectName("play_prev_button")
        self._play_prev_button.setStyleSheet(self._styles)
        self._play_prev_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._play_prev_button.setFixedSize(CONTROL_BUTTON_SIZE, CONTROL_BUTTON_SIZE)
        self._play_prev_button.clicked.connect(self._play_prev)
        self._control_buttons_layout.addWidget(self._play_prev_button)

        self._play_button = QPushButton(QIcon("common/assets/play_active.svg"), "")
        self._play_button.setObjectName("play_button")
        self._play_button.setStyleSheet(self._styles)
        self._play_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._play_button.setFixedSize(PLAY_BUTTON_SIZE, PLAY_BUTTON_SIZE)
        self._play_button.clicked.connect(self._play_song)
        self._control_buttons_layout.addWidget(self._play_button)

        self._play_next_button = QPushButton("")
        self._play_next_button.setObjectName("play_next_button")
        self._play_next_button.setStyleSheet(self._styles)
        self._play_next_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._play_next_button.setFixedSize(CONTROL_BUTTON_SIZE, CONTROL_BUTTON_SIZE)
        self._play_next_button.clicked.connect(self._play_next)
        self._control_buttons_layout.addWidget(self._play_next_button)

        self._cycle_button = QPushButton(QIcon("common/assets/cycle.svg"), "")
        self._cycle_button.setObjectName("cycle_button")
        self._cycle_button.setStyleSheet(self._styles)
        self._cycle_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._cycle_button.setFixedSize(CONTROL_BUTTON_SIZE, CONTROL_BUTTON_SIZE)
        self._cycle_button.clicked.connect(self._cycle)
        self._control_buttons_layout.addWidget(self._cycle_button)

        self._update_prev_next_buttons()

    def _create_slider(self):
        self._control_slider_widget = QWidget()
        self._control_slider_widget.setContentsMargins(0, 0, 0, 0)
        self._control_slider_widget.setFixedSize(config.SLIDER_BLOCK_WIDTH, CONTROL_SLIDER_WIDGET_HEIGHT)
        self._controls_layout.addWidget(self._control_slider_widget)

        self._control_slider_layout = QHBoxLayout()
        self._control_slider_layout.setContentsMargins(0, 0, 0, 0)
        self._control_slider_layout.setSpacing(CONTROL_SLIDER_LAYOUT_SPACING)
        self._control_slider_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._control_slider_widget.setLayout(self._control_slider_layout)

        self._current_time_label = QLabel(" 0:00")
        self._current_time_label.setObjectName("current_playback_time_label")
        self._current_time_label.setStyleSheet(self._styles)
        self._control_slider_layout.addWidget(self._current_time_label)

        self._playback_slider = QSlider(Qt.Orientation.Horizontal)
        self._playback_slider.setStyleSheet(self._styles)
        self._playback_slider.sliderMoved.connect(self._set_position)
        self._control_slider_layout.addWidget(self._playback_slider)

        self._total_time_label = QLabel(self._current_song.song_duration)
        self._total_time_label.setObjectName("total_playback_time_label")
        self._total_time_label.setStyleSheet(self._styles)
        self._control_slider_layout.addWidget(self._total_time_label)

    def _create_sound_controls_widget(self):
        self._sound_controls_widget = QWidget()
        self._sound_controls_widget.setContentsMargins(
            self._current_song_and_sound_width -
            SOUND_SLIDER_WIDTH -
            SOUND_CONTROLS_LAYOUT_SPACING -
            SOUND_ICON_SIZE,
            0,
            0,
            0
        )
        self._sound_controls_widget.setFixedWidth(self._current_song_and_sound_width)
        self._layout.addWidget(self._sound_controls_widget)

        self._sound_controls_layout = QHBoxLayout()
        self._sound_controls_layout.setContentsMargins(0, 0, 0, 0)
        self._sound_controls_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self._sound_controls_layout.setSpacing(SOUND_CONTROLS_LAYOUT_SPACING)
        self._sound_controls_widget.setLayout(self._sound_controls_layout)

        self._sound_icon = QSvgWidget("common/assets/sound.svg")
        self._sound_icon.setFixedSize(SOUND_ICON_SIZE, SOUND_ICON_SIZE)
        self._sound_controls_layout.addWidget(self._sound_icon)

        self._sound_slider = QSlider(Qt.Orientation.Horizontal)
        self._sound_slider.setStyleSheet(self._styles)
        self._sound_slider.setRange(SOUND_RANGE_MIN, SOUND_RANGE_MAX)
        self._sound_slider.sliderMoved.connect(self._set_volume)
        self._sound_slider.setValue(INIT_VOLUME)
        self._set_volume(INIT_VOLUME)
        self._sound_controls_layout.addWidget(self._sound_slider)

    def _set_cover(self):
        if self._current_song.song_cover_bytes is not None:
            cover_image = QImage.fromData(self._current_song.song_cover_bytes)
            cover_pixmap = QPixmap.fromImage(cover_image)
        else:
            cover_pixmap = QPixmap("common/assets/placeholder.png")
        cover_pixmap_scaled = cover_pixmap.scaled(
            CURRENT_SONG_COVER_SIZE,
            CURRENT_SONG_COVER_SIZE,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio
        )
        self._cover_label.setPixmap(cover_pixmap_scaled)

    def _set_current_song(self, song):
        self._current_song = song
        self._title_label.setText(song.song_title)
        if song.song_author:
            self._author_label.setText(song.song_author)
        else:
            self._author_label.setVisible(False)
        self._set_cover()

    def _set_source(self, file_path):
        self._media_player.setSource(QUrl.fromLocalFile(file_path))

    def _position_changed(self, position):
        self._playback_slider.setValue(position)
        self._refresh_current_time_label(position)

    def _source_changed(self):
        self._update_prev_next_buttons()
        current_song = self._media_player.get_current_song()
        self._set_current_song(current_song)

    def _set_position(self, position):
        self._media_player.setPosition(position)
        self._refresh_current_time_label(position)

    def _refresh_current_time_label(self, position):
        current_second, _ = divmod(position, 1000)
        if self._current_song_second != current_second:
            self._current_time_label.setText(str(number_to_mins_and_secs(current_second)))
            self._current_song_second = current_second

    def _play_song(self):
        if self._media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self._media_player.pause()
            self._play_button.setIcon(QIcon("common/assets/play_active.svg"))
        else:
            self._media_player.play()
            self._play_button.setIcon(QIcon("common/assets/pause_active.svg"))

    def _set_duration(self, duration):
        self._playback_slider.setRange(SOUND_RANGE_MIN, duration)
        self._total_time_label.setText(self._current_song.song_duration)

    def _set_prev_button_disabled(self):
        self._play_prev_button.setDisabled(True)
        self._play_prev_button.setIcon(QIcon("common/assets/play_prev_inactive.svg"))

    def _set_prev_button_active(self):
        self._play_prev_button.setDisabled(False)
        self._play_prev_button.setIcon(QIcon("common/assets/play_prev_active.svg"))

    def _set_next_button_disabled(self):
        self._play_next_button.setDisabled(True)
        self._play_next_button.setIcon(QIcon("common/assets/play_next_inactive.svg"))

    def _set_next_button_active(self):
        self._play_next_button.setDisabled(False)
        self._play_next_button.setIcon(QIcon("common/assets/play_next_active.svg"))

    def _set_volume(self, volume):
        self._media_player.set_volume(volume)

    def _play_next(self):
        self._set_prev_button_active()
        self._media_player.play_next()
        current_song = self._media_player.get_current_song()
        self._set_current_song(current_song)

        if self._media_player.is_current_song_last() and not self._media_player.cycling():
            self._set_next_button_disabled()

    def _play_prev(self):
        self._set_next_button_active()
        self._media_player.play_prev()
        current_song = self._media_player.get_current_song()
        self._set_current_song(current_song)
        if self._media_player.is_current_song_first() and not self._media_player.cycling():
            self._set_prev_button_disabled()

    def _cycle(self):
        if self._media_player.cycling():
            self._media_player.cycle_one_song()
        elif self._media_player.cycling():
            self._media_player.uncycle()
        else:
            self._media_player.cycle_playlist()

    def _shuffle_songs(self):
        if self._media_player.get_shuffled():
            self._media_player.unshuffle()
        else:
            self._media_player.shuffle()

    def _playback_state_changed(self):
        if self._media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self._play_button.setIcon(QIcon("common/assets/pause_active.svg"))
        else:
            self._play_button.setIcon(QIcon("common/assets/play_active.svg"))

    def _sound_position_changed(self, position):
        self._sound_slider.setValue(int(position * 100))

    def _update_prev_next_buttons(self):
        if self._media_player.is_current_song_first() and self._media_player.cycling != Cycling.PLAYLIST_CYCLED:
            self._set_prev_button_disabled()
        else:
            self._set_prev_button_active()

        if self._media_player.is_current_song_last() and self._media_player.cycling != Cycling.PLAYLIST_CYCLED:
            self._set_next_button_disabled()
        else:
            self._set_next_button_active()

    def _cycling_changed(self):
        if self._media_player.cycling() and self._media_player.cycling == Cycling.PLAYLIST_CYCLED:
            self._cycle_button.setIcon(QIcon("common/assets/cycle_list.svg"))
        elif not self._media_player.cycling() and self._media_player.cycling == Cycling.SONG_CYCLED:
            self._cycle_button.setIcon(QIcon("common/assets/cycle_one.svg"))
        elif not self._media_player.cycling() and self._media_player.cycling == Cycling.NO_CYCLING:
            self._cycle_button.setIcon(QIcon("common/assets/cycle.svg"))

        self._update_prev_next_buttons()

    def _shuffling_changed(self):
        if self._media_player.shuffled:
            self._shuffle_button.setIcon(QIcon("common/assets/shuffle_active.svg"))
        else:
            self._shuffle_button.setIcon(QIcon("common/assets/shuffle_inactive.svg"))

        self._update_prev_next_buttons()
        
    def _song_deleted(self, _):
        self._update_prev_next_buttons()

    def _songs_added(self, _):
        self._update_prev_next_buttons()

