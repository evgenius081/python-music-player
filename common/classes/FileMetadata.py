from common.utils.formatter import number_to_mins_and_secs


class FileMetadata:
    def __init__(self,
                 full_path="",
                 file_name="",
                 song_title="",
                 song_author="",
                 song_album="",
                 song_duration_in_sec=0,
                 song_cover_bytes=None):
        self._full_path = full_path
        self._file_name = file_name
        self._song_title = song_title
        self._song_author = song_author
        self._song_album = song_album
        self._song_duration_in_sec = song_duration_in_sec
        self._song_cover_bytes = song_cover_bytes
        self._song_duration = number_to_mins_and_secs(song_duration_in_sec)
        
    @property
    def full_path(self):
        return self._full_path

    @property
    def file_name(self):
        return self._file_name

    @property
    def song_title(self):
        return self._song_title

    @property
    def song_author(self):
        return self._song_author

    @property
    def song_album(self):
        return self._song_album

    @property
    def song_duration_in_sec(self):
        return self._song_duration_in_sec

    @property
    def song_cover_bytes(self):
        return self._song_cover_bytes

    @property
    def song_duration(self):
        return self._song_duration

    def _str__(self):
        return (f"full path: {self._full_path}, file name: {self._file_name}, song name: {self._song_title}, "
                f"song author: {self._song_author}, song album: {self._song_album}, "
                f"duration [s]: {self._song_duration_in_sec}")
