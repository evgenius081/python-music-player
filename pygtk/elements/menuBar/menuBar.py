import gi.repository
from gi.repository.Gio import Menu, MenuItem, MenuModel, Action, SimpleAction

from common.classes.Cycling import Cycling

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GObject, Gst
from gi.repository.Gtk import ActionBar, MenuButton, FileDialog, Button, HeaderBar, PopoverMenu

import config
from common.utils.files import clone_and_rename_file

VOLUME_CHANGE_VALUE = 5.0


class MenuBar(ActionBar):
    __gsignals__ = {
        'songs_added': (GObject.SignalFlags.DETAILED, GObject.TYPE_NONE, (GObject.TYPE_OBJECT,)),
    }

    def __init__(self, parent):
        super().__init__()
        self.set_name("menu_bar")
        self.__media_player = None
        self.__parent = parent
        self.__create_menu()

    def __create_menu(self):
        self.__file_menu = Menu.new()

        self.__file_popover_menu = PopoverMenu()
        self.__file_popover_menu.set_menu_model(self.__file_menu)

        self.__playback_popover_menu = PopoverMenu()

        self.__file_menu_button = MenuButton()
        self.__file_menu_button.set_label("Plik")
        self.__file_menu_button.set_popover(self.__file_popover_menu)
        self.pack_start(self.__file_menu_button)

        self.__playback_menu_button = MenuButton()
        self.__playback_menu_button.set_label("Odtwarzanie")
        self.__playback_menu_button.set_popover(self.__playback_popover_menu)
        self.pack_start(self.__playback_menu_button)

        self.__create_actions()
        self.__actions = {
            "play/pause": [self.__play_action],
            "prev/next": [self.__prev_action, self.__next_action],
            "shuffle/cycle": [self.__shuffle_action, self.__cycle_playlist_action],
            "quieter/louder": [self.__quiet_action, self.__loud_action]
        }
        self.__actions_labels = [
            (self.__add_file_action, "Dodaj pliki"),
            (self.__exit_action, "Wyjdź"),
            (self.__stop_action, "Pauza"),
            (self.__play_action,"Odtwarzaj"),
            (self.__prev_action, "Poprzednia"),
            (self.__next_action, "Następna"),
            (self.__shuffle_action, "Przetasuj"),
            (self.__unshuffle_action, "Nie tasuj"),
            (self.__cycle_playlist_action, "Powtarzaj listę"),
            (self.__cycle_one_song_action, "Powtarzaj jedną"),
            (self.__uncycle_action, "Nie powtarzaj"),
            (self.__quiet_action, "Ciszej"),
            (self.__loud_action, "Głośniej")
        ]
        self.__update_playback_menu()

    def __create_actions(self):
        self.__add_file_action = SimpleAction.new("add_files", None)
        self.__add_file_action.activate()
        self.__parent.add_action(self.__add_file_action)
        self.__add_file_action.connect("activate", self.__add_files)
        self.__file_menu.append("Dodaj pliki", "win.add_files")

        self.__exit_action = SimpleAction.new("exit", None)
        self.__exit_action.activate()
        self.__parent.add_action(self.__exit_action)
        self.__exit_action.connect("activate", self.__close_window)
        self.__file_menu.append("Wyjdź", "win.exit")

        self.__stop_action = SimpleAction.new("stop", None)
        self.__parent.add_action(self.__stop_action)

        self.__play_action = SimpleAction.new("play", None)
        self.__parent.add_action(self.__play_action)

        self.__prev_action = SimpleAction.new("prev", None)
        self.__parent.add_action(self.__prev_action)

        self.__next_action = SimpleAction.new("next", None)
        self.__parent.add_action(self.__next_action)

        self.__shuffle_action = SimpleAction.new("shuffle", None)
        self.__parent.add_action(self.__shuffle_action)

        self.__unshuffle_action = SimpleAction.new("unshuffle", None)
        self.__parent.add_action(self.__unshuffle_action)

        self.__cycle_playlist_action = SimpleAction.new("cycle_playlist", None)
        self.__parent.add_action(self.__cycle_playlist_action)

        self.__cycle_one_song_action = SimpleAction.new("cycle_song", None)
        self.__parent.add_action(self.__cycle_one_song_action)

        self.__uncycle_action = SimpleAction.new("uncycle", None)
        self.__parent.add_action(self.__uncycle_action)

        self.__quiet_action = SimpleAction.new("quiet", None)
        self.__parent.add_action(self.__quiet_action)

        self.__loud_action = SimpleAction.new("loud", None)
        self.__parent.add_action(self.__loud_action)

    def __add_files(self, _, __):
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
            self.emit("songs_added", None)
        dialog.destroy()

    def __empty_playback_menu(self):
        self.__playback_popover_menu.set_menu_model(None)

    def __update_playback_menu(self):
        action_lists = self.__actions.values()
        sub_menu = Menu.new()
        for action_list in action_lists:
            for action in action_list:
                sub_menu.append(
                    next(filter(lambda action_tuple: action_tuple[0] == action, self.__actions_labels), None)[1],
                    f"win.{action.get_name()}")
            self.__playback_popover_menu.set_menu_model(sub_menu)

    def __volume_down(self, _, __):
        current_volume = self.__media_player.get_volume() * 100
        _, diff = divmod(current_volume, VOLUME_CHANGE_VALUE)
        if diff != 0:
            self.__media_player.set_volume(current_volume - diff)
        else:
            self.__media_player.set_volume(current_volume - VOLUME_CHANGE_VALUE)

    def __volume_up(self, _, __):
        current_volume = self.__media_player.get_volume() * 100
        _, diff = divmod(current_volume, VOLUME_CHANGE_VALUE)
        if diff != 0:
            self.__media_player.set_volume(current_volume + VOLUME_CHANGE_VALUE - diff)
        else:
            self.__media_player.set_volume(current_volume + VOLUME_CHANGE_VALUE)

    def __playback_state_changed(self, _, __):
        self.__empty_playback_menu()
        if self.__media_player.get_current_playback_state() == Gst.State.PLAYING:
            self.__actions["play/pause"] = [self.__stop_action]
        else:
            self.__actions["play/pause"] = [self.__play_action]
        self.__update_playback_menu()

    def __volume_changed(self, _, volume):
        if volume == 0.0 and self.__actions["quieter/louder"].count(self.__quiet_action) != 0:
            self.__empty_playback_menu()
            self.__actions["quieter/louder"].remove(self.__quiet_action)
            self.__update_playback_menu()
        elif 0.0 < volume < 100.0:
            self.__empty_playback_menu()
            if self.__actions["quieter/louder"].count(self.__quiet_action) == 0:
                self.__actions["quieter/louder"][0] = self.__quiet_action

            if self.__actions["quieter/louder"].count(self.__loud_action) == 0:
                self.__actions["quieter/louder"].append(self.__loud_action)
            self.__update_playback_menu()
        elif volume == 100.0 and self.__actions["quieter/louder"].count(self.__loud_action) != 0:
            self.__empty_playback_menu()
            self.__actions["quieter/louder"].remove(self.__loud_action)
            self.__update_playback_menu()

    def __source_changed(self, _, __):
        self.__update_nex_prev_actions()

    def __update_nex_prev_actions(self):
        if self.__media_player.is_current_song_first() and self.__media_player.cycling != Cycling.PLAYLIST_CYCLED:
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

        if self.__media_player.is_current_song_last() and self.__media_player.cycling != Cycling.PLAYLIST_CYCLED:
            self.__empty_playback_menu()
            if self.__actions["prev/next"].count(self.__next_action) > 0:
                self.__actions["prev/next"].remove(self.__next_action)
            self.__update_playback_menu()
        else:
            self.__empty_playback_menu()
            if self.__actions["prev/next"].count(self.__next_action) == 0:
                self.__actions["prev/next"].append(self.__next_action)
            self.__update_playback_menu()

    def __cycling_changed(self, _, __):
        self.__empty_playback_menu()
        if self.__media_player.cycling == Cycling.PLAYLIST_CYCLED:
            self.__actions["shuffle/cycle"][1] = self.__cycle_one_song_action
        elif self.__media_player.cycling == Cycling.SONG_CYCLED:
            self.__actions["shuffle/cycle"][1] = self.__uncycle_action
        elif self.__media_player.cycling == Cycling.NO_CYCLING:
            self.__actions["shuffle/cycle"][1] = self.__cycle_playlist_action
        self.__update_playback_menu()
        self.__update_nex_prev_actions()

    def __shuffling_changed(self, _, __):
        self.__empty_playback_menu()
        if self.__media_player.shuffled:
            self.__actions["shuffle/cycle"][0] = self.__unshuffle_action
        else:
            self.__actions["shuffle/cycle"][0] = self.__shuffle_action
        self.__update_playback_menu()
        self.__update_nex_prev_actions()

    def __song_deleted(self, _, __):
        self.__update_nex_prev_actions()

    def __songs_added(self, _, __):
        self.__update_nex_prev_actions()

    def set_media_player(self, media_player):
        self.__media_player = media_player
        self.__update_nex_prev_actions()
        self.__media_player.connect("volume_changed", self.__volume_changed)

        self.__media_player.connect("cycling_changed", self.__cycling_changed)
        self.__media_player.connect("shuffling_changed", self.__shuffling_changed)
        self.__media_player.connect("song_deleted", self.__song_deleted)
        self.__media_player.connect("volume_changed", self.__song_deleted)
        self.__media_player.bus.connect("message::state-changed", self.__playback_state_changed)
        self.__media_player.connect("source_changed", self.__source_changed)
        self.__media_player.connect("songs_added", self.__songs_added)

        self.__stop_action.connect("activate", self.__media_player.pause)
        self.__play_action.connect("activate", self.__media_player.play)
        self.__prev_action.connect("activate", self.__media_player.play_prev)
        self.__next_action.connect("activate", self.__media_player.play_next)
        self.__shuffle_action.connect("activate", self.__media_player.shuffle)
        self.__unshuffle_action.connect("activate", self.__media_player.unshuffle)
        self.__cycle_playlist_action.connect("activate", self.__media_player.cycle_playlist)
        self.__cycle_one_song_action.connect("activate", self.__media_player.cycle_one_song)
        self.__uncycle_action.connect("activate", self.__media_player.uncycle)
        self.__quiet_action.connect("activate", self.__volume_down)
        self.__loud_action.connect("activate", self.__volume_up)

    def __close_window(self, _, __):
        self.__parent.close()

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
