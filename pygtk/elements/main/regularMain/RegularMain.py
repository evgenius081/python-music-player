import gi

from pygtk.elements.main.regularMain.controls.Controls import Controls
from pygtk.elements.main.regularMain.musicList.SongList import SongList

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
        self.set_size_request(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.margin_bottom = 0
        self.margin_top = config.MENU_BAR_HEIGHT
        self.margin_start = 0
        self.margin_end = 0
        self._media_player = media_player
        self._create_UI()

    def _create_UI(self):
        self._box = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=BOX_SPACING)
        self._box.set_halign(Gtk.Align.CENTER)
        self._box.set_valign(Gtk.Align.START)
        self.set_child(self._box)

        self._music_list = SongList(self._media_player)
        self._box.append(self._music_list)

        self._controls = Controls(self._media_player)
        self._box.append(self._controls)

