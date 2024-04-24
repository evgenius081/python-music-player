import gi

from pygtk.elements.main.emptyMusicFolderMain.EmptyMusicFolderMain import EmptyMusicFolderMain
from pygtk.elements.main.regularMain.RegularMain import RegularMain
from pygtk.elements.menuBar.MenuBar import MenuBar
from pygtk.MediaPlayer import MediaPlayer

gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')

from gi.repository import Gtk, Gdk
from gi.repository.Gtk import ApplicationWindow, CssProvider, Box

from common.utils.files import *


class MainWindow(ApplicationWindow):
    def __init__(self, application=None):
        super().__init__()
        self.set_application(application)
        self.set_default_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        style_provider = CssProvider()
        with open("./pygtk/elements/mainWindow/MainWindow.css", "r") as file:
            self._styles = file.read()
        self.set_name("main_window")
        self.set_title("Odtwarzacz")
        style_provider.load_from_data(self._styles)
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),
                                                  style_provider,
                                                  Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.props.margin_top = 0
        self.props.margin_bottom = 0
        self.props.margin_end = 0
        self.props.margin_start = 0
        self._main_widget = None
        self._empty_music_folder_main = None
        self._regular_main = None
        self._media_player = None
        self._create_UI()

    def _create_UI(self):
        self._central_box = Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self._central_box.props.margin_end = 0
        self._central_box.props.margin_start = 0
        self._central_box.props.margin_bottom = 0
        self._central_box.props.margin_top = 0
        self._central_box.set_css_name("central_box")
        self.set_child(self._central_box)

        self._create_menu_bar()
        self._create_main_part()

    def _create_menu_bar(self):
        self._menu_bar = MenuBar(self)
        self._menu_bar.connect("songs_added", self._songs_added)
        self._central_box.append(self._menu_bar)

    def _create_main_part(self):
        if is_folder_empty(config.MUSIC_FOLDER_PATH):
            self._create_empty_main()
        else:
            self._create_regular_main()

    def _create_empty_main(self):
        self._empty_music_folder_main = EmptyMusicFolderMain()
        self._empty_music_folder_main.connect("songs_added", self._songs_added)
        self._central_box.append(self._empty_music_folder_main)
        self._main_widget = self._empty_music_folder_main

    def _create_regular_main(self):
        self._media_player = MediaPlayer()
        self._menu_bar.set_media_player(self._media_player)
        self._regular_main = RegularMain(self._media_player)
        self._central_box.append(self._regular_main)
        self._main_widget = self._regular_main

    def _songs_added(self, _, __):
        if not is_folder_empty(config.MUSIC_FOLDER_PATH) and self._main_widget == self._empty_music_folder_main:
            self._central_box.remove(self._main_widget)
            self._create_regular_main()
            self._empty_music_folder_main = None
        else:
            self._media_player.add_new_songs()
