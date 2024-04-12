from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtWidgets import QMenuBar, QMenu, QApplication, QFileDialog, QMessageBox

import config
from common.utils.files import clone_and_rename_file

VOLUME_CHANGE_VALUE = 0.05


class MenuBar(QMenuBar):
    songs_added = pyqtSignal()

    def __init__(self):
        super().__init__()
        with open("./pyqt/elements/menuBar/menuBar.css", "r") as file:
            self.__styles = file.read()
        self.setStyleSheet(self.__styles)
        self.__media_player = None
        self.__create_actions()
        self.__create_menu()

    def __create_menu(self):
        self.__file_menu = QMenu("Plik")
        self.__file_menu.setStyleSheet(self.__styles)
        self.__file_menu.addAction(self.__add_file_action)
        self.__file_menu.addSeparator()
        self.__file_menu.addAction(self.__exit_action)

        self.__actions = {
            "play/pause": [self.__play_action],
            "prev/next": [self.__prev_action, self.__next_action],
            "shuffle/cycle": [self.__shuffle_action, self.__cycle_playlist_action],
            "quieter/louder": [self.__quiet_action, self.__loud_action]
        }

        self.__playback_menu = QMenu("Odtwarzanie")
        self.__playback_menu.setStyleSheet(self.__styles)
        self.__playback_menu.setDisabled(True)
        self.__update_playback_menu()

        self.__about_action = QAction("Opis")
        self.__about_action.triggered.connect(self.__show_about_window)

        self.addMenu(self.__file_menu)
        self.addMenu(self.__playback_menu)
        self.addAction(self.__about_action)

    def __create_actions(self):
        self.__add_file_action = QAction("Dodaj pliki")
        self.__add_file_action.triggered.connect(self.__add_music_files_action)

        self.__exit_action = QAction("Wyjdź")
        self.__exit_action.triggered.connect(QApplication.instance().quit)

        self.__stop_action = QAction("Pauza")

        self.__play_action = QAction("Odtwarzaj")

        self.__prev_action = QAction("Poprzednia")

        self.__next_action = QAction("Następna")

        self.__shuffle_action = QAction("Przetasuj")

        self.__unshuffle_action = QAction("Nie tasuj")

        self.__cycle_playlist_action = QAction("Powtarzaj listę")

        self.__cycle_one_song_action = QAction("Powtarzaj jedną")

        self.__uncycle_action = QAction("Nie powtarzaj")

        self.__quiet_action = QAction("Ciszej")

        self.__loud_action = QAction("Głośniej")

    def __add_music_files_action(self):
        file_filter = " ".join(map(lambda s: f"*.{s}", config.MUSIC_FILE_FORMATS))
        file_dialog = QFileDialog.getOpenFileNames(self, "Select audio files", "", file_filter)
        filenames = file_dialog[0]
        if self.__media_player is None:
            last_song_number = 0
        else:
            last_song_number = int(self.__media_player.get_songs()[-1].file_name.split(".")[0])
        for index, filename in enumerate(filenames):
            clone_and_rename_file(filename, config.MUSIC_FOLDER_PATH, last_song_number + index + 1)

        if len(filenames) > 0:
            self.songs_added.emit()

    def __empty_playback_menu(self):
        for action in self.__playback_menu.actions():
            self.__playback_menu.removeAction(action)

    def __update_playback_menu(self):
        action_lists = self.__actions.values()
        for action_list in action_lists:
            self.__playback_menu.addActions(action_list)
            self.__playback_menu.addSeparator()

    def __volume_down(self):
        current_volume = self.__media_player.audioOutput().volume()
        _, diff = divmod(round(current_volume, 2), VOLUME_CHANGE_VALUE)
        if diff != 0:
            self.__media_player.audioOutput().setVolume(round(current_volume, 2) - diff)
        else:
            self.__media_player.audioOutput().setVolume(round(current_volume, 2) - VOLUME_CHANGE_VALUE)

    def __volume_up(self):
        current_volume = self.__media_player.audioOutput().volume()
        _, diff = divmod(round(current_volume, 2), VOLUME_CHANGE_VALUE)
        if diff != 0:
            self.__media_player.audioOutput().setVolume(round(current_volume, 2) + VOLUME_CHANGE_VALUE - diff)
        else:
            self.__media_player.audioOutput().setVolume(round(current_volume, 2) + VOLUME_CHANGE_VALUE)

    def __playback_state_changed(self):
        self.__empty_playback_menu()
        if self.__media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.__actions["play/pause"] = [self.__stop_action]
        else:
            self.__playback_menu.removeAction(self.__play_action)
            self.__actions["play/pause"] = [self.__play_action]
        self.__update_playback_menu()

    def __cycle_playlist(self):
        self.__media_player.cycle_playlist()

    def __uncycle(self):
        self.__media_player.uncycle()

    def __cycle_one_song(self):
        self.__media_player.cycle_one_song()

    def __volume_changed(self, position):
        if position == 0.0:
            self.__empty_playback_menu()
            self.__actions["quieter/louder"].remove(self.__quiet_action)
            self.__update_playback_menu()
        elif 0 < position < 1.0:

            self.__empty_playback_menu()
            if self.__actions["quieter/louder"].count(self.__quiet_action) == 0:
                self.__actions["quieter/louder"][0] = self.__quiet_action

            if self.__actions["quieter/louder"].count(self.__loud_action) == 0:
                self.__actions["quieter/louder"].append(self.__loud_action)
            self.__update_playback_menu()
        else:
            self.__empty_playback_menu()
            self.__actions["quieter/louder"].remove(self.__loud_action)
            self.__update_playback_menu()

    def __source_changed(self):
        self.__update_nex_prev_actions()

    def __update_nex_prev_actions(self):
        if self.__media_player.is_current_song_first() and not self.__media_player.get_cycled_playlist():
            self.__empty_playback_menu()
            if self.__actions["prev/next"].count(self.__prev_action) > 0:
                self.__actions["prev/next"].remove(self.__prev_action)
            self.__update_playback_menu()
        else:
            self.__empty_playback_menu()
            if self.__actions["prev/next"].count(self.__prev_action) == 0 and len(self.__actions["prev/next"]) > 0:
                self.__actions["prev/next"][0] = self.__prev_action
            elif self.__actions["prev/next"].count(self.__prev_action) == 0:
                self.__actions["prev/next"].append(self.__prev_action)
            self.__update_playback_menu()

        if self.__media_player.is_current_song_last() and not self.__media_player.get_cycled_playlist():
            self.__empty_playback_menu()
            if self.__actions["prev/next"].count(self.__next_action) > 0:
                self.__actions["prev/next"].remove(self.__next_action)
            self.__update_playback_menu()
        else:
            self.__empty_playback_menu()
            if self.__actions["prev/next"].count(self.__next_action) == 0:
                self.__actions["prev/next"].append(self.__next_action)
            self.__update_playback_menu()

    def __cycling_changed(self):
        self.__empty_playback_menu()
        if self.__media_player.get_cycled_playlist():
            self.__actions["shuffle/cycle"][1] = self.__cycle_one_song_action
        elif self.__media_player.get_cycled_one_song():
            self.__actions["shuffle/cycle"][1] = self.__uncycle_action
        elif not self.__media_player.get_cycled_playlist() and not self.__media_player.get_cycled_one_song():
            self.__actions["shuffle/cycle"][1] = self.__cycle_playlist_action
        self.__update_playback_menu()
        self.__update_nex_prev_actions()

    def __shuffling_changed(self):
        self.__empty_playback_menu()
        if self.__media_player.get_shuffled():
            self.__actions["shuffle/cycle"][0] = self.__unshuffle_action
        else:
            self.__actions["shuffle/cycle"][0] = self.__shuffle_action
        self.__update_playback_menu()
        self.__update_nex_prev_actions()

    def __song_deleted(self, _):
        self.__update_nex_prev_actions()

    def __songs_added(self, _):
        self.__update_nex_prev_actions()

    def set_media_player(self, media_player):
        self.__media_player = media_player

        self.__media_player.cycling_changed.connect(self.__cycling_changed)
        self.__media_player.shuffling_changed.connect(self.__shuffling_changed)
        self.__media_player.song_deleted.connect(self.__song_deleted)
        self.__media_player.playbackStateChanged.connect(self.__playback_state_changed)
        self.__media_player.audioOutput().volumeChanged.connect(self.__volume_changed)
        self.__media_player.sourceChanged.connect(self.__source_changed)
        self.__media_player.songs_added.connect(self.__songs_added)

        self.__stop_action.triggered.connect(self.__media_player.pause)
        self.__play_action.triggered.connect(self.__media_player.play)
        self.__prev_action.triggered.connect(self.__media_player.play_prev)
        self.__next_action.triggered.connect(self.__media_player.play_next)
        self.__shuffle_action.triggered.connect(self.__media_player.shuffle)
        self.__unshuffle_action.triggered.connect(self.__media_player.unshuffle)
        self.__cycle_playlist_action.triggered.connect(self.__cycle_playlist)
        self.__cycle_one_song_action.triggered.connect(self.__cycle_one_song)
        self.__uncycle_action.triggered.connect(self.__uncycle)
        self.__quiet_action.triggered.connect(self.__volume_down)
        self.__loud_action.triggered.connect(self.__volume_up)

        self.__playback_menu.setDisabled(False)

    def __show_about_window(self):
        msg_box = QMessageBox()
        msg_box.setStyleSheet(self.__styles)
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
