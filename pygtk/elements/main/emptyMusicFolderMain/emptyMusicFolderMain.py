import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")

from gi.repository import Gtk
from gi.repository.Gdk import Cursor

from common.utils.files import clone_and_rename_file
import config

EMPTY_FOLDER_LABEL_HEIGHT = 80
ADD_MUSIC_BUTTON_WIDTH = 257
ADD_MUSIC_BUTTON_HEIGHT = 33
BOX_SPACING = 20


class EmptyMusicFolderMain(Gtk.AspectFrame):
    # songs_added = pyqtSignal()

    def __init__(self):
        super().__init__()
        # self.set(config.WINDOW_WIDTH)
        # self.setFixedHeight(config.WINDOW_HEIGHT-config.MENU_BAR_HEIGHT)
        self.set_name("empty_music_folder_main")
        self.layout = None
        self.empty_folder_label = None
        self.add_music_button = None
        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)
        self.set_hexpand(config.WINDOW_WIDTH)
        self.set_vexpand(config.WINDOW_HEIGHT)
        self.margin_bottom = 0
        self.margin_top = config.MENU_BAR_HEIGHT
        self.margin_start = 0
        self.margin_end = 0
        self.__create_UI()

    def __create_UI(self):
        self.__box = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=BOX_SPACING)
        self.set_child(self.__box)

        self.__create_label()
        self.__create_add_button()

    def __create_label(self):
        self.__empty_folder_label = Gtk.Label(label='Brak dodanych piosenek')
        self.__empty_folder_label.set_name("empty_music_folder_label")
        self.__empty_folder_label.set_halign(Gtk.Align.CENTER)
        self.__empty_folder_label.set_valign(Gtk.Align.CENTER)
        self.__box.append(self.__empty_folder_label)

    def __create_add_button(self):
        self.__add_music_button = Gtk.Button(label="Dodaj piosenki")
        self.__add_music_button.set_name("add_music_button")
        self.__add_music_button.set_hexpand(ADD_MUSIC_BUTTON_WIDTH)
        self.__add_music_button.set_vexpand(ADD_MUSIC_BUTTON_HEIGHT)
        self.__add_music_button.set_cursor(Cursor.new_from_name("pointer"))
        self.__add_music_button.connect("clicked", self._add_music_files_action)
        self.__box.append(self.__add_music_button)

    def _add_music_files_action(self, _):
        file_filters = map(lambda s: f"*.{s}", config.MUSIC_FILE_FORMATS)
        dialog = Gtk.FileChooserNative.new(
            title="Wybierz pliki",
            parent=None,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.set_select_multiple(True)
        dialog.connect("response", self.__on_file_chosen)
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Pliki dźwiękowe")
        for file_filter in file_filters:
            filter_text.add_pattern(file_filter)
        dialog.add_filter(filter_text)
        dialog.show()

    def __on_file_chosen(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            for index, file in enumerate(dialog.get_files()):
                clone_and_rename_file(file.get_path(), config.MUSIC_FOLDER_PATH, index + 1)
            # self.songs_added.emit()
        dialog.destroy()
