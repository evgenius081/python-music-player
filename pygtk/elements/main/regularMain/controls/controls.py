import config
from common.classes.Cycling import Cycling
from common.utils.formatter import number_to_mins_and_secs

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version('Gst', '1.0')

from gi.repository import Gtk, Gdk, GdkPixbuf, Gst, GLib

Gst.init(None)

from gi.repository.Gtk import Box, Label, Image, AspectFrame, Button, Scale

CURRENT_SONG_COVER_SIZE = 50
CURRENT_SONG_TITLE_LABEL = 17
CURRENT_SONG_AUTHOR_LABEL_HEIGHT = 17
CURRENT_SONG_LAYOUT_SPACING = 10
CONTROLS_LAYOUT_SPACING = 16
TITLE_AUTHOR_LAYOUT_SPACING = 2
TITLE_AUTHOR_WIDGET_HEIGHT = 36
CURRENT_SONG_WIDGET_HEIGHT = 50
CONTROL_BUTTONS_WIDGET_HEIGHT = 36
CONTROL_BUTTONS_LAYOUT_SPACING = 22
CONTROL_BUTTON_SIZE = 20
PLAY_BUTTON_SIZE = 36
CONTROL_SLIDER_WIDGET_HEIGHT = 17
CONTROL_SLIDER_LAYOUT_SPACING = 13
SOUND_CONTROLS_LAYOUT_SPACING = 15
SOUND_ICON_SIZE = 24
RANGE_MIN = 0
SOUND_RANGE_MAX = 100
SOUND_SLIDER_WIDTH = 100
INIT_VOLUME = 0


