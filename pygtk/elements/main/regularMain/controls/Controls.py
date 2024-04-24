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
        self._media_player = media_player
        self._current_song = self._media_player.get_current_song()
        self._media_player.connect("cycling_changed", self._cycling_changed)
        self._media_player.connect("shuffling_changed", self._shuffling_changed)
        self._media_player.connect("song_deleted", self._song_deleted)
        self._media_player.play_bin.connect("source-setup", self._source_changed)
        self._media_player.bus.connect("message::state-changed", self._on_state_changed)
        self._media_player.connect("volume_changed", self._sound_position_changed)
        self._media_player.connect("songs_added", self._songs_added)
        GLib.timeout_add(10, self._refresh_slider)
        GLib.timeout_add(1000, self._refresh_current_time_label)
        self._current_song_second = 0
        self.set_halign(Gtk.Align.START)
        self.set_valign(Gtk.Align.CENTER)
        self.set_xalign(0)
        self.set_name("controls")
        self._current_song_and_sound_width = int((config.WINDOW_WIDTH - config.SLIDER_BLOCK_WIDTH - 10) / 2)
        self._create_UI()

    def _create_UI(self):
        self._box = Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self._box.set_margin_bottom(0)
        self._box.set_margin_top(0)
        self._box.set_margin_start(0)
        self._box.set_margin_end(0)
        self._box.set_halign(Gtk.Align.START)
        self._box.set_valign(Gtk.Align.CENTER)
        self.set_child(self._box)

        self._create_current_song_widget()
        self._create_controls_widget()
        self._create_sound_controls_widget()

    def _create_current_song_widget(self):
        self._current_song_frame = AspectFrame()
        self._current_song_frame.set_size_request(self._current_song_and_sound_width, CURRENT_SONG_WIDGET_HEIGHT)
        self._current_song_frame.set_margin_bottom(0)
        self._current_song_frame.set_margin_top(0)
        self._current_song_frame.set_margin_start(0)
        self._current_song_frame.set_margin_end(0)
        self._current_song_frame.set_halign(Gtk.Align.START)
        self._current_song_frame.set_valign(Gtk.Align.CENTER)
        self._box.append(self._current_song_frame)

        self._current_song_box = Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=CURRENT_SONG_LAYOUT_SPACING)
        self._current_song_box.set_margin_bottom(0)
        self._current_song_box.set_margin_top(0)
        self._current_song_box.set_margin_start(0)
        self._current_song_box.set_margin_end(0)
        self._current_song_box.set_halign(Gtk.Align.START)
        self._current_song_box.set_valign(Gtk.Align.CENTER)
        self._current_song_frame.set_child(self._current_song_box)

        self._cover_image = Image.new()
        self._set_cover()
        self._cover_image.set_name("current_cover_label")
        self._cover_image.set_size_request(CURRENT_SONG_COVER_SIZE, CURRENT_SONG_COVER_SIZE)
        self._current_song_box.append(self._cover_image)

        self._title_author_frame = AspectFrame()
        self._title_author_frame.set_size_request(
            self._current_song_and_sound_width - CURRENT_SONG_COVER_SIZE - CURRENT_SONG_LAYOUT_SPACING,
            TITLE_AUTHOR_WIDGET_HEIGHT
        )
        self._title_author_frame.set_margin_bottom(0)
        self._title_author_frame.set_margin_top(0)
        self._title_author_frame.set_margin_start(0)
        self._title_author_frame.set_margin_end(0)
        self._current_song_box.append(self._title_author_frame)

        self._title_author_box = Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=TITLE_AUTHOR_LAYOUT_SPACING)
        self._title_author_box.set_margin_bottom(0)
        self._title_author_box.set_margin_top(0)
        self._title_author_box.set_margin_start(0)
        self._title_author_box.set_margin_end(0)
        self._title_author_box.set_halign(Gtk.Align.START)
        self._title_author_box.set_valign(Gtk.Align.CENTER)
        self._title_author_frame.set_child(self._title_author_box)

        self._title_label = Label(label=self._current_song.song_title if self._current_song.song_title != "" else
                                  self._current_song.file_name
        )
        self._title_label.set_name("current_song_title_label")
        self._title_label.set_xalign(0)
        self._title_label.set_size_request(
            self._current_song_and_sound_width - CURRENT_SONG_COVER_SIZE - CURRENT_SONG_LAYOUT_SPACING,
            CURRENT_SONG_TITLE_LABEL
        )
        self._title_label.set_margin_bottom(0)
        self._title_label.set_margin_top(0)
        self._title_label.set_margin_start(0)
        self._title_label.set_margin_end(0)
        self._title_author_box.append(self._title_label)

        if self._current_song.song_author != "":
            self._author_label = Label(label=self._current_song.song_author)
            self._author_label.set_name("current_song_author_label")
            self._author_label.set_xalign(0)
            self._author_label.set_margin_bottom(0)
            self._author_label.set_margin_top(0)
            self._author_label.set_margin_start(0)
            self._author_label.set_margin_end(0)
            self._author_label.set_size_request(
                self._current_song_and_sound_width - CURRENT_SONG_COVER_SIZE - CURRENT_SONG_LAYOUT_SPACING,
                CURRENT_SONG_TITLE_LABEL
            )
            self._title_author_box.append(self._author_label)

    def _create_controls_widget(self):
        self._controls_frame = AspectFrame()
        self._controls_frame.set_margin_bottom(0)
        self._controls_frame.set_margin_top(0)
        self._controls_frame.set_margin_start(0)
        self._controls_frame.set_margin_end(0)
        self._controls_frame.set_size_request(config.SLIDER_BLOCK_WIDTH, -1)
        self._box.append(self._controls_frame)

        self._controls_box = Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=CONTROLS_LAYOUT_SPACING)
        self._controls_box.set_halign(Gtk.Align.CENTER)
        self._controls_box.set_valign(Gtk.Align.CENTER)
        self._controls_box.set_margin_bottom(0)
        self._controls_box.set_margin_top(0)
        self._controls_box.set_margin_start(0)
        self._controls_box.set_margin_end(0)
        self._controls_frame.set_child(self._controls_box)

        self._create_buttons()
        self._create_slider()

    def _create_buttons(self):
        self._control_buttons_frame = AspectFrame()
        self._control_buttons_frame.set_margin_bottom(0)
        self._control_buttons_frame.set_margin_top(0)
        self._control_buttons_frame.set_margin_start(0)
        self._control_buttons_frame.set_margin_end(0)
        self._controls_box.append(self._control_buttons_frame)

        self._control_buttons_box = Box.new(orientation=Gtk.Orientation.HORIZONTAL,
                                            spacing=CONTROL_BUTTONS_LAYOUT_SPACING
        )
        self._control_buttons_box.set_halign(Gtk.Align.CENTER)
        self._control_buttons_box.set_valign(Gtk.Align.CENTER)
        self._control_buttons_box.set_margin_bottom(0)
        self._control_buttons_box.set_margin_top(0)
        self._control_buttons_box.set_margin_start(0)
        self._control_buttons_box.set_margin_end(0)
        self._control_buttons_frame.set_child(self._control_buttons_box)

        self._shuffle_button = Button(label="")
        self._shuffle_button.set_child(Image.new_from_file("common/assets/shuffle_inactive.svg"))
        self._shuffle_button.set_name("shuffle_button")
        self._shuffle_button.set_cursor(Gdk.Cursor.new_from_name("pointer"))
        self._shuffle_button.set_size_request(CONTROL_BUTTON_SIZE, CONTROL_BUTTON_SIZE)
        self._shuffle_button.connect("clicked", self._shuffle_songs)
        self._control_buttons_box.append(self._shuffle_button)

        self._play_prev_button = Button(label="")
        self._play_prev_button.set_name("play_prev_button")
        self._play_prev_button.set_cursor(Gdk.Cursor.new_from_name("pointer"))
        self._play_prev_button.set_size_request(CONTROL_BUTTON_SIZE, CONTROL_BUTTON_SIZE)
        self._play_prev_button.connect("clicked", self._play_prev)
        self._control_buttons_box.append(self._play_prev_button)

        self._play_button = Button(label="")
        self._play_button.set_child(Image.new_from_file("common/assets/play_active.svg"))
        self._play_button.set_name("play_button")
        self._play_button.set_cursor(Gdk.Cursor.new_from_name("pointer"))
        self._play_button.set_size_request(PLAY_BUTTON_SIZE, PLAY_BUTTON_SIZE)
        self._play_button.connect("clicked", self._play_song)
        self._control_buttons_box.append(self._play_button)

        self._play_next_button = Button(label="")
        self._play_next_button.set_name("play_next_button")
        self._play_next_button.set_cursor(Gdk.Cursor.new_from_name("pointer"))
        self._play_next_button.set_size_request(CONTROL_BUTTON_SIZE, CONTROL_BUTTON_SIZE)
        self._play_next_button.connect("clicked", self._play_next)
        self._control_buttons_box.append(self._play_next_button)

        self._cycle_button = Button(label="")
        self._cycle_button.set_child(Image.new_from_file("common/assets/cycle.svg"))
        self._cycle_button.set_name("cycle_button")
        self._cycle_button.set_cursor(Gdk.Cursor.new_from_name("pointer"))
        self._cycle_button.set_size_request(CONTROL_BUTTON_SIZE, CONTROL_BUTTON_SIZE)
        self._cycle_button.connect("clicked", self._cycle)
        self._control_buttons_box.append(self._cycle_button)

        self._update_prev_next_buttons()

    def _create_slider(self):
        self._control_slider_frame = AspectFrame()
        self._control_slider_frame.set_margin_bottom(0)
        self._control_slider_frame.set_margin_top(0)
        self._control_slider_frame.set_margin_start(0)
        self._control_slider_frame.set_margin_end(0)
        self._control_slider_frame.set_size_request(config.SLIDER_BLOCK_WIDTH, CONTROL_SLIDER_WIDGET_HEIGHT)
        self._controls_box.append(self._control_slider_frame)

        self._control_slider_box = Box.new(orientation=Gtk.Orientation.HORIZONTAL,
                                           spacing=CONTROL_SLIDER_LAYOUT_SPACING)
        self._control_slider_box.set_halign(Gtk.Align.CENTER)
        self._control_slider_box.set_valign(Gtk.Align.CENTER)
        self._control_slider_box.set_margin_bottom(0)
        self._control_slider_box.set_margin_top(0)
        self._control_slider_box.set_margin_start(0)
        self._control_slider_box.set_margin_end(0)
        self._control_slider_frame.set_child(self._control_slider_box)

        self._current_time_label = Label(label=" 0:00")
        self._current_time_label.set_name("current_playback_time_label")
        self._control_slider_box.append(self._current_time_label)

        self._playback_slider = Scale()
        self._playback_slider.set_name("playback_slider")
        self._playback_slider_update_signal_id = self._playback_slider.connect(
            "value-changed",
            self._set_position)
        self._playback_slider.set_size_request(config.SLIDER_BLOCK_WIDTH, -1)
        self._control_slider_box.append(self._playback_slider)

        self._total_time_label = Label(label=self._current_song.song_duration)
        self._total_time_label.set_name("total_playback_time_label")
        self._control_slider_box.append(self._total_time_label)

    def _create_sound_controls_widget(self):
        self._sound_controls_frame = AspectFrame()
        self._sound_controls_frame.set_margin_bottom(0)
        self._sound_controls_frame.set_margin_top(0)
        self._sound_controls_frame.set_margin_start(self._current_song_and_sound_width -
                                                    SOUND_SLIDER_WIDTH -
                                                    SOUND_CONTROLS_LAYOUT_SPACING -
                                                    SOUND_ICON_SIZE)
        self._sound_controls_frame.set_margin_end(0)
        self._box.append(self._sound_controls_frame)

        self._sound_controls_box = Box.new(orientation=Gtk.Orientation.HORIZONTAL,
                                           spacing=SOUND_CONTROLS_LAYOUT_SPACING)
        self._control_slider_box.set_halign(Gtk.Align.END)
        self._control_slider_box.set_valign(Gtk.Align.CENTER)
        self._control_slider_box.set_margin_bottom(0)
        self._control_slider_box.set_margin_top(0)
        self._control_slider_box.set_margin_start(0)
        self._control_slider_box.set_margin_end(0)
        self._sound_controls_frame.set_child(self._sound_controls_box)

        self._sound_icon = Image.new_from_file("common/assets/sound.svg")
        self._sound_icon.set_size_request(SOUND_ICON_SIZE, SOUND_ICON_SIZE)
        self._sound_controls_box.append(self._sound_icon)

        self._sound_slider = Scale()
        self._sound_slider.set_name("sound_slider")
        self._sound_slider.set_range(RANGE_MIN, SOUND_RANGE_MAX)
        self._sound_slider.set_size_request(SOUND_RANGE_MAX, -1)
        self._sound_slider.connect("value-changed", self._set_volume)
        self._sound_slider.set_value(INIT_VOLUME)
        self._media_player.set_volume(INIT_VOLUME)
        self._sound_controls_box.append(self._sound_slider)

    def _set_cover(self):
        if self._current_song.song_cover_bytes is not None:
            loader = GdkPixbuf.PixbufLoader.new()
            loader.write(self._current_song.song_cover_bytes)
            loader.close()
            pixbuf = loader.get_pixbuf()
        else:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file("common/assets/placeholder.png")
        pixbuf_scaled = pixbuf.scale_simple(
            CURRENT_SONG_COVER_SIZE,
            CURRENT_SONG_COVER_SIZE,
            GdkPixbuf.InterpType.BILINEAR
        )
        self._cover_image = Image.new_from_pixbuf(pixbuf_scaled)

    def _set_current_song(self, song):
        self._current_song = song
        self._title_label.set_label(song.song_title)
        if song.song_author:
            self._author_label.set_label(song.song_author)
        else:
            self._author_label.set_visible(False)
        self._set_cover()

    def _position_changed(self, position):
        self._playback_slider.set_value(position)
        self._set_current_time_label(int(position))

    def _source_changed(self, _, __):
        self._playback_slider.set_range(RANGE_MIN, self._current_song.song_duration_in_sec)
        self._total_time_label.set_label(self._current_song.song_duration)
        self._update_prev_next_buttons()
        current_song = self._media_player.get_current_song()
        self._set_current_song(current_song)

    def _set_position(self, slider):
        position = int(slider.get_value())
        self._media_player.set_position(position)
        self._set_current_time_label(position)

    def _set_current_time_label(self, position):
        if self._current_song_second != position:
            self._current_time_label.set_label(str(number_to_mins_and_secs(position)))
            self._current_song_second = position

    def _refresh_current_time_label(self):
        ret, current = self._media_player.play_bin.query_position(Gst.Format.TIME)
        if ret:
            self._set_current_time_label(current / Gst.SECOND)
        return True

    def _play_song(self, _):
        if self._media_player.get_current_playback_state() == Gst.State.PLAYING:
            self._media_player.pause()
            self._play_button.set_child(Image.new_from_file("common/assets/play_active.svg"))
        else:
            self._media_player.play()
            self._play_button.set_child(Image.new_from_file("common/assets/pause_active.svg"))

    def _set_duration(self, duration):
        self._playback_slider.set_range(RANGE_MIN, duration)
        self._total_time_label.set_label(self._current_song.song_duration)

    def _set_prev_button_disabled(self):
        self._play_prev_button.set_sensitive(False)
        self._play_prev_button.set_child(Image.new_from_file("common/assets/play_prev_inactive.svg"))

    def _set_prev_button_active(self):
        self._play_prev_button.set_sensitive(True)
        self._play_prev_button.set_child(Image.new_from_file("common/assets/play_prev_active.svg"))

    def _set_next_button_disabled(self):
        self._play_next_button.set_sensitive(False)
        self._play_next_button.set_child(Image.new_from_file("common/assets/play_next_inactive.svg"))

    def _set_next_button_active(self):
        self._play_next_button.set_sensitive(True)
        self._play_next_button.set_child(Image.new_from_file("common/assets/play_next_active.svg"))

    def _set_volume(self, slider):
        self._media_player.set_volume(int(slider.get_value()))

    def _play_next(self, _):
        self._set_prev_button_active()
        self._media_player.play_next()
        current_song = self._media_player.get_current_song()
        self._set_current_song(current_song)

        if self._media_player.is_current_song_last() and self._media_player.cycling != Cycling.PLAYLIST_CYCLED:
            self._set_next_button_disabled()

    def _play_prev(self, _):
        self._set_next_button_active()
        self._media_player.play_prev()
        current_song = self._media_player.get_current_song()
        self._set_current_song(current_song)
        if self._media_player.is_current_song_first() and self._media_player.cycling != Cycling.PLAYLIST_CYCLED:
            self._set_prev_button_disabled()

    def _cycle(self, _):
        if self._media_player.cycling == Cycling.PLAYLIST_CYCLED:
            self._media_player.cycle_one_song()
        elif self._media_player.cycling == Cycling.SONG_CYCLED:
            self._media_player.uncycle()
        else:
            self._media_player.cycle_playlist()

    def _shuffle_songs(self, _):
        if self._media_player.shuffled:
            self._media_player.unshuffle()
        else:
            self._media_player.shuffle()

    def _sound_position_changed(self, _, position):
        self._sound_slider.set_value(position)

    def _update_prev_next_buttons(self):
        if self._media_player.is_current_song_first() and self._media_player.cycling != Cycling.PLAYLIST_CYCLED:
            self._set_prev_button_disabled()
        else:
            self._set_prev_button_active()

        if self._media_player.is_current_song_last() and self._media_player.cycling != Cycling.PLAYLIST_CYCLED:
            self._set_next_button_disabled()
        else:
            self._set_next_button_active()

    def _cycling_changed(self, _, __):
        if self._media_player.cycling == Cycling.PLAYLIST_CYCLED:
            self._cycle_button.set_child(Image.new_from_file("common/assets/cycle_list.svg"))
        elif self._media_player.cycling == Cycling.SONG_CYCLED:
            self._cycle_button.set_child(Image.new_from_file("common/assets/cycle_one.svg"))
        elif self._media_player.cycling == Cycling.NO_CYCLING:
            self._cycle_button.set_child(Image.new_from_file("common/assets/cycle.svg"))

        self._update_prev_next_buttons()

    def _shuffling_changed(self, _, __):
        if self._media_player.shuffled:
            self._shuffle_button.set_child(Image.new_from_file("common/assets/shuffle_active.svg"))
        else:
            self._shuffle_button.set_child(Image.new_from_file("common/assets/shuffle_inactive.svg"))

        self._update_prev_next_buttons()

    def _song_deleted(self, _, __):
        self._update_prev_next_buttons()

    def _songs_added(self, _, __):
        self._update_prev_next_buttons()

    def _on_state_changed(self, _, __):
        if self._media_player.get_current_playback_state() == Gst.State.PLAYING:
            self._play_button.set_child(Image.new_from_file("common/assets/pause_active.svg"))
        else:
            self._play_button.set_child(Image.new_from_file("common/assets/play_active.svg"))

    def _refresh_slider(self):
        ret, current = self._media_player.play_bin.query_position(Gst.Format.TIME)
        if ret:
            self._playback_slider.handler_block(self._playback_slider_update_signal_id)
            self._playback_slider.set_value(current / Gst.SECOND)
            self._playback_slider.handler_unblock(self._playback_slider_update_signal_id)

        return True
