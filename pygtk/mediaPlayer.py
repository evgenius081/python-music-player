import random

import gi

import config
from common.classes.Cycling import Cycling
from common.utils.files import get_all_audio_files, remove_file

gi.require_version('Gtk', '4.0')
gi.require_version('Gst', '1.0')

from gi.repository import Gst, GObject

Gst.init(None)

MAX_INT = 2147483647


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
        self.__play_bin = Gst.ElementFactory.make("playbin", "player")
        self.__songs = get_all_audio_files(config.MUSIC_FOLDER_PATH)
        self.__songs.sort(key=lambda song: int(song.file_name.split(".")[0]))
        self.__bus = self.__play_bin.get_bus()
        self.__bus.add_signal_watch()
        self.__bus.connect("message::eos", self.__on_eos)
        self.__bus.connect("message::state-changed", self.__on_state_changed)
        self.__bus.connect("message::error", self.on_error)
        self.__play_bin.connect("source-setup", self.__source_changed)
        self.__playlist = self.__songs[:]
        self.__current_song = self.__songs[0]
        self.__play_bin.set_property("uri", f"file:///{self.__current_song.full_path}".replace("\\", "/"))
        self.__current_song_index = 0
        self.__cycling = Cycling.NO_CYCLING
        self.__shuffled = False

    @property
    def play_bin(self):
        return self.__play_bin

    @property
    def bus(self):
        return self.__bus
    
    @property
    def cycling(self):
        return self.__cycling
    
    @cycling.setter
    def cycling(self, value):
        self.__cycling = value

    @property
    def shuffled(self):
        return self.__shuffled

    def shuffle(self, _=None, __=None):
        self.__shuffled = True
        random.shuffle(self.__playlist)
        self.__playlist[self.__playlist.index(self.__current_song)], self.__playlist[0] = (
            self.__playlist[0], self.__playlist[self.__playlist.index(self.__current_song)])
        self.__current_song_index = self.__playlist.index(self.__current_song)
        self.emit("shuffling_changed", True)

    def on_error(self, _, msg):
        err, dbg = msg.parse_error()
        print("ERROR:", msg.src.get_name(), ":", err.message)
        if dbg:
            print("Debug info:", dbg)

    def unshuffle(self, _=None, __=None):
        self.__playlist = self.__songs[:]
        self.__shuffled = False
        self.__current_song_index = self.__playlist.index(self.__current_song)
        self.emit("shuffling_changed", False)

    def get_songs(self):
        return self.__songs

    def cycle_one_song(self, _=None, __=None):
        self.__cycling = Cycling.SONG_CYCLED
        self.unshuffle()
        self.emit("cycling_changed", None)

    def cycle_playlist(self, _=None, __=None):
        self.__cycling = Cycling.PLAYLIST_CYCLED
        self.emit("cycling_changed", None)

    def uncycle(self, _=None, __=None):
        self.__cycling = Cycling.NO_CYCLING
        self.emit("cycling_changed", None)

    def is_current_song_last(self):
        return self.__current_song_index == len(self.__songs) - 1

    def is_current_song_first(self):
        return self.__current_song_index == 0

    def set_volume(self, volume):
        self.__play_bin.set_property("volume", volume/100)
        self.emit("volume_changed", volume)

    def get_volume(self):
        return self.__play_bin.get_property("volume")

    def play_next(self, _=None, __=None):
        self.pause()
        if self.cycling == Cycling.PLAYLIST_CYCLED and self.__current_song_index == len(self.__playlist) - 1:
            next_song = self.__playlist[0]
        else:
            next_song = self.__playlist[self.__current_song_index + 1]

        if self.cycling == Cycling.SONG_CYCLED:
            self.uncycle()
        self.__set_and_play_song(next_song)

    def play_prev(self, _=None, __=None):
        if self.cycling == Cycling.PLAYLIST_CYCLED and self.__current_song_index == 0:
            prev_song = self.__playlist[len(self.__playlist) - 1]
        else:
            prev_song = self.__playlist[self.__current_song_index - 1]
        self.__set_and_play_song(prev_song)

    def __set_and_play_song(self, song):
        if len(self.__songs) == 1:
            self.set_position(0)
        else:
            self.__current_song = song
            self.__current_song_index = self.__playlist.index(self.__current_song)
            self.__play_bin.set_state(Gst.State.NULL)
            self.set_position(0)
            self.emit("source_changed", None)
            self.__play_bin.set_property("uri", f"file:///{self.__current_song.full_path}".replace("\\", "/"))
            self.play()

    def __replay_song(self):
        self.set_position(0)
        self.play()

    def play_song(self, song):
        if self.__shuffled:
            self.shuffle()
        self.__set_and_play_song(song)

    def get_current_song(self):
        return self.__current_song

    def __on_state_changed(self, bus, message):
        old, new, pending = message.parse_state_changed()
        if not message.src == self.__play_bin:
            return

    def get_current_playback_state(self):
        return self.__play_bin.get_state(0)[1]

    def __on_eos(self, _, __):
        if (self.cycling == Cycling.PLAYLIST_CYCLED or 
                (self.cycling == Cycling.NO_CYCLING and not self.is_current_song_last())):
            self.play_next()
        elif self.cycling == Cycling.SONG_CYCLED or (self.cycling == Cycling.PLAYLIST_CYCLED and len(self.__songs) == 0):
            self.__replay_song()

    def delete_song(self, song):
        song_to_remove = \
            [self.__songs[i] for i in range(len(self.__songs)) if self.__songs[i].file_name == song.file_name][0]
        self.__songs.remove(song_to_remove)
        self.__playlist.remove(song_to_remove)
        self.__current_song_index = self.__songs.index(self.__current_song)
        self.emit("song_deleted", song)
        remove_file(song.full_path)

    def add_new_songs(self):
        known_songs_file_names = list(map(lambda song: song.file_name, self.__songs))
        all_songs = get_all_audio_files(config.MUSIC_FOLDER_PATH)
        new_songs = list(filter(lambda song: known_songs_file_names.count(song.file_name) == 0, all_songs))
        new_songs.sort(key=lambda song: int(song.file_name.split(".")[0]))
        self.__songs.extend(new_songs)
        if self.__shuffled:
            self.shuffle()
        else:
            self.__playlist.extend(new_songs)

        self.emit("songs_added", new_songs)

    def play(self, _=None, __=None):
        self.__play_bin.set_state(Gst.State.PLAYING)
        self.emit("playback_state_changed", None)

    def pause(self, _=None, __=None):
        self.__play_bin.set_state(Gst.State.PAUSED)
        self.emit("playback_state_changed", None)

    def __source_changed(self, e, a):
        print(self.__play_bin.query_duration(Gst.Format.TIME))

    def set_position(self, position):
        self.__play_bin.seek_simple(Gst.Format.TIME,
                                    Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
                                    position * Gst.SECOND)

