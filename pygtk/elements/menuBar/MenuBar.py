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
        self._media_player = None
        self._parent = parent
        self._create_menu()

    def _create_menu(self):
        self._file_menu = Menu.new()

        self._file_popover_menu = PopoverMenu()
        self._file_popover_menu.set_menu_model(self._file_menu)

        self._playback_popover_menu = PopoverMenu()

        self._file_menu_button = MenuButton()
        self._file_menu_button.set_label("Plik")
        self._file_menu_button.set_popover(self._file_popover_menu)
        self.pack_start(self._file_menu_button)

        self._playback_menu_button = MenuButton()
        self._playback_menu_button.set_label("Odtwarzanie")
        self._playback_menu_button.set_popover(self._playback_popover_menu)
        self.pack_start(self._playback_menu_button)

        self._about_button = Button()
        self._about_button.set_label("About")
        self._about_button.connect("clicked", self._show_about_window)
        self.pack_start(self._about_button)

        self._create_actions()
        self._actions = {
            "play/pause": [self._play_action],
            "prev/next": [self._prev_action, self._next_action],
            "shuffle/cycle": [self._shuffle_action, self._cycle_playlist_action],
            "quieter/louder": [self._quiet_action, self._loud_action]
        }
        self._actions_labels = [
            (self._add_file_action, "Dodaj pliki"),
            (self._exit_action, "Wyjdź"),
            (self._stop_action, "Pauza"),
            (self._play_action,"Odtwarzaj"),
            (self._prev_action, "Poprzednia"),
            (self._next_action, "Następna"),
            (self._shuffle_action, "Przetasuj"),
            (self._unshuffle_action, "Nie tasuj"),
            (self._cycle_playlist_action, "Powtarzaj listę"),
            (self._cycle_one_song_action, "Powtarzaj jedną"),
            (self._uncycle_action, "Nie powtarzaj"),
            (self._quiet_action, "Ciszej"),
            (self._loud_action, "Głośniej")
        ]
        self._update_playback_menu()

    def _create_actions(self):
        self._add_file_action = SimpleAction.new("add_files", None)
        self._add_file_action.activate()
        self._parent.add_action(self._add_file_action)
        self._add_file_action.connect("activate", self._add_files)
        self._file_menu.append("Dodaj pliki", "win.add_files")

        self._exit_action = SimpleAction.new("exit", None)
        self._exit_action.activate()
        self._parent.add_action(self._exit_action)
        self._exit_action.connect("activate", self._close_window)
        self._file_menu.append("Wyjdź", "win.exit")

        self._stop_action = SimpleAction.new("stop", None)
        self._parent.add_action(self._stop_action)

        self._play_action = SimpleAction.new("play", None)
        self._parent.add_action(self._play_action)

        self._prev_action = SimpleAction.new("prev", None)
        self._parent.add_action(self._prev_action)

        self._next_action = SimpleAction.new("next", None)
        self._parent.add_action(self._next_action)

        self._shuffle_action = SimpleAction.new("shuffle", None)
        self._parent.add_action(self._shuffle_action)

        self._unshuffle_action = SimpleAction.new("unshuffle", None)
        self._parent.add_action(self._unshuffle_action)

        self._cycle_playlist_action = SimpleAction.new("cycle_playlist", None)
        self._parent.add_action(self._cycle_playlist_action)

        self._cycle_one_song_action = SimpleAction.new("cycle_song", None)
        self._parent.add_action(self._cycle_one_song_action)

        self._uncycle_action = SimpleAction.new("uncycle", None)
        self._parent.add_action(self._uncycle_action)

        self._quiet_action = SimpleAction.new("quiet", None)
        self._parent.add_action(self._quiet_action)

        self._loud_action = SimpleAction.new("loud", None)
        self._parent.add_action(self._loud_action)

    def _add_files(self, _, __):
        file_filters = map(lambda s: f"*.{s}", config.MUSIC_FILE_FORMATS)
        dialog = Gtk.FileChooserNative.new(
            title="Wybierz pliki",
            parent=None,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.set_select_multiple(True)
        dialog.connect("response", self._on_file_chosen)
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Pliki dźwiękowe")
        for file_filter in file_filters:
            filter_text.add_pattern(file_filter)
        dialog.add_filter(filter_text)
        dialog.show()

    def _on_file_chosen(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            if self._media_player is None:
                last_song_number = 0
            else:
                last_song_number = int(self._media_player.songs[-1].file_name.split(".")[0])

            for index, file in enumerate(dialog.get_files()):
                clone_and_rename_file(file.get_path(), config.MUSIC_FOLDER_PATH, last_song_number + index + 1)
            self.emit("songs_added", None)
        dialog.destroy()

    def _empty_playback_menu(self):
        self._playback_popover_menu.set_menu_model(None)

    def _update_playback_menu(self):
        action_lists = self._actions.values()
        sub_menu = Menu.new()
        for action_list in action_lists:
            for action in action_list:
                sub_menu.append(
                    next(filter(lambda action_tuple: action_tuple[0] == action, self._actions_labels), None)[1],
                    f"win.{action.get_name()}")
            self._playback_popover_menu.set_menu_model(sub_menu)

    def _volume_down(self, _, __):
        current_volume = self._media_player.get_volume() * 100
        _, diff = divmod(current_volume, VOLUME_CHANGE_VALUE)
        if diff != 0:
            self._media_player.set_volume(current_volume - diff)
        else:
            self._media_player.set_volume(current_volume - VOLUME_CHANGE_VALUE)

    def _volume_up(self, _, __):
        current_volume = self._media_player.get_volume() * 100
        _, diff = divmod(current_volume, VOLUME_CHANGE_VALUE)
        if diff != 0:
            self._media_player.set_volume(current_volume + VOLUME_CHANGE_VALUE - diff)
        else:
            self._media_player.set_volume(current_volume + VOLUME_CHANGE_VALUE)

    def _playback_state_changed(self, _, __):
        self._empty_playback_menu()
        if self._media_player.get_current_playback_state() == Gst.State.PLAYING:
            self._actions["play/pause"] = [self._stop_action]
        else:
            self._actions["play/pause"] = [self._play_action]
        self._update_playback_menu()

    def _volume_changed(self, _, volume):
        if volume == 0.0 and self._actions["quieter/louder"].count(self._quiet_action) != 0:
            self._empty_playback_menu()
            self._actions["quieter/louder"].remove(self._quiet_action)
            self._update_playback_menu()
        elif 0.0 < volume < 100.0:
            self._empty_playback_menu()
            if self._actions["quieter/louder"].count(self._quiet_action) == 0:
                self._actions["quieter/louder"][0] = self._quiet_action

            if self._actions["quieter/louder"].count(self._loud_action) == 0:
                self._actions["quieter/louder"].append(self._loud_action)
            self._update_playback_menu()
        elif volume == 100.0 and self._actions["quieter/louder"].count(self._loud_action) != 0:
            self._empty_playback_menu()
            self._actions["quieter/louder"].remove(self._loud_action)
            self._update_playback_menu()

    def _source_changed(self, _, __):
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

    def _cycling_changed(self, _, __):
        self._empty_playback_menu()
        if self._media_player.cycling == Cycling.PLAYLIST_CYCLED:
            self._actions["shuffle/cycle"][1] = self._cycle_one_song_action
        elif self._media_player.cycling == Cycling.SONG_CYCLED:
            self._actions["shuffle/cycle"][1] = self._uncycle_action
        elif self._media_player.cycling == Cycling.NO_CYCLING:
            self._actions["shuffle/cycle"][1] = self._cycle_playlist_action
        self._update_playback_menu()
        self._update_nex_prev_actions()

    def _shuffling_changed(self, _, __):
        self._empty_playback_menu()
        if self._media_player.shuffled:
            self._actions["shuffle/cycle"][0] = self._unshuffle_action
        else:
            self._actions["shuffle/cycle"][0] = self._shuffle_action
        self._update_playback_menu()
        self._update_nex_prev_actions()

    def _song_deleted(self, _, __):
        self._update_nex_prev_actions()

    def _songs_added(self, _, __):
        self._update_nex_prev_actions()

    def set_media_player(self, media_player):
        self._media_player = media_player
        self._update_nex_prev_actions()
        self._media_player.connect("volume_changed", self._volume_changed)

        self._media_player.connect("cycling_changed", self._cycling_changed)
        self._media_player.connect("shuffling_changed", self._shuffling_changed)
        self._media_player.connect("song_deleted", self._song_deleted)
        self._media_player.connect("volume_changed", self._song_deleted)
        self._media_player.bus.connect("message::state-changed", self._playback_state_changed)
        self._media_player.connect("source_changed", self._source_changed)
        self._media_player.connect("songs_added", self._songs_added)

        self._stop_action.connect("activate", self._media_player.pause)
        self._play_action.connect("activate", self._media_player.play)
        self._prev_action.connect("activate", self._media_player.play_prev)
        self._next_action.connect("activate", self._media_player.play_next)
        self._shuffle_action.connect("activate", self._media_player.shuffle)
        self._unshuffle_action.connect("activate", self._media_player.unshuffle)
        self._cycle_playlist_action.connect("activate", self._media_player.cycle_playlist)
        self._cycle_one_song_action.connect("activate", self._media_player.cycle_one_song)
        self._uncycle_action.connect("activate", self._media_player.uncycle)
        self._quiet_action.connect("activate", self._volume_down)
        self._loud_action.connect("activate", self._volume_up)

    def _close_window(self, _, __):
        self._parent.close()

    @staticmethod
    def _show_about_window(_):
        dialog = Gtk.MessageDialog(

            message_type=Gtk.MessageType.INFO,
            text="Aplikacja przedstawia sobą odtwarzacz muzyki, który pozwala wybierać pliki do odtwarzania, "
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
                        "piosenki, przycisków na dole okna aplikacji oraz menu Odtwarzanie w pasku menu.",
            title="Opis aplikacji"
        )
        dialog.show()
