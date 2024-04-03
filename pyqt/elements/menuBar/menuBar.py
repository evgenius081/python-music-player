from PyQt6.QtCore import QCoreApplication, pyqtSignal
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMenuBar, QMenu, QApplication, QFileDialog

import config
from common.utils.files import clone_file


class MenuBar(QMenuBar):
    refresh_signal = pyqtSignal()

    def __init__(self, parent, refresh_slot):
        super().__init__(parent)
        with open("./pyqt/elements/menuBar/menuBar.css", "r") as file:
            self.styles = file.read()
        self.setStyleSheet(self.styles)
        self.refresh_signal.connect(refresh_slot)
        self._create_actions()
        self._create_menu()

    def _create_menu(self):
        file_menu = QMenu("&Plik", self)
        file_menu.setStyleSheet(self.styles)
        file_menu.addAction(self.add_file_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        playback_menu = QMenu("&Odtwarzanie", self)
        playback_menu.setStyleSheet(self.styles)
        playback_menu.addAction(self.play_action)
        file_menu.addSeparator()
        playback_menu.addAction(self.prev_action)
        playback_menu.addAction(self.next_action)
        file_menu.addSeparator()
        playback_menu.addAction(self.shuffle_action)
        playback_menu.addAction(self.repeatList_action)
        file_menu.addSeparator()
        playback_menu.addAction(self.quiet_action)
        playback_menu.addAction(self.loud_action)

        about_menu = QMenu("&Opis", self)
        about_menu.setStyleSheet(self.styles)
        self.addMenu(file_menu)
        self.addMenu(playback_menu)
        self.addMenu(about_menu)

    def _create_actions(self):
        self.add_file_action = QAction(QIcon("pyqt/assets/add_file.svg"), "&Dodaj pliki")
        self.add_file_action.triggered.connect(self._add_music_files_action)
        self.exit_action = QAction(QIcon("pyqt/assets/exit.svg"), "&Wyjdź")
        self.exit_action.triggered.connect(QApplication.instance().quit)
        self.stop_action = QAction(QIcon("pyqt/assets/pause.svg"), "&Pauza")
        self.play_action = QAction("&Odtwarzaj")
        self.prev_action = QAction("&Poprzednia")
        self.next_action = QAction("&Następna")
        self.shuffle_action = QAction("&Przetasowanie")
        self.stopShuffle_action = QAction("&?")
        self.repeatList_action = QAction("&Powtarzaj listę")
        self.repeatSingle_action = QAction("&Powtarzaj jedną")
        self.stopRepeat_action = QAction("&Nie powtarzaj")
        self.quiet_action = QAction("&Ciszej")
        self.loud_action = QAction("&Głośniej")

    def _add_music_files_action(self):
        file_filter = " ".join(map(lambda s: f"*.{s}", config.music_file_formats))
        file_dialog = QFileDialog.getOpenFileNames(self, "Select audio files", "", file_filter)
        filenames = file_dialog[0]
        for filename in filenames:
            clone_file(filename, config.MUSIC_ABSOLUTE_PATH)\

        if len(filenames) > 0:
            self.refresh_signal.emit()

