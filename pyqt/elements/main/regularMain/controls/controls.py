from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

import config


class Controls(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(90)
        self.setFixedWidth(config.WINDOW_WIDTH)
        self.styles = None
        with open("pyqt/elements/main/regularMain/controls/controls.css", "r") as file:
            self.styles = file.read()
        self.setStyleSheet(self.styles)
        self.setObjectName("controls")
        self._layout = None
        self._current_song_layout = None
        self._controls_layout = None
        self._sound_controls_layout = None
        self._create_UI()

    def _create_UI(self):
        self._layout = QHBoxLayout()
        self._create_current_song_layout()

    def _create_current_song_layout(self):
        self._current_song_layout = QHBoxLayout()

    def _create_controls_layout(self):
        self._controls_layout = QVBoxLayout()

    def _create_sound_controls_layout(self):
        self._sound_controls_layout = QHBoxLayout()

