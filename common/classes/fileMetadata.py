class FileMetadata:
    def __init__(self,
                 full_path="",
                 file_name="",
                 song_name="",
                 song_author="",
                 song_album="",
                 song_duration_in_sec=0,
                 song_cover_image_stream=None):
        self.full_path = full_path
        self.file_name = file_name
        self.song_name = song_name
        self.song_author = song_author
        self.song_album = song_album
        self.song_duration_in_sec = song_duration_in_sec
        self.song_cover_image_stream = song_cover_image_stream

    def __str__(self):
        return (f"full path: {self.full_path}, file name: {self.file_name}, song name: {self.song_name}, "
                f"song author: {self.song_author}, song album: {self.song_album}, "
                f"duration [s]: {self.song_duration_in_sec}")
