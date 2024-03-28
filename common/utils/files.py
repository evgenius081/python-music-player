import audio_metadata
import os
from common.classes.fileMetadata import FileMetadata
import config
import shutil


def get_all_audio_files(folder_path):
    files_metadata = []
    for root, _, files in os.walk(os.path.abspath(folder_path)):
        for file in files:
            if file.split(".")[-1] in config.music_file_formats:
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


def is_folder_empty(folder_path):
    folder = os.listdir(folder_path)
    return len(folder) == 0


def clone_file(file_path, dest_folder):
    shutil.copy2(file_path, dest_folder)

