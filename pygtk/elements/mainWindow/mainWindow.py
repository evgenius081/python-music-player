import gi

from pygtk.elements.main.emptyMusicFolderMain.emptyMusicFolderMain import EmptyMusicFolderMain
from pygtk.elements.main.regularMain.regularMain import RegularMain
from pygtk.elements.menuBar.menuBar import MenuBar
from pygtk.mediaPlayer import MediaPlayer

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
        with open("./pygtk/elements/mainWindow/mainWindow.css", "r") as file:
            self.__styles = file.read()
        self.set_name("main_window")
        self.set_title("Odtwarzacz")
        style_provider.load_from_data(self.__styles)
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),
                                                  style_provider,
                                                  Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.props.margin_top = 0
        self.props.margin_bottom = 0
        self.props.margin_end = 0
        self.props.margin_start = 0
        self.__main_widget = None
        self.__empty_music_folder_main = None
        self.__regular_main = None
        self.__media_player = None
        self.__create_UI()

    def __create_UI(self):
        self.__central_box = Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.__central_box.props.margin_end = 0
        self.__central_box.props.margin_start = 0
        self.__central_box.props.margin_bottom = 0
        self.__central_box.props.margin_top = 0
        self.__central_box.set_css_name("central_box")
        self.set_child(self.__central_box)

        self.__create_menu_bar()
        self.__create_main_part()

    def __create_menu_bar(self):
        self.__menu_bar = MenuBar(self)
        self.__menu_bar.connect("songs_added", self.__songs_added)
        self.__central_box.append(self.__menu_bar)

    def __create_main_part(self):
        if is_folder_empty(config.MUSIC_FOLDER_PATH):
            self.__create_empty_main()
        else:
            self.__create_regular_main()

    def __create_empty_main(self):
        self.__empty_music_folder_main = EmptyMusicFolderMain()
        self.__empty_music_folder_main.connect("songs_added", self.__songs_added)
        self.__central_box.append(self.__empty_music_folder_main)
        self.__main_widget = self.__empty_music_folder_main

    def __create_regular_main(self):
        self.__media_player = MediaPlayer()
        self.__menu_bar.set_media_player(self.__media_player)
        self.__regular_main = RegularMain(self.__media_player)
        self.__central_box.append(self.__regular_main)
        self.__main_widget = self.__regular_main

    def __songs_added(self, _, __):
        if not is_folder_empty(config.MUSIC_FOLDER_PATH) and self.__main_widget == self.__empty_music_folder_main:
            self.__central_box.remove(self.__main_widget)
            self.__create_regular_main()
            self.__empty_music_folder_main = None
        else:
            self.__media_player.add_new_songs()
