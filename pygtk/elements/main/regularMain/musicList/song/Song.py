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
        self._media_player = media_player
        self._chosen = False
        self._song = song
        self._song_number = number
        self._create_UI()

    def _create_UI(self):
        self._box = Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=LAYOUT_SPACING)
        self._box.set_margin_bottom(0)
        self._box.set_margin_top(0)
        self._box.set_margin_start(0)
        self._box.set_margin_end(0)
        self.set_child(self._box)

        self._number_label = Label(label=str(self._song_number))
        self._number_label.set_name("song_number_label")
        self._number_label.set_margin_bottom(0)
        self._number_label.set_margin_top(0)
        self._number_label.set_margin_start(0)
        self._number_label.set_margin_end(0)
        self._number_label.set_size_request(config.NUMBER_LABEL_WIDTH, -1)
        self._number_label.set_xalign(1)
        self._number_label.set_valign(Gtk.Align.CENTER)
        self._box.append(self._number_label)

        self._song_frame = AspectFrame()
        self._song_frame.set_name("song_frame_unchosen")
        self._song_frame.set_size_request(config.TILE_WIDTH, TILE_HEIGHT)
        self._song_frame.set_xalign(0)
        self._song_frame.set_valign(Gtk.Align.CENTER)
        self._song_frame.set_margin_bottom(0)
        self._song_frame.set_margin_top(0)
        self._song_frame.set_margin_start(0)
        self._song_frame.set_margin_end(0)
        self._box.append(self._song_frame)

        self._event_controller = EventControllerMotion()
        self._event_controller.connect("enter", self._on_enter)
        self._event_controller.connect("leave", self._on_leave)
        self._song_frame.add_controller(self._event_controller)

        self._song_box = Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self._song_box.set_halign(Gtk.Align.START)
        self._song_box.set_margin_bottom(0)
        self._song_box.set_margin_top(0)
        self._song_box.set_margin_start(0)
        self._song_box.set_margin_end(0)
        self._create__title_layout()
        self._song_frame.set_child(self._song_box)

        self._album_label = Label(label=self._song.song_album)
        self._album_label.set_name("song_album_label")
        self._album_label.set_xalign(0)
        self._album_label.set_margin_bottom(0)
        self._album_label.set_margin_top(0)
        self._album_label.set_margin_start(0)
        self._album_label.set_margin_end(0)
        self._album_label.set_size_request(int(config.TILE_WIDTH * ALBUM_WIDGET_WIDTH_RATIO), LABEL_HEIGHT)
        self._song_box.append(self._album_label)

        self._duration_label = Label(label=self._song.song_duration)
        self._duration_label.set_name("song_duration_label")
        self._duration_label.set_size_request(DURATION_LABEL_WIDTH, LABEL_HEIGHT)
        self._duration_label.set_xalign(0)
        self._duration_label.set_valign(Gtk.Align.CENTER)
        self._duration_label.set_margin_bottom(0)
        self._duration_label.set_margin_top(0)
        self._duration_label.set_margin_start(0)
        self._duration_label.set_margin_end(0)
        self._song_box.append(self._duration_label)

        self._delete_song_button = Button(label="")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file("common/assets/delete.svg")
        pixbuf.scale_simple(
            SONG_COVER_SIZE,
            SONG_COVER_SIZE,
            GdkPixbuf.InterpType.BILINEAR
        )
        self._delete_song_button.set_child(Image.new_from_pixbuf(pixbuf))
        self._delete_song_button.set_margin_start(MARGIN_LABEL_WIDTH)
        self._delete_song_button.set_cursor(Cursor.new_from_name("pointer"))
        self._delete_song_button.set_name("delete_song_button")
        self._delete_song_button.connect("clicked", self._remove_song)
        self._song_box.append(self._delete_song_button)

    def _create__title_layout(self):
        self._title_box = Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=TITLE_LAYOUT_SPACING)
        self._title_box.set_margin_bottom(0)
        self._title_box.set_margin_top(0)
        self._title_box.set_margin_start(0)
        self._title_box.set_margin_end(0)
        self._title_box.set_halign(Gtk.Align.END)
        self._title_box.set_valign(Gtk.Align.CENTER)
        self._song_box.append(self._title_box)

        self._cover_image = Image()
        if self._song.song_cover_bytes is not None:
            loader = GdkPixbuf.PixbufLoader.new()
            loader.write(self._song.song_cover_bytes)
            loader.close()
            pixbuf = loader.get_pixbuf()
        else:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file("common/assets/placeholder.png")
        resized_pixbuf = pixbuf.scale_simple(
            SONG_COVER_SIZE,
            SONG_COVER_SIZE,
            GdkPixbuf.InterpType.BILINEAR
        )
        self._cover_image.set_from_pixbuf(resized_pixbuf)
        self._cover_image.set_name("cover_image")
        self._cover_image.set_margin_bottom(0)
        self._cover_image.set_margin_top(0)
        self._cover_image.set_margin_start(0)
        self._cover_image.set_margin_end(0)
        self._cover_image.set_size_request(SONG_COVER_SIZE+2, SONG_COVER_SIZE+2)
        self._title_box.append(self._cover_image)

        self._play_button = Button(label="")
        self._play_button.set_child(Image.new_from_file("common/assets/play_light.svg"))
        self._play_button.set_size_request(SONG_COVER_SIZE-2, SONG_COVER_SIZE-2)
        self._play_button.set_name("song_play_button_unchosen")
        self._play_button.set_cursor(Cursor.new_from_name("pointer"))
        self._play_button.set_visible(False)
        self._play_button.connect("clicked", self._play_song)
        self._title_box.append(self._play_button)

        self._title_author_box = Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=TITLE_AUTHOR_LAYOUT_SPACING)
        self._title_author_box.set_margin_bottom(0)
        self._title_author_box.set_margin_top(0)
        self._title_author_box.set_margin_start(0)
        self._title_author_box.set_margin_end(0)
        self._title_author_box.set_size_request(int(config.TILE_WIDTH * TITLE_WIDGET_WIDTH_RATIO), SONG_COVER_SIZE)
        self._title_author_box.set_halign(Gtk.Align.START)
        self._title_author_box.set_valign(Gtk.Align.START)
        self._title_box.append(self._title_author_box)

        self._title_label = Label(label=self._song.song_title if self._song.song_title != "" else self._song.file_name)
        self._title_label.set_name("song_title_label")
        self._title_label.set_size_request(int(config.TILE_WIDTH * TITLE_WIDGET_WIDTH_RATIO), LABEL_HEIGHT)
        self._title_label.set_margin_bottom(0)
        self._title_label.set_margin_top(0)
        self._title_label.set_margin_start(0)
        self._title_label.set_margin_end(0)
        self._title_label.set_xalign(0)
        self._title_author_box.append(self._title_label)

        if self._song.song_author != "":
            self._author_label = Label(label=self._song.song_author)
            self._author_label.set_name("song_author_label")
            self._author_label.set_margin_bottom(0)
            self._author_label.set_margin_top(0)
            self._author_label.set_margin_start(0)
            self._author_label.set_margin_end(0)
            self._author_label.set_size_request(int(config.TILE_WIDTH * TITLE_WIDGET_WIDTH_RATIO), LABEL_HEIGHT)
            self._author_label.set_xalign(0)
            self._title_author_box.append(self._author_label)

    def _on_enter(self, _, __, ___):
        if not self._chosen:
            self._play_button.set_visible(True)
            self._cover_image.set_visible(False)

    def _on_leave(self, _):
        if not self._chosen:
            self._play_button.set_visible(False)
            self._cover_image.set_visible(True)

    def _play_song(self, _):
        if not self._chosen:
            self._media_player.play_song(self._song)

    def choose(self):
        self._song_frame.set_name("song_frame_chosen")
        self._play_button.set_name("song_play_button_chosen")
        self._play_button.set_visible(True)
        self._play_button.set_cursor(Cursor.new_from_name("arrow"))
        self._play_button.set_child(Image.new_from_file("common/assets/play_active.svg"))
        self._cover_image.set_visible(False)
        self._delete_song_button.set_visible(False)
        self._chosen = True

    def unchoose(self):
        self._song_frame.set_name("song_frame_unchosen")
        self._play_button.set_name("song_play_button_unchosen")
        self._play_button.set_visible(False)
        self._play_button.set_cursor(Cursor.new_from_name("pointer"))
        self._play_button.set_child(Image.new_from_file("common/assets/play_light.svg"))
        self._cover_image.set_visible(True)
        self._delete_song_button.set_visible(True)
        self._chosen = False

    def _remove_song(self, _):
        self._media_player.delete_song(self._song)

    def set_song_number(self, number):
        self._song_number = number
        self._number_label.set_label(str(number))

