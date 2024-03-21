import audio_metadata
import os
from classes.fileMetadata import FileMetadata

formats = ["mp3", "ogg", "flac",  "wav"]


def get_all_audio_files(folder_path):
    files_metadata = []
    for root, dirs, files in os.walk(os.path.abspath(folder_path)):
        for file in files:
            if file.split(".")[-1] in formats:
                file_path = os.path.join(root, file)
                files_metadata.append(get_file_metadata(file_path))

    for file in files_metadata:
        print(file)

    return files_metadata


def get_file_metadata(file_path):
    metadata = audio_metadata.load(file_path)
    file_metadata = FileMetadata(
        full_path=file_path,
        file_name=file_path.split("\\")[-1],
        song_name=metadata["tags"]["title"][0],
        song_author=metadata["tags"]["artist"][0],
        song_album=metadata["tags"]["album"][0],
        song_duration_in_sec=metadata["streaminfo"]["duration"],
        song_cover_image_stream=metadata["pictures"][0]
    )
    print(metadata["pictures"])
    return file_metadata

get_all_audio_files("C:\\Users\\gulev\\Music\\")

