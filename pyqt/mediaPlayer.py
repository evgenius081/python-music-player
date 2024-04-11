import random

from PyQt6.QtCore import QUrl, pyqtSignal
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

import config
from common.classes.fileMetadata import FileMetadata
from common.utils.files import get_all_audio_files, remove_file

MAX_INT = 2147483647


class MediaPlayer(QMediaPlayer):
    cycling_changed = pyqtSignal()
    shuffling_changed = pyqtSignal()
    song_deleted = pyqtSignal(FileMetadata)

    def __init__(self):
        super().__init__()
        self.__audio = QAudioOutput()
        self.setAudioOutput(self.__audio)
        self.__songs = get_all_audio_files(config.MUSIC_FOLDER_PATH)
        self.mediaStatusChanged.connect(self.__media_status_changed)
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
        self.shuffling_changed.emit()

    def unshuffle(self):
        self.__playlist = self.__songs[:]
        self.__shuffled = False
        self.__current_song_index = self.__playlist.index(self.__current_song)
        self.shuffling_changed.emit()

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
        self.cycling_changed.emit()

    def cycle_playlist(self):
        self.__cycled_playlist = True
        self.__cycled_one_song = False
        self.setLoops(1)
        self.cycling_changed.emit()

    def uncycle(self):
        self.__cycled_one_song = False
        self.__cycled_playlist = False
        self.setLoops(1)
        self.cycling_changed.emit()

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
        self.__current_song = song
        self.__current_song_index = self.__playlist.index(self.__current_song)
        self.pause()
        self.setSource(QUrl.fromLocalFile(self.__current_song.full_path))
        self.play()

    def play_song(self, song):
        if self.__shuffled:
            self.shuffle()
        self.__set_and_play_song(song)

    def get_current_song(self):
        return self.__current_song

    def __media_status_changed(self):
        if self.playbackState() == QMediaPlayer.PlaybackState.PlayingState and self.mediaStatus() == MediaPlayer.MediaStatus.EndOfMedia and not self.__cycled_one_song:
            self.play_next()
        elif self.mediaStatus() == MediaPlayer.MediaStatus.EndOfMedia and self.__cycled_one_song:
            self.play()

    def delete_song(self, song):
        song_to_remove = \
            [self.__songs[i] for i in range(len(self.__songs)) if self.__songs[i].file_name == song.file_name][0]
        self.__songs.remove(song_to_remove)
        self.__playlist.remove(song_to_remove)
        self.__current_song_index = self.__songs.index(self.__current_song)
        self.song_deleted.emit(song)
        # remove_file(song.full_path)

