import random

import gi

import config
from common.classes.fileMetadata import FileMetadata
from common.utils.files import get_all_audio_files, remove_file

gi.require_version('Gtk', '4.0')
gi.require_version('Gst', '4.0')

from gi.repository import Gtk, Gdk, Gst

MAX_INT = 2147483647


class MediaPlayer():
    # cycling_changed = pyqtSignal()
    # shuffling_changed = pyqtSignal()
    # song_deleted = pyqtSignal(FileMetadata)
    # songs_added = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.__play_bin = Gst.ElementFactory.make("playbin", None)
        self.__songs = get_all_audio_files(config.MUSIC_FOLDER_PATH)
        self.__songs.sort(key=lambda song: int(song.file_name.split(".")[0]))
        self.__bus = self.__play_bin.get_bus()
        self.__bus.add_signal_watch()
        self.__bus.connect("message::eos", self.__on_eos)
        self.__bus.connect("message::state-changed", self.__on_state_changed)
        self.__bus.connect("message::application", self.__on_application_message)
        self.__playlist = self.__songs[:]
        self.__current_song = self.__songs[0]
        self.__current_song_index = 0
        self.__cycled_one_song = False
        self.__cycled_playlist = False
        self.__shuffled = False

    def shuffle(self):
        self.__shuffled = True
        random.shuffle(self.__playlist)
        self.__playlist[self.__playlist.index(self.__current_song)], self.__playlist[0] = (
            self.__playlist[0], self.__playlist[self.__playlist.index(self.__current_song)])
        self.__current_song_index = self.__playlist.index(self.__current_song)
        # self.shuffling_changed.emit()

    def unshuffle(self):
        self.__playlist = self.__songs[:]
        self.__shuffled = False
        self.__current_song_index = self.__playlist.index(self.__current_song)
        # self.shuffling_changed.emit()

    def get_songs(self):
        return self.__songs

    def get_shuffled(self):
        return self.__shuffled

    def get_cycled_one_song(self):
        return self.__cycled_one_song

    def get_cycled_playlist(self):
        return self.__cycled_playlist

    def cycle_one_song(self):
        self.__cycled_one_song = True
        self.__cycled_playlist = False
        self.__play_bin.set_property("repeat", True)
        # self.cycling_changed.emit()

    def cycle_playlist(self):
        self.__cycled_playlist = True
        self.__cycled_one_song = False
        self.__play_bin.set_property("repeat", False)
        # self.cycling_changed.emit()

    def uncycle(self):
        self.__cycled_one_song = False
        self.__cycled_playlist = False
        self.__play_bin.set_property("repeat", False)
        # self.cycling_changed.emit()

    def is_current_song_last(self):
        return self.__current_song_index == len(self.__songs) - 1

    def is_current_song_first(self):
        return self.__current_song_index == 0

    def set_volume(self, volume):
        self.__play_bin.set_property("volume", volume)

    def play_next(self):
        if self.__cycled_playlist and self.__current_song_index == len(self.__playlist) - 1:
            next_song = self.__playlist[0]
        else:
            next_song = self.__playlist[self.__current_song_index + 1]

        if self.__cycled_one_song:
            self.uncycle()
        self.__set_and_play_song(next_song)

    def play_prev(self):
        if self.__cycled_playlist and self.__current_song_index == 0:
            prev_song = self.__playlist[len(self.__playlist) - 1]
        else:
            prev_song = self.__playlist[self.__current_song_index - 1]
        self.__set_and_play_song(prev_song)

    def __set_and_play_song(self, song):
        if len(self.__songs) == 1:
            self.__play_bin.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, 0)
        else:
            self.__current_song = song
            self.__current_song_index = self.__playlist.index(self.__current_song)
            self.__play_bin.set_property("uri", f"file://{self.__current_song.full_path}")
            self.__play_bin.set_state(Gst.State.PLAYING)

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

        self.state = new
        print(f"State changed from {Gst.Element.state_get_name(old)} to {Gst.Element.state_get_name(new)}")
        # if (self.mediaStatus() == MediaPlayer.MediaStatus.EndOfMedia
        #         and (self.__cycled_playlist or (not self.__cycled_playlist and not self.is_current_song_last()))):
        #     self.play_next()
        # elif (self.mediaStatus() == MediaPlayer.MediaStatus.EndOfMedia
        #       and (self.__cycled_one_song or (self.__cycled_playlist and len(self.__songs) == 0))):
        #     self.__play_bin.set_state(Gst.State.PLAYING)

    def on_eos(self, _, __):
        print("End-Of-Stream reached")
        self.__play_bin.set_state(Gst.State.READY)

    def on_application_message(self, _, message):
        print(message.get_structure().get_name())
        # if message.get_structure().get_name() == "tags-changed":
            # if the message is the "tags-changed", update the stream info in
            # the GUI
            # self.analyze_streams()

    def delete_song(self, song):
        song_to_remove = \
            [self.__songs[i] for i in range(len(self.__songs)) if self.__songs[i].file_name == song.file_name][0]
        self.__songs.remove(song_to_remove)
        self.__playlist.remove(song_to_remove)
        self.__current_song_index = self.__songs.index(self.__current_song)
        # self.song_deleted.emit(song)
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

        # self.songs_added.emit(new_songs)
