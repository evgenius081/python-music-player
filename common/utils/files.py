from io import BytesIO

import os

import music_tag

from common.classes.fileMetadata import FileMetadata
import config
import shutil


def get_all_audio_files(folder_path):
    files_metadata = []
    for root, _, files in os.walk(os.path.abspath(folder_path)):
        for file in files:
            if file.split(".")[-1] in config.MUSIC_FILE_FORMATS:
                file_path = os.path.join(root, file)
                files_metadata.append(get_file_metadata(file_path))

    return files_metadata


def get_file_metadata(file_path):
    metadata = music_tag.load_file(file_path)
    file_metadata = FileMetadata(
        full_path=file_path,
        file_name=file_path.split("\\")[-1],
        song_title=metadata["tracktitle"].value,
        song_author=metadata["artist"].value,
        song_album=metadata["album"].value,
        song_duration_in_sec=metadata["#length"].value,
        song_cover_image_stream=BytesIO(metadata["artwork"].first.data).getvalue()
    )
    return file_metadata


def set_file_metadata(file_metadata):
    metadata = music_tag.load_file(file_metadata.full_path)
    metadata["tracktitle"] = file_metadata.song_title
    metadata["artist"] = file_metadata.song_author
    metadata["album"] = file_metadata.song_album
    metadata["artwork"] = file_metadata.song_cover_image_stream
    metadata.save()


def is_folder_empty(folder_path):
    folder = os.listdir(folder_path)
    return len(folder) == 0


def clone_and_rename_file(file_path, dest_folder, new_name):
    new_file_path = shutil.copy2(file_path, dest_folder)
    extension = file_path.split(".")[-1]
    os.rename(new_file_path, f"{dest_folder}/{new_name}.{extension}")


def remove_file(file_path):
    os.remove(file_path)

