from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtWidgets import QMenuBar, QMenu, QApplication, QFileDialog, QMessageBox

import config
from common.classes.Cycling import Cycling
from common.utils.files import clone_and_rename_file

VOLUME_CHANGE_VALUE = 5.0


class MenuBar(QMenuBar):
    songs_added = pyqtSignal()

    def __init__(self):
        super().__init__()
        with open("./pyqt/elements/menuBar/MenuBar.css", "r") as file:
            self._styles = file.read()
        self.setStyleSheet(self._styles)
        self._media_player = None
        self._create_actions()
        self._create_menu()

    def _create_menu(self):
        self._file_menu = QMenu("Plik")
        self._file_menu.setStyleSheet(self._styles)
        self._file_menu.addAction(self._add_file_action)
        self._file_menu.addSeparator()
        self._file_menu.addAction(self._exit_action)

        self._actions = {
            "play/pause": [self._play_action],
            "prev/next": [self._prev_action, self._next_action],
            "shuffle/cycle": [self._shuffle_action, self._cycle_playlist_action],
            "quieter/louder": [self._quiet_action, self._loud_action]
        }

        self._playback_menu = QMenu("Odtwarzanie")
        self._playback_menu.setStyleSheet(self._styles)
        self._playback_menu.setDisabled(True)
        self._update_playback_menu()

        self._about_action = QAction("Opis")
        self._about_action.triggered.connect(self._show_about_window)

        self.addMenu(self._file_menu)
        self.addMenu(self._playback_menu)
        self.addAction(self._about_action)

    def _create_actions(self):
        self._add_file_action = QAction("Dodaj pliki")
        self._add_file_action.triggered.connect(self._add_music_files_action)

        self._exit_action = QAction("Wyjdź")
        self._exit_action.triggered.connect(QApplication.instance().quit)

        self._stop_action = QAction("Pauza")

        self._play_action = QAction("Odtwarzaj")

        self._prev_action = QAction("Poprzednia")

        self._next_action = QAction("Następna")

        self._shuffle_action = QAction("Przetasuj")

        self._unshuffle_action = QAction("Nie tasuj")

        self._cycle_playlist_action = QAction("Powtarzaj listę")

        self._cycle_one_song_action = QAction("Powtarzaj jedną")

        self._uncycle_action = QAction("Nie powtarzaj")

        self._quiet_action = QAction("Ciszej")

        self._loud_action = QAction("Głośniej")

    def _add_music_files_action(self):
        file_filter = " ".join(map(lambda s: f"*.{s}", config.MUSIC_FILE_FORMATS))
        file_dialog = QFileDialog.getOpenFileNames(self, "Wybierz pliki dźwiękowe", "", file_filter)
        filenames = file_dialog[0]
        if self._media_player is None:
            last_song_number = 0
        else:
            last_song_number = int(self._media_player.songs[-1].file_name.split(".")[0])
        for index, filename in enumerate(filenames):
            clone_and_rename_file(filename, config.MUSIC_FOLDER_PATH, last_song_number + index + 1)

        if len(filenames) > 0:
            self.songs_added.emit()

    def _empty_playback_menu(self):
        for action in self._playback_menu.actions():
            self._playback_menu.removeAction(action)

    def _update_playback_menu(self):
        action_lists = self._actions.values()
        for action_list in action_lists:
            self._playback_menu.addActions(action_list)
            self._playback_menu.addSeparator()

    def _volume_down(self):
        current_volume = self._media_player.audioOutput().volume() * 100
        _, diff = divmod(round(current_volume, 2), VOLUME_CHANGE_VALUE)
        if diff != 0:
            self._media_player.set_volume(round(current_volume, 2) - diff)
        else:
            self._media_player.set_volume(round(current_volume, 2) - VOLUME_CHANGE_VALUE)

    def _volume_up(self):
        current_volume = self._media_player.audioOutput().volume() * 100
        _, diff = divmod(round(current_volume, 2), VOLUME_CHANGE_VALUE)
        if diff != 0:
            self._media_player.set_volume(round(current_volume, 2) + VOLUME_CHANGE_VALUE - diff)
        else:
            self._media_player.set_volume(round(current_volume, 2) + VOLUME_CHANGE_VALUE)

    def _playback_state_changed(self):
        self._empty_playback_menu()
        if self._media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self._actions["play/pause"] = [self._stop_action]
        else:
            self._playback_menu.removeAction(self._play_action)
            self._actions["play/pause"] = [self._play_action]
        self._update_playback_menu()

    def _cycle_playlist(self):
        self._media_player.cycle_playlist()

    def _uncycle(self):
        self._media_player.uncycle()

    def _cycle_one_song(self):
        self._media_player.cycle_one_song()

    def _volume_changed(self, position):
        if position == 0.0 and self._actions["quieter/louder"].count(self._quiet_action) != 0:
            self._empty_playback_menu()
            self._actions["quieter/louder"].remove(self._quiet_action)
            self._update_playback_menu()
        elif 0 < position < 1.0:
            self._empty_playback_menu()
            if self._actions["quieter/louder"].count(self._quiet_action) == 0:
                self._actions["quieter/louder"][0] = self._quiet_action

            if self._actions["quieter/louder"].count(self._loud_action) == 0:
                self._actions["quieter/louder"].append(self._loud_action)
            self._update_playback_menu()
        elif self._actions["quieter/louder"].count(self._loud_action) != 0:
            self._empty_playback_menu()
            self._actions["quieter/louder"].remove(self._loud_action)
            self._update_playback_menu()

    def _source_changed(self):
        self._update_nex_prev_actions()

    def _update_nex_prev_actions(self):
        if self._media_player.is_current_song_first() and self._media_player.cycling != Cycling.PLAYLIST_CYCLED:
            self._empty_playback_menu()
            if self._actions["prev/next"].count(self._prev_action) > 0:
                self._actions["prev/next"].remove(self._prev_action)
            self._update_playback_menu()
        else:
            self._empty_playback_menu()
            if self._actions["prev/next"].count(self._prev_action) == 0 and len(self._actions["prev/next"]) > 0:
                self._actions["prev/next"][0] = self._prev_action
            elif self._actions["prev/next"].count(self._prev_action) == 0:
                self._actions["prev/next"].append(self._prev_action)
            self._update_playback_menu()

        if self._media_player.is_current_song_last() and self._media_player.cycling != Cycling.PLAYLIST_CYCLED:
            self._empty_playback_menu()
            if self._actions["prev/next"].count(self._next_action) > 0:
                self._actions["prev/next"].remove(self._next_action)
            self._update_playback_menu()
        else:
            self._empty_playback_menu()
            if self._actions["prev/next"].count(self._next_action) == 0:
                self._actions["prev/next"].append(self._next_action)
            self._update_playback_menu()

    def _cycling_changed(self):
        self._empty_playback_menu()
        if self._media_player.cycling == Cycling.PLAYLIST_CYCLED:
            self._actions["shuffle/cycle"][1] = self._cycle_one_song_action
        elif self._media_player.cycling != Cycling.SONG_CYCLED:
            self._actions["shuffle/cycle"][1] = self._uncycle_action
        elif self._media_player.cycling != Cycling.NO_CYCLING:
            self._actions["shuffle/cycle"][1] = self._cycle_playlist_action
        self._update_playback_menu()
        self._update_nex_prev_actions()

    def _shuffling_changed(self):
        self._empty_playback_menu()
        if self._media_player.shuffled:
            self._actions["shuffle/cycle"][0] = self._unshuffle_action
        else:
            self._actions["shuffle/cycle"][0] = self._shuffle_action
        self._update_playback_menu()
        self._update_nex_prev_actions()

    def _song_deleted(self, _):
        self._update_nex_prev_actions()

    def _songs_added(self, _):
        self._update_nex_prev_actions()

    def set_media_player(self, media_player):
        self._media_player = media_player

        self._media_player.cycling_changed.connect(self._cycling_changed)
        self._media_player.shuffling_changed.connect(self._shuffling_changed)
        self._media_player.song_deleted.connect(self._song_deleted)
        self._media_player.playbackStateChanged.connect(self._playback_state_changed)
        self._media_player.audioOutput().volumeChanged.connect(self._volume_changed)
        self._media_player.sourceChanged.connect(self._source_changed)
        self._media_player.songs_added.connect(self._songs_added)

        self._stop_action.triggered.connect(self._media_player.pause)
        self._play_action.triggered.connect(self._media_player.play)
        self._prev_action.triggered.connect(self._media_player.play_prev)
        self._next_action.triggered.connect(self._media_player.play_next)
        self._shuffle_action.triggered.connect(self._media_player.shuffle)
        self._unshuffle_action.triggered.connect(self._media_player.unshuffle)
        self._cycle_playlist_action.triggered.connect(self._cycle_playlist)
        self._cycle_one_song_action.triggered.connect(self._cycle_one_song)
        self._uncycle_action.triggered.connect(self._uncycle)
        self._quiet_action.triggered.connect(self._volume_down)
        self._loud_action.triggered.connect(self._volume_up)

        self._playback_menu.setDisabled(False)

    def _show_about_window(self):
        msg_box = QMessageBox()
        msg_box.setStyleSheet(self._styles)
        msg_box.setText("Aplikacja przedstawia sobą odtwarzacz muzyki, który pozwala wybierać pliki do odtwarzania, "
                        "formując playlistę, po czym pozwala:\n"
                        " - odtwarzac piosenki,\n"
                        " - spyniać odtwarzanie,\n"
                        " - przechodzić do następnej/poprzedniej piosenki w playliście,\n"
                        " - ustawiać/usuwać losową kolejnośc odtwarzania piosenek,\n"
                        " - ustawiać/usuwać nieskończone powtarzanie jednej piosenki/całej playlisty,\n"
                        " - ustawiać moment piosenki od którego rozpocząć odtwarzanie,\n"
                        " - ustawiać poziom głosności,\n"
                        " - usuwać piosenki.\n"
                        "Powyższe funkcjonalności są wykonywane za pomocą przycisków na płytkach reprezentujących "
                        "piosenki, przycisków na dole okna aplikacji oraz menu Odtwarzanie w pasku menu.")
        msg_box.setWindowTitle("Opis aplikacji")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        return_value = msg_box.exec()
        if return_value == QMessageBox.StandardButton.Ok:
            msg_box.close()
