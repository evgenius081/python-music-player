import os

import gi

import config
from pygtk.elements.mainWindow.MainWindow import MainWindow

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk


def on_activate(app):
    if not os.path.exists(config.MUSIC_FOLDER_PATH):
        os.makedirs(config.MUSIC_FOLDER_PATH)
    win = MainWindow(app)
    win.present()


application = Gtk.Application(application_id='yahul.GtkApplication')
application.connect('activate', on_activate)

application.run(None)