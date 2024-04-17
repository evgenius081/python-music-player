import gi

from pygtk.elements.main.regularMain.musicList.song.song import Song

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

from gi.repository.Gtk import Box, Label, Image, Viewport, AspectFrame

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
        self.set_hexpand(config.WINDOW_HEIGHT - config.MENU_BAR_HEIGHT - config.CONTROL_BLOCK_HEIGHT)
        self.set_vexpand(config.WINDOW_WIDTH)
        self.set_name("music_list")
        self.__media_player = media_player
        # self.__media_player.sourceChanged.connect(self.__current_song_updated)
        # self.__media_player.song_deleted.connect(self.__song_deleted)
        # self.__media_player.songs_added.connect(self.__songs_added)
        self.__songs = self.__media_player.get_songs()[:]
        self.__current_song_index = 0
        self.__song_widgets = []
        self.__create_UI()

    def __create_UI(self):
        self.__box = Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        side_margin = int((config.WINDOW_WIDTH - config.TILE_WIDTH) / 2) - config.NUMBER_LABEL_WIDTH
        self.__box.set_margin_start(side_margin)
        self.__box.set_margin_top(LAYOUT_VERTICAL_MARGIN)
        self.__box.set_margin_end(LAYOUT_RIGHT_MARGIN)
        self.__box.set_margin_bottom(LAYOUT_VERTICAL_MARGIN)

        self.__box.set_halign(Gtk.Align.START)
        self.__box.set_valign(Gtk.Align.CENTER)
        self.set_child(self.__box)

        self.__create_header()
        # self.__create_list()

    def __create_header(self):
        self.__header_box = Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__header_box.set_halign(Gtk.Align.START)
        self.__header_box.set_valign(Gtk.Align.CENTER)
        self.__header_box.set_margin_start(HEADER_LEFT_MARGIN)
        self.__header_box.set_margin_top(0)
        self.__header_box.set_margin_end(0)
        self.__header_box.set_margin_bottom(HEADER_BOTTOM_MARGIN)
        self.__box.append(self.__header_box)

        self.__number_label = Label(label="#")
        self.__number_label.set_name("header_number_label")
        self.__header_box.append(self.__number_label)

        self.__title_label = Label(label="Tytuł")
        self.__title_label.set_name("header_title_label")
        self.__header_box.append(self.__title_label)

        self.__album_label = Label(label="Album")
        self.__album_label.set_name("header_album_label")
        self.__header_box.append(self.__album_label)

        self.__duration_icon = Image.new_from_file("common/assets/duration.svg")
        self.__duration_icon.set_name("header_duration_icon")
        self.__duration_icon.set_hexpand(DURATION_ICON_SIZE)
        self.__duration_icon.set_vexpand(DURATION_ICON_SIZE)
        self.__header_box.append(self.__duration_icon)

    def __create_list(self):
        # self.__scroll_bar = QScrollBar()
        # self.__scroll_bar.setCursor(Qt.CursorShape.PointingHandCursor)
        # self.setStyleSheet(self.__styles)

        self.__scroll_area = Viewport()
        self.__scroll_area.set_name("song_scroll")
        self.__scroll_area.set_halign(Gtk.Align.CENTER)
        self.__scroll_area.set_valign(Gtk.Align.START)
        self.__scroll_area.set_margin_bottom(0)
        self.__scroll_area.set_margin_top(0)
        self.__scroll_area.set_margin_start(0)
        self.__scroll_area.set_margin_end(0)
        self.__scroll_area.set_hscroll_policy(Gtk.ScrollablePolicy.MINIMUM)
        # self.__scroll_area.resiz(True)
        # self.__scroll_area.setVerticalScrollBar(self.__scroll_bar)

        self.__song_box = Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=LIST_LAYOUT_SPACING)
        self.__song_box.set_margin_bottom(0)
        self.__song_box.set_margin_top(0)
        self.__song_box.set_margin_start(0)
        self.__song_box.set_margin_end(0)
        self.__song_box.set_halign(Gtk.Align.START)
        self.__song_box.set_valign(Gtk.Align.START)

        for index, song in enumerate(self.__songs):
            song_widget = Song(song, index + 1, self.__media_player)
            if index == 0:
                song_widget.choose()
            self.__song_widgets.append(song_widget)
            self.__song_box.append(song_widget)

        self.__scroll_area.set_child(self.__song_box)
        self.__box.append(self.__scroll_area)

    def __current_song_updated(self):
        chosen_song_index = self.__songs.index(self.__media_player.get_current_song())
        if chosen_song_index != self.__current_song_index:
            self.__song_widgets[self.__current_song_index].unchoose()
            self.__song_widgets[chosen_song_index].choose()
            self.__current_song_index = chosen_song_index

    # def __song_deleted(self, song):
    #     song_to_remove = \
    #         [self.__songs[i] for i in range(len(self.__songs)) if self.__songs[i].file_name == song.file_name][0]
    #     song_to_remove_index = self.__songs.index(song_to_remove)
    #     self.__songs.remove(song_to_remove)
    #     song_widget_to_remove = self.__song_widgets[song_to_remove_index]
    #     self.__list_layout.removeWidget(song_widget_to_remove)
    #     song_widget_to_remove.setParent(None)
    #     self.__song_widgets.remove(song_widget_to_remove)
    #     self.__current_song_index = self.__media_player.get_current_song()
    #     for index, song_widget in enumerate(self.__song_widgets):
    #         song_widget.set_song_number(index + 1)
    #
    # def __songs_added(self, new_songs):
    #     for index, song in enumerate(new_songs):
    #         song_widget = Song(song, len(self.__songs) + index + 1, self.__media_player)
    #         self.__song_widgets.append(song_widget)
    #         self.__list_layout.addWidget(song_widget)
    #     self.__songs.extend(new_songs)