class Controls(AspectFrame):
    def __init__(self, media_player):
        super().__init__()
        self.set_size_request(config.WINDOW_WIDTH, config.CONTROL_BLOCK_HEIGHT)
        self.__media_player = media_player
        self.__current_song = self.__media_player.get_current_song()
        self.__media_player.connect("cycling_changed", self.__cycling_changed)
        self.__media_player.connect("shuffling_changed", self.__shuffling_changed)
        self.__media_player.connect("song_deleted", self.__song_deleted)
        self.__media_player.play_bin.connect("source-setup", self.__source_changed)
        self.__media_player.bus.connect("message::state-changed", self.__on_state_changed)
        self.__media_player.connect("volume_changed", self.__sound_position_changed)
        self.__media_player.connect("songs_added", self.__songs_added)
        GLib.timeout_add(10, self.__refresh_slider)
        GLib.timeout_add(1000, self.__refresh_current_time_label)
        self.__current_song_second = 0
        self.set_halign(Gtk.Align.START)
        self.set_valign(Gtk.Align.CENTER)
        self.set_xalign(0)
        self.set_name("controls")
        self.__current_song_and_sound_width = int((config.WINDOW_WIDTH - config.SLIDER_BLOCK_WIDTH - 10) / 2)
        self.__create_UI()

    def __create_UI(self):
        self.__box = Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__box.set_margin_bottom(0)
        self.__box.set_margin_top(0)
        self.__box.set_margin_start(0)
        self.__box.set_margin_end(0)
        self.__box.set_halign(Gtk.Align.START)
        self.__box.set_valign(Gtk.Align.CENTER)
        self.set_child(self.__box)

        self.__create_current_song_widget()
        self.__create_controls_widget()
        self.__create_sound_controls_widget()

    def __create_current_song_widget(self):
        self.__current_song_frame = AspectFrame()
        self.__current_song_frame.set_size_request(self.__current_song_and_sound_width, CURRENT_SONG_WIDGET_HEIGHT)
        self.__current_song_frame.set_margin_bottom(0)
        self.__current_song_frame.set_margin_top(0)
        self.__current_song_frame.set_margin_start(0)
        self.__current_song_frame.set_margin_end(0)
        self.__current_song_frame.set_halign(Gtk.Align.START)
        self.__current_song_frame.set_valign(Gtk.Align.CENTER)
        self.__box.append(self.__current_song_frame)

        self.__current_song_box = Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=CURRENT_SONG_LAYOUT_SPACING)
        self.__current_song_box.set_margin_bottom(0)
        self.__current_song_box.set_margin_top(0)
        self.__current_song_box.set_margin_start(0)
        self.__current_song_box.set_margin_end(0)
        self.__current_song_box.set_halign(Gtk.Align.START)
        self.__current_song_box.set_valign(Gtk.Align.CENTER)
        self.__current_song_frame.set_child(self.__current_song_box)

        self.__cover_image = Image.new()
        self.__set_cover()
        self.__cover_image.set_name("current_cover_label")
        self.__cover_image.set_size_request(CURRENT_SONG_COVER_SIZE, CURRENT_SONG_COVER_SIZE)
        self.__current_song_box.append(self.__cover_image)

        self.__title_author_frame = AspectFrame()
        self.__title_author_frame.set_size_request(
            self.__current_song_and_sound_width - CURRENT_SONG_COVER_SIZE - CURRENT_SONG_LAYOUT_SPACING,
            TITLE_AUTHOR_WIDGET_HEIGHT
        )
        self.__title_author_frame.set_margin_bottom(0)
        self.__title_author_frame.set_margin_top(0)
        self.__title_author_frame.set_margin_start(0)
        self.__title_author_frame.set_margin_end(0)
        self.__current_song_box.append(self.__title_author_frame)

        self.__title_author_box = Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=TITLE_AUTHOR_LAYOUT_SPACING)
        self.__title_author_box.set_margin_bottom(0)
        self.__title_author_box.set_margin_top(0)
        self.__title_author_box.set_margin_start(0)
        self.__title_author_box.set_margin_end(0)
        self.__title_author_box.set_halign(Gtk.Align.START)
        self.__title_author_box.set_valign(Gtk.Align.CENTER)
        self.__title_author_frame.set_child(self.__title_author_box)

        self.__title_label = Label(label=self.__current_song.song_title if self.__current_song.song_title != "" else
        self.__current_song.file_name
                                   )
        self.__title_label.set_name("current_song_title_label")
        self.__title_label.set_xalign(0)
        self.__title_label.set_size_request(
            self.__current_song_and_sound_width - CURRENT_SONG_COVER_SIZE - CURRENT_SONG_LAYOUT_SPACING,
            CURRENT_SONG_TITLE_LABEL
        )
        self.__title_label.set_margin_bottom(0)
        self.__title_label.set_margin_top(0)
        self.__title_label.set_margin_start(0)
        self.__title_label.set_margin_end(0)
        self.__title_author_box.append(self.__title_label)

        if self.__current_song.song_author != "":
            self.__author_label = Label(label=self.__current_song.song_author)
            self.__author_label.set_name("current_song_author_label")
            self.__author_label.set_xalign(0)
            self.__author_label.set_margin_bottom(0)
            self.__author_label.set_margin_top(0)
            self.__author_label.set_margin_start(0)
            self.__author_label.set_margin_end(0)
            self.__author_label.set_size_request(
                self.__current_song_and_sound_width - CURRENT_SONG_COVER_SIZE - CURRENT_SONG_LAYOUT_SPACING,
                CURRENT_SONG_TITLE_LABEL)
            self.__title_author_box.append(self.__author_label)

    def __create_controls_widget(self):
        self.__controls_frame = AspectFrame()
        self.__controls_frame.set_margin_bottom(0)
        self.__controls_frame.set_margin_top(0)
        self.__controls_frame.set_margin_start(0)
        self.__controls_frame.set_margin_end(0)
        self.__controls_frame.set_size_request(config.SLIDER_BLOCK_WIDTH, -1)
        self.__box.append(self.__controls_frame)

        self.__controls_box = Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=CONTROLS_LAYOUT_SPACING)
        self.__controls_box.set_halign(Gtk.Align.CENTER)
        self.__controls_box.set_valign(Gtk.Align.CENTER)
        self.__controls_box.set_margin_bottom(0)
        self.__controls_box.set_margin_top(0)
        self.__controls_box.set_margin_start(0)
        self.__controls_box.set_margin_end(0)
        self.__controls_frame.set_child(self.__controls_box)

        self.__create_buttons()
        self.__create_slider()

    def __create_buttons(self):
        self.__control_buttons_frame = AspectFrame()
        self.__control_buttons_frame.set_margin_bottom(0)
        self.__control_buttons_frame.set_margin_top(0)
        self.__control_buttons_frame.set_margin_start(0)
        self.__control_buttons_frame.set_margin_end(0)
        self.__controls_box.append(self.__control_buttons_frame)

        self.__control_buttons_box = Box.new(orientation=Gtk.Orientation.HORIZONTAL,
                                             spacing=CONTROL_BUTTONS_LAYOUT_SPACING)
        self.__control_buttons_box.set_halign(Gtk.Align.CENTER)
        self.__control_buttons_box.set_valign(Gtk.Align.CENTER)
        self.__control_buttons_box.set_margin_bottom(0)
        self.__control_buttons_box.set_margin_top(0)
        self.__control_buttons_box.set_margin_start(0)
        self.__control_buttons_box.set_margin_end(0)
        self.__control_buttons_frame.set_child(self.__control_buttons_box)

        self.__shuffle_button = Button(label="")
        self.__shuffle_button.set_child(Image.new_from_file("common/assets/shuffle_inactive.svg"))
        self.__shuffle_button.set_name("shuffle_button")
        self.__shuffle_button.set_cursor(Gdk.Cursor.new_from_name("pointer"))
        self.__shuffle_button.set_size_request(CONTROL_BUTTON_SIZE, CONTROL_BUTTON_SIZE)
        self.__shuffle_button.connect("clicked", self.__shuffle_songs)
        self.__control_buttons_box.append(self.__shuffle_button)

        self.__play_prev_button = Button(label="")
        self.__play_prev_button.set_name("play_prev_button")
        self.__play_prev_button.set_cursor(Gdk.Cursor.new_from_name("pointer"))
        self.__play_prev_button.set_size_request(CONTROL_BUTTON_SIZE, CONTROL_BUTTON_SIZE)
        self.__play_prev_button.connect("clicked", self.__play_prev)
        self.__control_buttons_box.append(self.__play_prev_button)

        self.__play_button = Button(label="")
        self.__play_button.set_child(Image.new_from_file("common/assets/play_active.svg"))
        self.__play_button.set_name("play_button")
        self.__play_button.set_cursor(Gdk.Cursor.new_from_name("pointer"))
        self.__play_button.set_size_request(PLAY_BUTTON_SIZE, PLAY_BUTTON_SIZE)
        self.__play_button.connect("clicked", self.__play_song)
        self.__control_buttons_box.append(self.__play_button)

        self.__play_next_button = Button(label="")
        self.__play_next_button.set_name("play_next_button")
        self.__play_next_button.set_cursor(Gdk.Cursor.new_from_name("pointer"))
        self.__play_next_button.set_size_request(CONTROL_BUTTON_SIZE, CONTROL_BUTTON_SIZE)
        self.__play_next_button.connect("clicked", self.__play_next)
        self.__control_buttons_box.append(self.__play_next_button)

        self.__cycle_button = Button(label="")
        self.__cycle_button.set_child(Image.new_from_file("common/assets/cycle.svg"))
        self.__cycle_button.set_name("cycle_button")
        self.__cycle_button.set_cursor(Gdk.Cursor.new_from_name("pointer"))
        self.__cycle_button.set_size_request(CONTROL_BUTTON_SIZE, CONTROL_BUTTON_SIZE)
        self.__cycle_button.connect("clicked", self.__cycle)
        self.__control_buttons_box.append(self.__cycle_button)

        self.__update_prev_next_buttons()

    def __create_slider(self):
        self.__control_slider_frame = AspectFrame()
        self.__control_slider_frame.set_margin_bottom(0)
        self.__control_slider_frame.set_margin_top(0)
        self.__control_slider_frame.set_margin_start(0)
        self.__control_slider_frame.set_margin_end(0)
        self.__control_slider_frame.set_size_request(config.SLIDER_BLOCK_WIDTH, CONTROL_SLIDER_WIDGET_HEIGHT)
        self.__controls_box.append(self.__control_slider_frame)

        self.__control_slider_box = Box.new(orientation=Gtk.Orientation.HORIZONTAL,
                                            spacing=CONTROL_SLIDER_LAYOUT_SPACING)
        self.__control_slider_box.set_halign(Gtk.Align.CENTER)
        self.__control_slider_box.set_valign(Gtk.Align.CENTER)
        self.__control_slider_box.set_margin_bottom(0)
        self.__control_slider_box.set_margin_top(0)
        self.__control_slider_box.set_margin_start(0)
        self.__control_slider_box.set_margin_end(0)
        self.__control_slider_frame.set_child(self.__control_slider_box)

        self.__current_time_label = Label(label=" 0:00")
        self.__current_time_label.set_name("current_playback_time_label")
        self.__control_slider_box.append(self.__current_time_label)

        self.__playback_slider = Scale()
        self.__playback_slider.set_name("playback_slider")
        self.__playback_slider_update_signal_id = self.__playback_slider.connect(
            "value-changed",
            self.__set_position)
        self.__playback_slider.set_size_request(config.SLIDER_BLOCK_WIDTH, -1)
        self.__control_slider_box.append(self.__playback_slider)

        self.__total_time_label = Label(label=self.__current_song.song_duration)
        self.__total_time_label.set_name("total_playback_time_label")
        self.__control_slider_box.append(self.__total_time_label)

    def __create_sound_controls_widget(self):
        self.__sound_controls_frame = AspectFrame()
        self.__sound_controls_frame.set_margin_bottom(0)
        self.__sound_controls_frame.set_margin_top(0)
        self.__sound_controls_frame.set_margin_start(self.__current_song_and_sound_width -
                                                     SOUND_SLIDER_WIDTH -
                                                     SOUND_CONTROLS_LAYOUT_SPACING -
                                                     SOUND_ICON_SIZE)
        self.__sound_controls_frame.set_margin_end(0)
        self.__box.append(self.__sound_controls_frame)

        self.__sound_controls_box = Box.new(orientation=Gtk.Orientation.HORIZONTAL,
                                            spacing=SOUND_CONTROLS_LAYOUT_SPACING)
        self.__control_slider_box.set_halign(Gtk.Align.END)
        self.__control_slider_box.set_valign(Gtk.Align.CENTER)
        self.__control_slider_box.set_margin_bottom(0)
        self.__control_slider_box.set_margin_top(0)
        self.__control_slider_box.set_margin_start(0)
        self.__control_slider_box.set_margin_end(0)
        self.__sound_controls_frame.set_child(self.__sound_controls_box)

        self.__sound_icon = Image.new_from_file("common/assets/sound.svg")
        self.__sound_icon.set_size_request(SOUND_ICON_SIZE, SOUND_ICON_SIZE)
        self.__sound_controls_box.append(self.__sound_icon)

        self.__sound_slider = Scale()
        self.__sound_slider.set_name("sound_slider")
        self.__sound_slider.set_range(RANGE_MIN, SOUND_RANGE_MAX)
        self.__sound_slider.set_size_request(SOUND_RANGE_MAX, -1)
        self.__sound_slider.connect("value-changed", self.__set_volume)
        self.__sound_slider.set_value(INIT_VOLUME)
        self.__media_player.set_volume(INIT_VOLUME)
        self.__sound_controls_box.append(self.__sound_slider)

    def __set_cover(self):
        if self.__current_song.song_cover_image_stream is not None:
            loader = GdkPixbuf.PixbufLoader.new()
            loader.write(self.__current_song.song_cover_image_stream)
            loader.close()
            pixbuf = loader.get_pixbuf()
        else:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file("common/assets/placeholder.png")
        pixbuf_scaled = pixbuf.scale_simple(
            CURRENT_SONG_COVER_SIZE,
            CURRENT_SONG_COVER_SIZE,
            GdkPixbuf.InterpType.BILINEAR
        )
        self.__cover_image = Image.new_from_pixbuf(pixbuf_scaled)

    def __set_current_song(self, song):
        self.__current_song = song
        self.__title_label.set_label(song.song_title)
        if song.song_author:
            self.__author_label.set_label(song.song_author)
        else:
            self.__author_label.set_visible(False)
        self.__set_cover()

    def __position_changed(self, position):
        self.__playback_slider.set_value(position)
        self.__set_current_time_label(int(position))

    def __source_changed(self, _, __):
        self.__playback_slider.set_range(RANGE_MIN, self.__current_song.song_duration_in_sec)
        self.__total_time_label.set_label(self.__current_song.song_duration)
        self.__update_prev_next_buttons()
        current_song = self.__media_player.get_current_song()
        self.__set_current_song(current_song)

    def __set_position(self, slider):
        position = int(slider.get_value())
        self.__media_player.set_position(position)
        self.__set_current_time_label(position)

    def __set_current_time_label(self, position):
        if self.__current_song_second != position:
            self.__current_time_label.set_label(str(number_to_mins_and_secs(position)))
            self.__current_song_second = position

    def __refresh_current_time_label(self):
        ret, current = self.__media_player.play_bin.query_position(Gst.Format.TIME)
        if ret:
            self.__set_current_time_label(current / Gst.SECOND)
        return True

    def __play_song(self, _):
        if self.__media_player.get_current_playback_state() == Gst.State.PLAYING:
            self.__media_player.pause()
            self.__play_button.set_child(Image.new_from_file("common/assets/play_active.svg"))
        else:
            self.__media_player.play()
            self.__play_button.set_child(Image.new_from_file("common/assets/pause_active.svg"))

    def __set_duration(self, duration):
        self.__playback_slider.set_range(RANGE_MIN, duration)
        self.__total_time_label.set_label(self.__current_song.song_duration)

    def __set_prev_button_disabled(self):
        self.__play_prev_button.set_sensitive(False)
        self.__play_prev_button.set_child(Image.new_from_file("common/assets/play_prev_inactive.svg"))

    def __set_prev_button_active(self):
        self.__play_prev_button.set_sensitive(True)
        self.__play_prev_button.set_child(Image.new_from_file("common/assets/play_prev_active.svg"))

    def __set_next_button_disabled(self):
        self.__play_next_button.set_sensitive(False)
        self.__play_next_button.set_child(Image.new_from_file("common/assets/play_next_inactive.svg"))

    def __set_next_button_active(self):
        self.__play_next_button.set_sensitive(True)
        self.__play_next_button.set_child(Image.new_from_file("common/assets/play_next_active.svg"))

    def __set_volume(self, slider):
        self.__media_player.set_volume(int(slider.get_value()))

    def __play_next(self, _):
        self.__set_prev_button_active()
        self.__media_player.play_next()
        current_song = self.__media_player.get_current_song()
        self.__set_current_song(current_song)

        if self.__media_player.is_current_song_last() and self.__media_player.cycling != Cycling.PLAYLIST_CYCLED:
            self.__set_next_button_disabled()

    def __play_prev(self, _):
        self.__set_next_button_active()
        self.__media_player.play_prev()
        current_song = self.__media_player.get_current_song()
        self.__set_current_song(current_song)
        if self.__media_player.is_current_song_first() and self.__media_player.cycling != Cycling.PLAYLIST_CYCLED:
            self.__set_prev_button_disabled()

    def __cycle(self, _):
        if self.__media_player.cycling == Cycling.PLAYLIST_CYCLED:
            self.__media_player.cycle_one_song()
        elif self.__media_player.cycling == Cycling.SONG_CYCLED:
            self.__media_player.uncycle()
        else:
            self.__media_player.cycle_playlist()

    def __shuffle_songs(self, _):
        if self.__media_player.shuffled:
            self.__media_player.unshuffle()
        else:
            self.__media_player.shuffle()

    def __sound_position_changed(self, _, position):
        self.__sound_slider.set_value(position)

    def __update_prev_next_buttons(self):
        if self.__media_player.is_current_song_first() and self.__media_player.cycling != Cycling.PLAYLIST_CYCLED:
            self.__set_prev_button_disabled()
        else:
            self.__set_prev_button_active()

        if self.__media_player.is_current_song_last() and self.__media_player.cycling != Cycling.PLAYLIST_CYCLED:
            self.__set_next_button_disabled()
        else:
            self.__set_next_button_active()

    def __cycling_changed(self, _, __):
        if self.__media_player.cycling == Cycling.PLAYLIST_CYCLED:
            self.__cycle_button.set_child(Image.new_from_file("common/assets/cycle_list.svg"))
        elif self.__media_player.cycling == Cycling.SONG_CYCLED:
            self.__cycle_button.set_child(Image.new_from_file("common/assets/cycle_one.svg"))
        elif self.__media_player.cycling == Cycling.NO_CYCLING:
            self.__cycle_button.set_child(Image.new_from_file("common/assets/cycle.svg"))

        self.__update_prev_next_buttons()

    def __shuffling_changed(self, _, __):
        if self.__media_player.shuffled:
            self.__shuffle_button.set_child(Image.new_from_file("common/assets/shuffle_active.svg"))
        else:
            self.__shuffle_button.set_child(Image.new_from_file("common/assets/shuffle_inactive.svg"))

        self.__update_prev_next_buttons()

    def __song_deleted(self, _, __):
        self.__update_prev_next_buttons()

    def __songs_added(self, _, __):
        self.__update_prev_next_buttons()

    def __on_state_changed(self, _, __):
        if self.__media_player.get_current_playback_state() == Gst.State.PLAYING:
            self.__play_button.set_child(Image.new_from_file("common/assets/pause_active.svg"))
        else:
            self.__play_button.set_child(Image.new_from_file("common/assets/play_active.svg"))

    def __refresh_slider(self):
        ret, current = self.__media_player.play_bin.query_position(Gst.Format.TIME)
        if ret:
            self.__playback_slider.handler_block(self.__playback_slider_update_signal_id)

            self.__playback_slider.set_value(current / Gst.SECOND)

            self.__playback_slider.handler_unblock(self.__playback_slider_update_signal_id)

        return True
