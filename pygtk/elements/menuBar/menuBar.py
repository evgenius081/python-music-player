import gi.repository
from gi.repository.Gio import Menu, MenuItem, MenuModel

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from gi.repository.Gtk import ActionBar, MenuButton, FileDialog

import config
from common.utils.files import clone_and_rename_file

VOLUME_CHANGE_VALUE = 0.05


class AMenuBar(ActionBar):
    # songs_added = pyqtSignal()

    def __init__(self):
        super().__init__()
        with open("./pyqt/elements/menuBar/menuBar.css", "r") as file:
            self.__styles = file.read()
        self.set_name("menu_bar")
        self.__media_player = None
        self.__create_actions()
        self.__create_menu()

    def __create_menu(self):
        self.__file_menu_button = MenuButton()
        self.__file_menu_button.set_label("Plik")
        self.pack_start(self.__file_menu_button)

        self.__playback_menu_button = MenuButton()
        self.__playback_menu_button.set_label("Odtwarzanie")
        self.pack_start(self.__playback_menu_button)

        self.__about_menu_button = MenuButton()
        self.__about_menu_button.set_label("Opis")
        self.pack_start(self.__about_menu_button)

        self.__file_menu = Menu()
        self.__file_menu.append("Dodaj pliki")
        self.__file_menu.append("Wyjdź")
        self.__file_menu_button.set_menu_model(self.__file_menu)

        self.__playback_menu = Menu()
        self.__playback_menu_button.set_menu_model(self.__playback_menu)

        self.__actions = {
            "play/pause": [self.__play_action],
            "prev/next": [self.__prev_action, self.__next_action],
            "shuffle/cycle": [self.__shuffle_action, self.__cycle_playlist_action],
            "quieter/louder": [self.__quiet_action, self.__loud_action]
        }

        self.__create_actions()
        self.__update_playback_menu()

    def __create_actions(self):
        self.__add_file_action = MenuItem.new("Dodaj pliki", None)

        self.__exit_action = MenuItem.new("Wyjdź", None)

        self.__stop_action = MenuItem.new("Pauza", None)

        self.__play_action = MenuItem.new("Odtwarzaj", None)

        self.__prev_action = MenuItem.new("Poprzednia", None)

        self.__next_action = MenuItem.new("Następna", None)

        self.__shuffle_action = MenuItem.new("Przetasuj", None)

        self.__unshuffle_action = MenuItem.new("Nie tasuj", None)

        self.__cycle_playlist_action = MenuItem.new("Powtarzaj listę", None)

        self.__cycle_one_song_action = MenuItem.new("Powtarzaj jedną", None)

        self.__uncycle_action = MenuItem.new("Nie powtarzaj", None)

        self.__quiet_action = MenuItem.new("Ciszej", None)

        self.__loud_action = MenuItem.new("Głośniej", None)

    def __add_music_files_action(self):
        file_filters = map(lambda s: f"*.{s}", config.MUSIC_FILE_FORMATS)
        dialog = Gtk.FileChooserNative.new(
            title="Wybierz pliki",
            parent=None,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.set_select_multiple(True)
        dialog.connect("response", self.__on_file_chosen)
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Pliki dźwiękowe")
        for file_filter in file_filters:
            filter_text.add_pattern(file_filter)
        dialog.add_filter(filter_text)
        dialog.show()

    def __on_file_chosen(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            if self.__media_player is None:
                last_song_number = 0
            else:
                last_song_number = int(self.__media_player.get_songs()[-1].file_name.split(".")[0])

            for index, file in enumerate(dialog.get_files()):
                clone_and_rename_file(file.get_path(), config.MUSIC_FOLDER_PATH, last_song_number + index + 1)
            # self.songs_added.emit()
        dialog.destroy()

    def __empty_playback_menu(self):
        self.__playback_menu.remove_all()

    def __update_playback_menu(self):
        action_lists = self.__actions.values()
        for action_list in action_lists:
            sub_menu = Menu()
            for action in action_list:
                sub_menu.append_item(action)
            self.__playback_menu.append_section(None, sub_menu)
    #
    # def __volume_down(self):
    #     current_volume = self.__media_player.audioOutput().volume()
    #     _, diff = divmod(round(current_volume, 2), VOLUME_CHANGE_VALUE)
    #     if diff != 0:
    #         self.__media_player.audioOutput().setVolume(round(current_volume, 2) - diff)
    #     else:
    #         self.__media_player.audioOutput().setVolume(round(current_volume, 2) - VOLUME_CHANGE_VALUE)
    #
    # def __volume_up(self):
    #     current_volume = self.__media_player.audioOutput().volume()
    #     _, diff = divmod(round(current_volume, 2), VOLUME_CHANGE_VALUE)
    #     if diff != 0:
    #         self.__media_player.audioOutput().setVolume(round(current_volume, 2) + VOLUME_CHANGE_VALUE - diff)
    #     else:
    #         self.__media_player.audioOutput().setVolume(round(current_volume, 2) + VOLUME_CHANGE_VALUE)
    #
    # def __playback_state_changed(self):
    #     self.__empty_playback_menu()
    #     if self.__media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
    #         self.__actions["play/pause"] = [self.__stop_action]
    #     else:
    #         self.__playback_menu.removeAction(self.__play_action)
    #         self.__actions["play/pause"] = [self.__play_action]
    #     self.__update_playback_menu()
    #
    # def __cycle_playlist(self):
    #     self.__media_player.cycle_playlist()
    #
    # def __uncycle(self):
    #     self.__media_player.uncycle()
    #
    # def __cycle_one_song(self):
    #     self.__media_player.cycle_one_song()
    #
    # def __volume_changed(self, position):
    #     if position == 0.0:
    #         self.__empty_playback_menu()
    #         self.__actions["quieter/louder"].remove(self.__quiet_action)
    #         self.__update_playback_menu()
    #     elif 0 < position < 1.0:
    #
    #         self.__empty_playback_menu()
    #         if self.__actions["quieter/louder"].count(self.__quiet_action) == 0:
    #             self.__actions["quieter/louder"][0] = self.__quiet_action
    #
    #         if self.__actions["quieter/louder"].count(self.__loud_action) == 0:
    #             self.__actions["quieter/louder"].append(self.__loud_action)
    #         self.__update_playback_menu()
    #     else:
    #         self.__empty_playback_menu()
    #         self.__actions["quieter/louder"].remove(self.__loud_action)
    #         self.__update_playback_menu()
    #
    # def __source_changed(self):
    #     self.__update_nex_prev_actions()
    #
    # def __update_nex_prev_actions(self):
    #     if self.__media_player.is_current_song_first() and not self.__media_player.get_cycled_playlist():
    #         self.__empty_playback_menu()
    #         if self.__actions["prev/next"].count(self.__prev_action) > 0:
    #             self.__actions["prev/next"].remove(self.__prev_action)
    #         self.__update_playback_menu()
    #     else:
    #         self.__empty_playback_menu()
    #         if self.__actions["prev/next"].count(self.__prev_action) == 0 and len(self.__actions["prev/next"]) > 0:
    #             self.__actions["prev/next"][0] = self.__prev_action
    #         elif self.__actions["prev/next"].count(self.__prev_action) == 0:
    #             self.__actions["prev/next"].append(self.__prev_action)
    #         self.__update_playback_menu()
    #
    #     if self.__media_player.is_current_song_last() and not self.__media_player.get_cycled_playlist():
    #         self.__empty_playback_menu()
    #         if self.__actions["prev/next"].count(self.__next_action) > 0:
    #             self.__actions["prev/next"].remove(self.__next_action)
    #         self.__update_playback_menu()
    #     else:
    #         self.__empty_playback_menu()
    #         if self.__actions["prev/next"].count(self.__next_action) == 0:
    #             self.__actions["prev/next"].append(self.__next_action)
    #         self.__update_playback_menu()
    #
    # def __cycling_changed(self):
    #     self.__empty_playback_menu()
    #     if self.__media_player.get_cycled_playlist():
    #         self.__actions["shuffle/cycle"][1] = self.__cycle_one_song_action
    #     elif self.__media_player.get_cycled_one_song():
    #         self.__actions["shuffle/cycle"][1] = self.__uncycle_action
    #     elif not self.__media_player.get_cycled_playlist() and not self.__media_player.get_cycled_one_song():
    #         self.__actions["shuffle/cycle"][1] = self.__cycle_playlist_action
    #     self.__update_playback_menu()
    #     self.__update_nex_prev_actions()
    #
    # def __shuffling_changed(self):
    #     self.__empty_playback_menu()
    #     if self.__media_player.get_shuffled():
    #         self.__actions["shuffle/cycle"][0] = self.__unshuffle_action
    #     else:
    #         self.__actions["shuffle/cycle"][0] = self.__shuffle_action
    #     self.__update_playback_menu()
    #     self.__update_nex_prev_actions()
    #
    # def __song_deleted(self, _):
    #     self.__update_nex_prev_actions()
    #
    # def __songs_added(self, _):
    #     self.__update_nex_prev_actions()

    def set_media_player(self, media_player):
        self.__media_player = media_player
    #
    #     self.__media_player.cycling_changed.connect(self.__cycling_changed)
    #     self.__media_player.shuffling_changed.connect(self.__shuffling_changed)
    #     self.__media_player.song_deleted.connect(self.__song_deleted)
    #     self.__media_player.playbackStateChanged.connect(self.__playback_state_changed)
    #     self.__media_player.audioOutput().volumeChanged.connect(self.__volume_changed)
    #     self.__media_player.sourceChanged.connect(self.__source_changed)
    #     self.__media_player.songs_added.connect(self.__songs_added)
    #
    #     self.__stop_action.triggered.connect(self.__media_player.pause)
    #     self.__play_action.triggered.connect(self.__media_player.play)
    #     self.__prev_action.triggered.connect(self.__media_player.play_prev)
    #     self.__next_action.triggered.connect(self.__media_player.play_next)
    #     self.__shuffle_action.triggered.connect(self.__media_player.shuffle)
    #     self.__unshuffle_action.triggered.connect(self.__media_player.unshuffle)
    #     self.__cycle_playlist_action.triggered.connect(self.__cycle_playlist)
    #     self.__cycle_one_song_action.triggered.connect(self.__cycle_one_song)
    #     self.__uncycle_action.triggered.connect(self.__uncycle)
    #     self.__quiet_action.triggered.connect(self.__volume_down)
    #     self.__loud_action.triggered.connect(self.__volume_up)
    #
    #     self.__playback_menu.setDisabled(False)
    #
    # def __show_about_window(self):
    #     msg_box = QMessageBox()
    #     msg_box.setStyleSheet(self.__styles)
    #     msg_box.setText("Aplikacja przedstawia sobą odtwarzacz muzyki, który pozwala wybierać pliki do odtwarzania, "
    #                     "formując playlistę, po czym pozwala:\n"
    #                     " - odtwarzac piosenki,\n"
    #                     " - spyniać odtwarzanie,\n"
    #                     " - przechodzić do następnej/poprzedniej piosenki w playliście,\n"
    #                     " - ustawiać/usuwać losową kolejnośc odtwarzania piosenek,\n"
    #                     " - ustawiać/usuwać nieskończone powtarzanie jednej piosenki/całej playlisty,\n"
    #                     " - ustawiać moment piosenki od którego rozpocząć odtwarzanie,\n"
    #                     " - ustawiać poziom głosności,\n"
    #                     " - usuwać piosenki.\n"
    #                     "Powyższe funkcjonalności są wykonywane za pomocą przycisków na płytkach reprezentujących "
    #                     "piosenki, przycisków na dole okna aplikacji oraz menu Odtwarzanie w pasku menu.")
    #     msg_box.setWindowTitle("Opis aplikacji")
    #     msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    #
    #     return_value = msg_box.exec()
    #     if return_value == QMessageBox.StandardButton.Ok:
    #         msg_box.close()
