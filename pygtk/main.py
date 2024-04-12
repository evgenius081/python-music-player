import os

import gi

import config

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk


def on_activate(app):
    win = Gtk.ApplicationWindow(application=app)
    win.set_title("Odtwarzacz")
    if not os.path.exists(config.MUSIC_FOLDER_PATH):
        os.makedirs(config.MUSIC_FOLDER_PATH)
    win.present()


app = Gtk.Application(application_id='com.example.GtkApplication')
app.connect('activate', on_activate)

app.run(None)