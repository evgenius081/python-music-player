import gi

from pygtk.elements.main.regularMain.musicList.songList import SongList

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")

from gi.repository import Gtk
import config

BOX_SPACING = 15


class RegularMain(Gtk.AspectFrame):
    def __init__(self, media_player):
        super().__init__()
        self.set_halign(Gtk.Align.START)
        self.set_valign(Gtk.Align.START)
        self.set_hexpand(config.WINDOW_WIDTH)
        self.set_vexpand(config.WINDOW_HEIGHT)
        self.margin_bottom = 0
        self.margin_top = config.MENU_BAR_HEIGHT
        self.margin_start = 0
        self.margin_end = 0
        self.__media_player = media_player
        self.__create_UI()

    def __create_UI(self):
        self.__box = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=BOX_SPACING)
        self.set_child(self.__box)

        self.__music_list = SongList(self.__media_player)
        self.__box.append(self.__music_list)

        # self.__controls = Controls(self.__media_player)
        # self.__box.append(self.__controls)

