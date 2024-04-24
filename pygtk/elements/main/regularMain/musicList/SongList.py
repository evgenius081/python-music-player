import gi

from pygtk.elements.main.regularMain.musicList.song.Song import Song

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

from gi.repository.Gtk import Box, Label, Image, ScrolledWindow, AspectFrame

import config

LAYOUT_VERTICAL_MARGIN = 22
LAYOUT_RIGHT_MARGIN = 3
HEADER_LEFT_MARGIN = 20
HEADER_BOTTOM_MARGIN = 15
DURATION_ICON_SIZE = 18
LIST_LAYOUT_SPACING = 15


class SongList(AspectFrame):
    def __init__(self, media_player):
        super().__init__()
        self.set_size_request(
            config.WINDOW_WIDTH,
            config.WINDOW_HEIGHT - config.MENU_BAR_HEIGHT - config.CONTROL_BLOCK_HEIGHT
        )
        self.set_valign(Gtk.Align.START)
        self.set_halign(Gtk.Align.START)
        self._media_player = media_player
        self._media_player.connect("source_changed", self._current_song_updated)
        self._media_player.connect("song_deleted", self._song_deleted)
        self._media_player.connect("songs_added", self._songs_added)
        self._songs = self._media_player.songs[:]
        self._current_song_index = 0
        self._song_widgets = []
        self._create_UI()

    def _create_UI(self):
        self._box = Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self._side_margin = int((config.WINDOW_WIDTH - config.TILE_WIDTH) / 2) - config.NUMBER_LABEL_WIDTH
        self._box.set_margin_start(self._side_margin)
        self._box.set_margin_top(LAYOUT_VERTICAL_MARGIN)
        self._box.set_margin_end(0)
        self._box.set_margin_bottom(LAYOUT_VERTICAL_MARGIN)
        self._box.set_size_request(
            config.WINDOW_WIDTH - self._side_margin,
            config.WINDOW_HEIGHT - config.MENU_BAR_HEIGHT - config.CONTROL_BLOCK_HEIGHT - LAYOUT_VERTICAL_MARGIN * 2
        )
        self._box.set_halign(Gtk.Align.START)
        self._box.set_valign(Gtk.Align.START)
        self.set_child(self._box)

        self._create_header()
        self._create_list()

    def _create_header(self):
        self._header_box = Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self._header_box.set_halign(Gtk.Align.START)
        self._header_box.set_valign(Gtk.Align.START)
        self._header_box.set_margin_start(HEADER_LEFT_MARGIN)
        self._header_box.set_margin_top(0)
        self._header_box.set_margin_end(0)
        self._header_box.set_margin_bottom(HEADER_BOTTOM_MARGIN)
        self._box.append(self._header_box)

        self._number_label = Label(label="#")
        self._number_label.set_name("header_number_label")
        self._header_box.append(self._number_label)

        self._title_label = Label(label="Tytuł")
        self._title_label.set_name("header_title_label")
        self._header_box.append(self._title_label)

        self._album_label = Label(label="Album")
        self._album_label.set_name("header_album_label")
        self._header_box.append(self._album_label)

        self._duration_icon = Image.new_from_file("common/assets/duration.svg")
        self._duration_icon.set_name("header_duration_icon")
        self._duration_icon.set_size_request(DURATION_ICON_SIZE, DURATION_ICON_SIZE)
        self._header_box.append(self._duration_icon)

    def _create_list(self):
        self._scroll_area = ScrolledWindow()
        self._scroll_area.set_size_request(
            config.WINDOW_WIDTH - self._side_margin,
            config.WINDOW_HEIGHT - config.MENU_BAR_HEIGHT - config.CONTROL_BLOCK_HEIGHT - LAYOUT_VERTICAL_MARGIN * 2
        )
        self._scroll_area.set_name("song_scroll")
        self._scroll_area.set_hexpand(config.TILE_WIDTH)
        self._scroll_area.set_halign(Gtk.Align.START)
        self._scroll_area.set_valign(Gtk.Align.START)
        self._scroll_area.set_margin_bottom(0)
        self._scroll_area.set_margin_top(0)
        self._scroll_area.set_margin_start(0)
        self._scroll_area.set_margin_end(0)

        self._song_box = Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=LIST_LAYOUT_SPACING)
        self._song_box.set_hexpand(True)
        self._song_box.set_margin_bottom(0)
        self._song_box.set_margin_top(0)
        self._song_box.set_margin_start(0)
        self._song_box.set_margin_end(0)
        self._song_box.set_halign(Gtk.Align.START)
        self._song_box.set_valign(Gtk.Align.START)

        for index, song in enumerate(self._songs):
            song_widget = Song(song, index + 1, self._media_player)
            if index == 0:
                song_widget.choose()
            self._song_widgets.append(song_widget)
            self._song_box.append(song_widget)

        self._scroll_area.set_child(self._song_box)
        self._box.append(self._scroll_area)

    def _current_song_updated(self, _, __):
        chosen_song_index = self._songs.index(self._media_player.get_current_song())
        if chosen_song_index != self._current_song_index:
            if self._song_widgets.count(self._song_widgets[self._current_song_index]) != 0:
                self._song_widgets[self._current_song_index].unchoose()
            self._song_widgets[chosen_song_index].choose()
            self._current_song_index = chosen_song_index

    def _song_deleted(self, _, song):
        song_to_remove = \
            [self._songs[i] for i in range(len(self._songs)) if self._songs[i].file_name == song.file_name][0]
        song_to_remove_index = self._songs.index(song_to_remove)
        self._songs.remove(song_to_remove)
        song_widget_to_remove = self._song_widgets[song_to_remove_index]
        self._song_box.remove(song_widget_to_remove)
        self._song_widgets.remove(song_widget_to_remove)
        self._current_song_index = self._songs.index(self._media_player.get_current_song())
        for index, song_widget in enumerate(self._song_widgets):
            song_widget.set_song_number(index + 1)

    def _songs_added(self, _, new_songs):
        for index, song in enumerate(new_songs):
            song_widget = Song(song, len(self._songs) + index + 1, self._media_player)
            self._song_widgets.append(song_widget)
            self._song_box.append(song_widget)
        self._songs.extend(new_songs)

