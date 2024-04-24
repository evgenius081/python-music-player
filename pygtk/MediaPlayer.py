import random

import gi

import config
from common.classes.Cycling import Cycling
from common.utils.files import get_all_audio_files, remove_file

gi.require_version('Gtk', '4.0')
gi.require_version('Gst', '1.0')

from gi.repository import Gst, GObject

Gst.init(None)


class MediaPlayer(GObject.Object):
    __gsignals__ = {
        'cycling_changed': (GObject.SignalFlags.DETAILED, GObject.TYPE_NONE, (GObject.TYPE_OBJECT,)),
        'shuffling_changed': (GObject.SignalFlags.DETAILED, GObject.TYPE_NONE, (GObject.TYPE_BOOLEAN,)),
        'song_deleted': (GObject.SignalFlags.DETAILED, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
        'songs_added': (GObject.SignalFlags.DETAILED, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
        'source_changed': (GObject.SignalFlags.DETAILED, GObject.TYPE_NONE, (GObject.TYPE_OBJECT,)),
        'volume_changed': (GObject.SignalFlags.DETAILED, GObject.TYPE_NONE, (GObject.TYPE_FLOAT,)),
        'playback_state_changed': (GObject.SignalFlags.DETAILED, GObject.TYPE_NONE, (GObject.TYPE_OBJECT,)),
    }

    def __init__(self):
        super(MediaPlayer, self).__init__()
        Gst.init_check(None)
        self.IS_GST010 = Gst.version()[0] == 0
        self._play_bin = Gst.ElementFactory.make("playbin", "player")
        self._songs = get_all_audio_files(config.MUSIC_FOLDER_PATH)
        self._songs.sort(key=lambda song: int(song.file_name.split(".")[0]))
        self._bus = self._play_bin.get_bus()
        self._bus.add_signal_watch()
        self._bus.connect("message::eos", self._on_eos)
        self._playlist = self._songs[:]
        self._current_song = self._songs[0]
        self._play_bin.set_property(
            "uri", f"file:///{self._current_song.full_path}".replace("\\", "/")
        )
        self._current_song_index = 0
        self._cycling = Cycling.NO_CYCLING
        self._shuffled = False

    @property
    def play_bin(self):
        return self._play_bin

    @property
    def bus(self):
        return self._bus

    @property
    def cycling(self):
        return self._cycling

    @cycling.setter
    def cycling(self, value):
        self._cycling = value

    @property
    def shuffled(self):
        return self._shuffled

    @property
    def songs(self):
        return self._songs

    def shuffle(self, _=None, __=None):
        self._shuffled = True
        random.shuffle(self._playlist)
        self._playlist[self._playlist.index(self._current_song)], self._playlist[0] = (
            self._playlist[0], self._playlist[self._playlist.index(self._current_song)])
        self._current_song_index = self._playlist.index(self._current_song)
        self.emit("shuffling_changed", True)

    def unshuffle(self, _=None, __=None):
        self._playlist = self._songs[:]
        self._shuffled = False
        self._current_song_index = self._playlist.index(self._current_song)
        self.emit("shuffling_changed", False)

    def cycle_one_song(self, _=None, __=None):
        self._cycling = Cycling.SONG_CYCLED
        self.unshuffle()
        self.emit("cycling_changed", None)

    def cycle_playlist(self, _=None, __=None):
        self._cycling = Cycling.PLAYLIST_CYCLED
        self.emit("cycling_changed", None)

    def uncycle(self, _=None, __=None):
        self._cycling = Cycling.NO_CYCLING
        self.emit("cycling_changed", None)

    def is_current_song_last(self):
        return self._current_song_index == len(self._songs) - 1

    def is_current_song_first(self):
        return self._current_song_index == 0

    def set_volume(self, volume):
        self._play_bin.set_property("volume", volume / 100)
        self.emit("volume_changed", volume)

    def get_volume(self):
        return self._play_bin.get_property("volume")

    def play_next(self, _=None, __=None):
        self.pause()
        if self.cycling == Cycling.PLAYLIST_CYCLED and self._current_song_index == len(self._playlist) - 1:
            next_song = self._playlist[0]
        else:
            next_song = self._playlist[self._current_song_index + 1]

        if self.cycling == Cycling.SONG_CYCLED:
            self.uncycle()
        self._set_and_play_song(next_song)

    def play_prev(self, _=None, __=None):
        if self.cycling == Cycling.PLAYLIST_CYCLED and self._current_song_index == 0:
            prev_song = self._playlist[len(self._playlist) - 1]
        else:
            prev_song = self._playlist[self._current_song_index - 1]
        self._set_and_play_song(prev_song)

    def _set_and_play_song(self, song):
        if len(self._songs) == 1:
            self.set_position(0)
        else:
            self._current_song = song
            self._current_song_index = self._playlist.index(self._current_song)
            self._play_bin.set_state(Gst.State.NULL)
            self.set_position(0)
            self.emit("source_changed", None)
            self._play_bin.set_property(
                "uri", f"file:///{self._current_song.full_path}".replace("\\", "/")
            )
            self.play()

    def _replay_song(self):
        self.set_position(0)
        self.play()

    def play_song(self, song):
        if self._shuffled:
            self.shuffle()
        self._set_and_play_song(song)

    def get_current_song(self):
        return self._current_song

    def get_current_playback_state(self):
        return self._play_bin.get_state(0)[1]

    def _on_eos(self, _, __):
        if (self.cycling == Cycling.PLAYLIST_CYCLED or
                (self.cycling == Cycling.NO_CYCLING and not self.is_current_song_last())):
            self.play_next()
        elif self.cycling == Cycling.SONG_CYCLED or (self.cycling == Cycling.PLAYLIST_CYCLED and len(self._songs) == 0):
            self._replay_song()

    def delete_song(self, song):
        song_to_remove = \
            [self._songs[i] for i in range(len(self._songs)) if self._songs[i].file_name == song.file_name][0]
        self._songs.remove(song_to_remove)
        self._playlist.remove(song_to_remove)
        self._current_song_index = self._songs.index(self._current_song)
        self.emit("song_deleted", song)
        remove_file(song.full_path)

    def add_new_songs(self):
        known_songs_file_names = list(map(lambda song: song.file_name, self._songs))
        all_songs = get_all_audio_files(config.MUSIC_FOLDER_PATH)
        new_songs = list(filter(lambda song: known_songs_file_names.count(song.file_name) == 0, all_songs))
        new_songs.sort(key=lambda song: int(song.file_name.split(".")[0]))
        self._songs.extend(new_songs)
        if self._shuffled:
            self.shuffle()
        else:
            self._playlist.extend(new_songs)

        self.emit("songs_added", new_songs)

    def play(self, _=None, __=None):
        self._play_bin.set_state(Gst.State.PLAYING)
        self.emit("playback_state_changed", None)

    def pause(self, _=None, __=None):
        self._play_bin.set_state(Gst.State.PAUSED)
        self.emit("playback_state_changed", None)

    def set_position(self, position):
        self._play_bin.seek_simple(Gst.Format.TIME,
                                   Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
                                   position * Gst.SECOND
                                   )
