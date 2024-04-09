import random

from PyQt6.QtCore import QUrl, pyqtSignal
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

import config
from common.utils.files import get_all_audio_files
MAX_INT = 2147483647


class MediaPlayer(QMediaPlayer):
    song_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__audio = QAudioOutput()
        self.setAudioOutput(self.__audio)
        self.__songs = get_all_audio_files(config.MUSIC_ABSOLUTE_PATH)
        self.sourceChanged.connect(self.p)
        self.playbackStateChanged.connect(self.__playback_state_changed)
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

    def unshuffle(self):
        self.__playlist = self.__songs[:]
        self.__shuffled = False
        self.__current_song_index = self.__playlist.index(self.__current_song)

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
        self.setLoops(MAX_INT)

    def cycle_playlist(self):
        self.__cycled_playlist = True
        self.__cycled_one_song = False
        self.setLoops(1)

    def p(self):
        print(f"now playing {self.__current_song_index + 1}")

    def uncycle(self):
        self.__cycled_one_song = False
        self.__cycled_playlist = False
        self.setLoops(0)

    def is_current_song_last(self):
        return self.__current_song_index == len(self.__songs) - 1

    def is_current_song_first(self):
        return self.__current_song_index == 0

    def set_volume(self, volume):
        self.audioOutput().setVolume(float(volume/100))

    def play_next(self):
        if self.__cycled_playlist and self.__current_song_index == len(self.__playlist) - 1:
            next_song = self.__playlist[0]
        else:
            next_song = self.__playlist[self.__current_song_index + 1]
        self.__current_song = next_song
        self.__current_song_index = self.__playlist.index(self.__current_song)
        self.setSource(QUrl.fromLocalFile(self.__current_song.full_path))
        self.play()

    def play_prev(self):
        if self.__cycled_playlist and self.__current_song_index == 0:
            prev_song = self.__playlist[len(self.__playlist) - 1]
        else:
            prev_song = self.__playlist[self.__current_song_index - 1]
        self.__current_song = prev_song
        self.__current_song_index = self.__playlist.index(self.__current_song)
        self.setSource(QUrl.fromLocalFile(self.__current_song.full_path))
        self.play()

    def play_song(self, song):
        self.__current_song = song
        self.__current_song_index = self.__playlist.index(self.__current_song)
        self.setSource(QUrl.fromLocalFile(self.__current_song.full_path))
        if self.__shuffled:
            self.shuffle()
        self.play()

    def get_current_song(self):
        return self.__current_song

    def __playback_state_changed(self):
        if self.playbackState() != QMediaPlayer.PlaybackState.PlayingState and self.position() == self.duration():
            self.play_next()

