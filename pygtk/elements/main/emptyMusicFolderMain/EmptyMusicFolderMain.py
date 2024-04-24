import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")

from gi.repository import Gtk, GObject
from gi.repository.Gdk import Cursor

from common.utils.files import clone_and_rename_file
import config

EMPTY_FOLDER_LABEL_HEIGHT = 80
ADD_MUSIC_BUTTON_WIDTH = 257
ADD_MUSIC_BUTTON_HEIGHT = 33
BOX_SPACING = 20


class EmptyMusicFolderMain(Gtk.AspectFrame):
    __gsignals__ = {
        'songs_added': (GObject.SignalFlags.DETAILED, GObject.TYPE_NONE, (GObject.TYPE_OBJECT,)),
    }

    def __init__(self):
        super().__init__()
        self.set_name("empty_music_folder_main")
        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)
        self.set_size_request(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.margin_bottom = 0
        self.margin_top = config.MENU_BAR_HEIGHT
        self.margin_start = 0
        self.margin_end = 0
        self._create_UI()

    def _create_UI(self):
        self._box = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=BOX_SPACING)
        self.set_child(self._box)

        self._create_label()
        self._create_add_button()

    def _create_label(self):
        self._empty_folder_label = Gtk.Label(label='Brak dodanych piosenek')
        self._empty_folder_label.set_name("empty_music_folder_label")
        self._empty_folder_label.set_halign(Gtk.Align.CENTER)
        self._empty_folder_label.set_valign(Gtk.Align.CENTER)
        self._box.append(self._empty_folder_label)

    def _create_add_button(self):
        self._add_music_button = Gtk.Button(label="Dodaj piosenki")
        self._add_music_button.set_name("add_music_button")
        self._add_music_button.set_size_request(ADD_MUSIC_BUTTON_WIDTH, ADD_MUSIC_BUTTON_HEIGHT)
        self._add_music_button.set_cursor(Cursor.new_from_name("pointer"))
        self._add_music_button.connect("clicked", self._add_music_files_action)
        self._box.append(self._add_music_button)

    def _add_music_files_action(self, _):
        file_filters = map(lambda s: f"*.{s}", config.MUSIC_FILE_FORMATS)
        dialog = Gtk.FileChooserNative.new(
            title="Wybierz pliki",
            parent=None,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.set_select_multiple(True)
        dialog.connect("response", self._on_file_chosen)
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Pliki dźwiękowe")
        for file_filter in file_filters:
            filter_text.add_pattern(file_filter)
        dialog.add_filter(filter_text)
        dialog.show()

    def _on_file_chosen(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            for index, file in enumerate(dialog.get_files()):
                clone_and_rename_file(file.get_path(), config.MUSIC_FOLDER_PATH, index + 1)
            self.emit("songs_added", None)
        dialog.destroy()
