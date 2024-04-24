import config
import gi


gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")

from gi.repository import Gtk, GdkPixbuf

from gi.repository.Gtk import Box, Label, Image, Button, AspectFrame, Window, EventControllerMotion
from gi.repository.Gdk import Cursor

TILE_HEIGHT = 52
TITLE_WIDGET_WIDTH_RATIO = 0.4
ALBUM_WIDGET_WIDTH_RATIO = 0.39
LAYOUT_SPACING = 10
LABEL_HEIGHT = 17
DURATION_LABEL_WIDTH = 30
MARGIN_LABEL_WIDTH = 35
TITLE_LAYOUT_SPACING = 9
SONG_COVER_SIZE = 34
TITLE_AUTHOR_LAYOUT_SPACING = 2


class Song(AspectFrame):
    def __init__(self, song, number, media_player):
        super().__init__()
        self.set_name("song")
        self.set_size_request(config.TILE_WIDTH + LAYOUT_SPACING + config.NUMBER_LABEL_WIDTH, TILE_HEIGHT)
        self.set_margin_bottom(0)
        self.set_margin_top(0)
        self.set_margin_start(0)
        self.set_margin_end(0)
        self.__media_player = media_player
        self.__chosen = False
        self.__song = song
        self.__song_number = number
        self.__create_UI()

    def __create_UI(self):
        self.__box = Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=LAYOUT_SPACING)
        self.__box.set_margin_bottom(0)
        self.__box.set_margin_top(0)
        self.__box.set_margin_start(0)
        self.__box.set_margin_end(0)
        self.set_child(self.__box)

        self.__number_label = Label(label=str(self.__song_number))
        self.__number_label.set_name("song_number_label")
        self.__number_label.set_margin_bottom(0)
        self.__number_label.set_margin_top(0)
        self.__number_label.set_margin_start(0)
        self.__number_label.set_margin_end(0)
        self.__number_label.set_size_request(config.NUMBER_LABEL_WIDTH, -1)
        self.__number_label.set_xalign(1)
        self.__number_label.set_valign(Gtk.Align.CENTER)
        self.__box.append(self.__number_label)

        self.__song_frame = AspectFrame()
        self.__song_frame.set_name("song_frame_unchosen")
        self.__song_frame.set_size_request(config.TILE_WIDTH, TILE_HEIGHT)
        self.__song_frame.set_xalign(0)
        self.__song_frame.set_valign(Gtk.Align.CENTER)
        self.__song_frame.set_margin_bottom(0)
        self.__song_frame.set_margin_top(0)
        self.__song_frame.set_margin_start(0)
        self.__song_frame.set_margin_end(0)
        # self.__song_frame.connect("enter-notify-even", self.__on_enter)
        # self.__song_frame.connect("leave-notify-even", self.__on_leave)
        self.__box.append(self.__song_frame)

        self.__event_controller = EventControllerMotion()
        self.__event_controller.connect("enter", self.__on_enter)
        self.__event_controller.connect("leave", self.__on_leave)
        self.__song_frame.add_controller(self.__event_controller)

        self.__song_box = Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__song_box.set_halign(Gtk.Align.START)
        self.__song_box.set_margin_bottom(0)
        self.__song_box.set_margin_top(0)
        self.__song_box.set_margin_start(0)
        self.__song_box.set_margin_end(0)
        self.__create__title_layout()
        self.__song_frame.set_child(self.__song_box)

        self.__album_label = Label(label=self.__song.song_album)
        self.__album_label.set_name("song_album_label")
        self.__album_label.set_xalign(0)
        self.__album_label.set_margin_bottom(0)
        self.__album_label.set_margin_top(0)
        self.__album_label.set_margin_start(0)
        self.__album_label.set_margin_end(0)
        self.__album_label.set_size_request(int(config.TILE_WIDTH * ALBUM_WIDGET_WIDTH_RATIO), LABEL_HEIGHT)
        self.__song_box.append(self.__album_label)

        self.__duration_label = Label(label=self.__song.song_duration)
        self.__duration_label.set_name("song_duration_label")
        self.__duration_label.set_size_request(DURATION_LABEL_WIDTH, LABEL_HEIGHT)
        self.__duration_label.set_xalign(0)
        self.__duration_label.set_valign(Gtk.Align.CENTER)
        self.__duration_label.set_margin_bottom(0)
        self.__duration_label.set_margin_top(0)
        self.__duration_label.set_margin_start(0)
        self.__duration_label.set_margin_end(0)
        self.__song_box.append(self.__duration_label)

        self.__delete_song_button = Button(label="")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file("common/assets/delete.svg")
        pixbuf.scale_simple(
            SONG_COVER_SIZE,
            SONG_COVER_SIZE,
            GdkPixbuf.InterpType.BILINEAR)
        self.__delete_song_button.set_child(Image.new_from_pixbuf(pixbuf))
        self.__delete_song_button.set_margin_start(MARGIN_LABEL_WIDTH)
        self.__delete_song_button.set_cursor(Cursor.new_from_name("pointer"))
        self.__delete_song_button.set_name("delete_song_button")
        self.__delete_song_button.connect("clicked", self.__remove_song)
        self.__song_box.append(self.__delete_song_button)

    def __create__title_layout(self):
        self.__title_box = Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=TITLE_LAYOUT_SPACING)
        self.__title_box.set_margin_bottom(0)
        self.__title_box.set_margin_top(0)
        self.__title_box.set_margin_start(0)
        self.__title_box.set_margin_end(0)
        self.__title_box.set_halign(Gtk.Align.END)
        self.__title_box.set_valign(Gtk.Align.CENTER)
        self.__song_box.append(self.__title_box)

        self.__cover_image = Image()
        if self.__song.song_cover_image_stream is not None:
            loader = GdkPixbuf.PixbufLoader.new()
            loader.write(self.__song.song_cover_image_stream)
            loader.close()
            pixbuf = loader.get_pixbuf()
        else:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file("common/assets/placeholder.png")
        resized_pixbuf = pixbuf.scale_simple(
            SONG_COVER_SIZE,
            SONG_COVER_SIZE,
            GdkPixbuf.InterpType.BILINEAR
        )
        self.__cover_image.set_from_pixbuf(resized_pixbuf)
        self.__cover_image.set_name("cover_image")
        self.__cover_image.set_margin_bottom(0)
        self.__cover_image.set_margin_top(0)
        self.__cover_image.set_margin_start(0)
        self.__cover_image.set_margin_end(0)
        self.__cover_image.set_size_request(SONG_COVER_SIZE+2, SONG_COVER_SIZE+2)
        self.__title_box.append(self.__cover_image)

        self.__play_button = Button(label="")
        self.__play_button.set_child(Image.new_from_file("common/assets/play_light.svg"))
        self.__play_button.set_size_request(SONG_COVER_SIZE-2, SONG_COVER_SIZE-2)
        self.__play_button.set_name("song_play_button_unchosen")
        self.__play_button.set_cursor(Cursor.new_from_name("pointer"))
        self.__play_button.set_visible(False)
        self.__play_button.connect("clicked", self.__play_song)
        self.__title_box.append(self.__play_button)

        self.__title_author_box = Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=TITLE_AUTHOR_LAYOUT_SPACING)
        self.__title_author_box.set_margin_bottom(0)
        self.__title_author_box.set_margin_top(0)
        self.__title_author_box.set_margin_start(0)
        self.__title_author_box.set_margin_end(0)
        self.__title_author_box.set_size_request(int(config.TILE_WIDTH * TITLE_WIDGET_WIDTH_RATIO), SONG_COVER_SIZE)
        self.__title_author_box.set_halign(Gtk.Align.START)
        self.__title_author_box.set_valign(Gtk.Align.START)
        self.__title_box.append(self.__title_author_box)

        self.__title_label = Label(label=self.__song.song_title if self.__song.song_title != "" else self.__song.file_name)
        self.__title_label.set_name("song_title_label")
        self.__title_label.set_size_request(int(config.TILE_WIDTH * TITLE_WIDGET_WIDTH_RATIO), LABEL_HEIGHT)
        self.__title_label.set_margin_bottom(0)
        self.__title_label.set_margin_top(0)
        self.__title_label.set_margin_start(0)
        self.__title_label.set_margin_end(0)
        self.__title_label.set_xalign(0)
        self.__title_author_box.append(self.__title_label)

        if self.__song.song_author != "":
            self.__author_label = Label(label=self.__song.song_author)
            self.__author_label.set_name("song_author_label")
            self.__author_label.set_margin_bottom(0)
            self.__author_label.set_margin_top(0)
            self.__author_label.set_margin_start(0)
            self.__author_label.set_margin_end(0)
            self.__author_label.set_size_request(int(config.TILE_WIDTH * TITLE_WIDGET_WIDTH_RATIO), LABEL_HEIGHT)
            self.__author_label.set_xalign(0)
            self.__title_author_box.append(self.__author_label)

    def __on_enter(self, _, __, ___):
        if not self.__chosen:
            self.__play_button.set_visible(True)
            self.__cover_image.set_visible(False)

    def __on_leave(self, _):
        if not self.__chosen:
            self.__play_button.set_visible(False)
            self.__cover_image.set_visible(True)

    def __play_song(self, _):
        if not self.__chosen:
            self.__media_player.play_song(self.__song)

    def choose(self):
        self.__song_frame.set_name("song_frame_chosen")
        self.__play_button.set_name("song_play_button_chosen")
        self.__play_button.set_visible(True)
        self.__play_button.set_cursor(Cursor.new_from_name("arrow"))
        self.__play_button.set_child(Image.new_from_file("common/assets/play_active.svg"))
        self.__cover_image.set_visible(False)
        self.__delete_song_button.set_visible(False)
        self.__chosen = True

    def unchoose(self):
        self.__song_frame.set_name("song_frame_unchosen")
        self.__play_button.set_name("song_play_button_unchosen")
        self.__play_button.set_visible(False)
        self.__play_button.set_cursor(Cursor.new_from_name("pointer"))
        self.__play_button.set_child(Image.new_from_file("common/assets/play_light.svg"))
        self.__cover_image.set_visible(True)
        self.__delete_song_button.set_visible(True)
        self.__chosen = False

    def __remove_song(self, _):
        self.__media_player.delete_song(self.__song)

    def set_song_number(self, number):
        self.__song_number = number
        self.__number_label.set_label(str(number))

