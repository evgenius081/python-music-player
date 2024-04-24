import random

from PyQt6.QtCore import QUrl, pyqtSignal
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

import config
from common.classes.Cycling import Cycling
from common.classes.FileMetadata import FileMetadata
from common.utils.files import get_all_audio_files, remove_file

MAX_INT = 2147483647


class MediaPlayer(QMediaPlayer):
    cycling_changed = pyqtSignal()
    shuffling_changed = pyqtSignal()
    song_deleted = pyqtSignal(FileMetadata)
    songs_added = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self._audio = QAudioOutput()
        self.setAudioOutput(self._audio)
        self._songs = get_all_audio_files(config.MUSIC_FOLDER_PATH)
        self._songs.sort(key=lambda song: int(song.file_name.split(".")[0]))
        self.mediaStatusChanged.connect(self._media_status_changed)
        self._playlist = self._songs[:]
        self._current_song = self._songs[0]
        self._current_song_index = 0
        self._cycling = Cycling.NO_CYCLING
        self._shuffled = False

    def shuffle(self):
        self._shuffled = True
        random.shuffle(self._playlist)
        self._playlist[self._playlist.index(self._current_song)], self._playlist[0] = (
            self._playlist[0], self._playlist[self._playlist.index(self._current_song)])
        self._current_song_index = self._playlist.index(self._current_song)
        self.shuffling_changed.emit()

    def unshuffle(self):
        self._playlist = self._songs[:]
        self._shuffled = False
        self._current_song_index = self._playlist.index(self._current_song)
        self.shuffling_changed.emit()

    @property
    def songs(self):
        return self._songs

    @property
    def shuffled(self):
        return self._shuffled

    @property
    def cycling(self):
        return self._cycling

    def cycle_one_song(self):
        self._cycling = Cycling.SONG_CYCLED
        self.setLoops(MAX_INT)
        self.cycling_changed.emit()

    def cycle_playlist(self):
        self._cycling = Cycling.PLAYLIST_CYCLED
        self.setLoops(1)
        self.cycling_changed.emit()

    def uncycle(self):
        self._cycling = Cycling.NO_CYCLING
        self.setLoops(1)
        self.cycling_changed.emit()

    def is_current_song_last(self):
        return self._current_song_index == len(self._songs) - 1

    def is_current_song_first(self):
        return self._current_song_index == 0

    def set_volume(self, volume):
        self.audioOutput().setVolume(float(volume/100))

    def play_next(self):
        if self._cycling == Cycling.PLAYLIST_CYCLED and self._current_song_index == len(self._playlist) - 1:
            next_song = self._playlist[0]
        else:
            next_song = self._playlist[self._current_song_index + 1]

        if self.cycling == Cycling.SONG_CYCLED:
            self.uncycle()
        self._set_and_play_song(next_song)

    def play_prev(self):
        if self._cycling == Cycling.PLAYLIST_CYCLED and self._current_song_index == 0:
            prev_song = self._playlist[len(self._playlist) - 1]
        else:
            prev_song = self._playlist[self._current_song_index - 1]
        self._set_and_play_song(prev_song)

    def _set_and_play_song(self, song):
        if len(self._songs) == 1:
            self.setPosition(0)
        else:
            self._current_song = song
            self._current_song_index = self._playlist.index(self._current_song)
            self.pause()
            self.setSource(QUrl.fromLocalFile(self._current_song.full_path))
            self.play()

    def play_song(self, song):
        if self._shuffled:
            self.shuffle()
        self._set_and_play_song(song)

    def get_current_song(self):
        return self._current_song

    def _media_status_changed(self):
        if (self.mediaStatus() == MediaPlayer.MediaStatus.EndOfMedia
                and (self._cycling == Cycling.PLAYLIST_CYCLED or
                     (self._cycling != Cycling.PLAYLIST_CYCLED and not self.is_current_song_last()))):
            self.play_next()
        elif (self.mediaStatus() == MediaPlayer.MediaStatus.EndOfMedia
              and (self._cycling == Cycling.SONG_CYCLED or
                   (self._cycling == Cycling.PLAYLIST_CYCLED and len(self._songs) == 0))):
            self.play()

    def delete_song(self, song):
        song_to_remove = \
            [self._songs[i] for i in range(len(self._songs)) if self._songs[i].file_name == song.file_name][0]
        self._songs.remove(song_to_remove)
        self._playlist.remove(song_to_remove)
        self._current_song_index = self._songs.index(self._current_song)
        self.song_deleted.emit(song)
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

        self.songs_added.emit(new_songs)
