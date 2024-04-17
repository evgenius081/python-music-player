import config
import gi


gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")

from gi.repository import Gtk, GdkPixbuf

from gi.repository.Gtk import Box, Label, Image, Button, AspectFrame
from gi.repository.Gdk import Cursor

TILE_HEIGHT = 52
TITLE_WIDGET_WIDTH_RATIO = 0.4
ALBUM_WIDGET_WIDTH_RATIO = 0.39
LAYOUT_SPACING = 14
SONG_LAYOUT_MARGIN = 7
LABEL_HEIGHT = 17
DURATION_LABEL_WIDTH = 30
MARGIN_LABEL_WIDTH = 35
TITLE_LAYOUT_SPACING = 9
SONG_COVER_SIZE = 34
TITLE_AUTHOR_LAYOUT_SPACING = 2


class Song(AspectFrame):
    def __init__(self, song, number, media_player):
        super().__init__()
        self.set_name("song")
        self.set_hexpand(config.TILE_WIDTH + LAYOUT_SPACING + config.NUMBER_LABEL_WIDTH)
        self.set_vexpand(TILE_HEIGHT)
        self.set_margin_bottom(0)
        self.set_margin_top(0)
        self.set_margin_start(0)
        self.set_margin_end(0)
        self.__media_player = media_player
        self.__chosen = False
        self.__song = song
        self.__song_number = number
        self.__create_UI()

    def __create_UI(self):
        self.__box = Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=LAYOUT_SPACING)
        self.__box.set_margin_bottom(0)
        self.__box.set_margin_top(0)
        self.__box.set_margin_start(0)
        self.__box.set_margin_end(0)
        self.set_child(self.__box)

        self.__number_label = Label(label=str(self.__song_number))
        self.__number_label.set_name("song_number_label")
        self.__number_label.set_margin_bottom(0)
        self.__number_label.set_margin_top(0)
        self.__number_label.set_margin_start(0)
        self.__number_label.set_margin_end(0)
        self.__number_label.set_hexpand(config.NUMBER_LABEL_WIDTH)
        self.__number_label.set_halign(Gtk.Align.END)
        self.__number_label.set_valign(Gtk.Align.CENTER)
        self.__box.append(self.__number_label)

        self.__song_frame = AspectFrame()
        self.__song_frame.set_name("song_frame")
        self.__song_frame.set_hexpand(config.TILE_WIDTH)
        self.__song_frame.set_vexpand(TILE_HEIGHT)
        self.__song_frame.set_margin_bottom(0)
        self.__song_frame.set_margin_top(0)
        self.__song_frame.set_margin_start(0)
        self.__song_frame.set_margin_end(0)
        self.__box.append(self.__song_frame)

        self.__song_box = Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__song_box.set_halign(Gtk.Align.START)
        self.__song_box.set_valign(Gtk.Align.CENTER)
        self.__song_box.set_margin_bottom(SONG_LAYOUT_MARGIN)
        self.__song_box.set_margin_top(SONG_LAYOUT_MARGIN)
        self.__song_box.set_margin_start(SONG_LAYOUT_MARGIN)
        self.__song_box.set_margin_end(SONG_LAYOUT_MARGIN)
        self.__create__title_layout()
        self.__song_frame.set_child(self.__song_box)

        self.__album_label = Label(label=self.__song.song_album)
        self.__album_label.set_name("song_album_label")
        self.__album_label.set_margin_bottom(0)
        self.__album_label.set_margin_top(0)
        self.__album_label.set_margin_start(0)
        self.__album_label.set_margin_end(0)
        self.__album_label.set_hexpand(int(config.TILE_WIDTH * ALBUM_WIDGET_WIDTH_RATIO))
        self.__album_label.set_vexpand(LABEL_HEIGHT)
        self.__song_box.append(self.__album_label)

        self.__duration_label = Label(label=self.__song.song_duration)
        self.__duration_label.set_name("song_duration_label")
        # self.__duration_label.(0)
        self.__duration_label.set_hexpand(DURATION_LABEL_WIDTH)
        self.__duration_label.set_halign(Gtk.Align.START)
        self.__duration_label.set_valign(Gtk.Align.CENTER)
        self.__duration_label.set_margin_bottom(0)
        self.__duration_label.set_margin_top(0)
        self.__duration_label.set_margin_start(0)
        self.__duration_label.set_margin_end(0)
        self.__song_box.append(self.__duration_label)

        # self.__margin_label = Label(label="")
        # self.__margin_label.set_hexpand(MARGIN_LABEL_WIDTH)
        # self.__song_box.append(self.__margin_label)

        self.__delete_song_button = Button(label="")
        self.__delete_song_button.
        self.__delete_song_button.set_margin_start(MARGIN_LABEL_WIDTH)
        self.__delete_song_button.set_cursor(Cursor.new_from_name("pointer"))
        self.__delete_song_button.set_name("delete_song_button")
        self.__delete_song_button.connect("clicked", self.__remove_song)
        self.__song_box.append(self.__delete_song_button)

    def __create__title_layout(self):
        self.__title_box = Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=TITLE_LAYOUT_SPACING)
        self.__title_box.set_margin_bottom(0)
        self.__title_box.set_margin_top(0)
        self.__title_box.set_margin_start(0)
        self.__title_box.set_margin_end(0)
        self.__title_box.set_halign(Gtk.Align.END)
        self.__title_box.set_valign(Gtk.Align.START)
        self.__song_box.append(self.__title_box)

        self.__cover_image = Image()
        if self.__song.song_cover_image_stream is not None:
            loader = GdkPixbuf.PixbufLoader.new()
            loader.write(self.__song.song_cover_image_stream)
            loader.close()
            pixbuf = loader.get_pixbuf()
        else:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file("common/assets/placeholder.png")
        resized_pixbuf = pixbuf.scale_simple(
            SONG_COVER_SIZE,
            SONG_COVER_SIZE,
            GdkPixbuf.InterpType.BILINEAR
        )
        self.__cover_image.set_from_pixbuf(resized_pixbuf)
        self.__cover_image.set_name("cover_label")
        self.__cover_image.set_hexpand(SONG_COVER_SIZE)
        self.__cover_image.set_vexpand(SONG_COVER_SIZE)
        self.__song_box.append(self.__cover_image)

        self.__play_button = Button(label="")
        self.__play_button.set_image(Image.new_from_file("common/assets/play_light.svg"))
        self.__play_button.set_hexpand(SONG_COVER_SIZE)
        self.__play_button.set_vexpand(SONG_COVER_SIZE)
        self.__play_button.set_name("song_play_button")
        self.__play_button.set_cursor(Cursor.new_from_name("pointer"))
        self.__play_button.set_visible(False)
        self.__play_button.connect("clicked", self.__play_song)
        self.__title_box.append(self.__play_button)

        self.__title_author_widget = QWidget()
        self.__title_author_widget.setFixedSize(int(config.TILE_WIDTH * TITLE_WIDGET_WIDTH_RATIO), SONG_COVER_SIZE)
        self.__title_author_widget.setContentsMargins(0, 0, 0, 0)
        self.__title_layout.addWidget(self.__title_author_widget)

        self.__title_author_layout = Box.new(orientation=)
        self.__title_author_layout.setSpacing(TITLE_AUTHOR_LAYOUT_SPACING)
        self.__title_author_layout.setContentsMargins(0, 0, 0, 0)
        self.__title_author_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__title_author_widget.setLayout(self.__title_author_layout)

        self.__title_label = QLabel(self.__song.song_title if self.__song.song_title != "" else self.__song.file_name)
        self.__title_label.setObjectName("song_title_label")
        self.__title_label.setStyleSheet(self.__styles)
        self.__title_label.setIndent(0)
        self.__title_label.setFixedSize(int(config.TILE_WIDTH * TITLE_WIDGET_WIDTH_RATIO), LABEL_HEIGHT)
        self.__title_label.set_margin_bottom(0)
        self.__title_label.set_margin_top(0)
        self.__title_label.set_margin_start(0)
        self.__title_label.set_margin_end(0)
        self.__title_author_layout.addWidget(self.__title_label)

        if self.__song.song_author != "":
            self.__author_label = Label(label=self.__song.song_author)
            self.__author_label.set_name("song_author_label")
            self.__author_label.set_margin_bottom(0)
            self.__author_label.set_margin_top(0)
            self.__author_label.set_margin_start(0)
            self.__author_label.set_margin_end(0)
            self.__author_label.set_hexpand(int(config.TILE_WIDTH * TITLE_WIDGET_WIDTH_RATIO))
            self.__author_label.set_vexpand(LABEL_HEIGHT)
            self.__title_author_layout.addWidget(self.__author_label)

    # def enterEvent(self, event):
    #     if not self.__chosen:
    #         self.__play_button.setVisible(True)
    #         self.__cover_label.setVisible(False)
    #         super().enterEvent(event)
    #
    # def leaveEvent(self, event):
    #     if not self.__chosen:
    #         self.__play_button.setVisible(False)
    #         self.__cover_label.setVisible(True)
    #         super().leaveEvent(event)

    def __play_song(self):
        if not self.__chosen:
            print(f"play '{self.__song.full_path}'")
            self.__media_player.play_song(self.__song)

    def choose(self):
        self.__song_frame.setStyleSheet(
            """QFrame#song_frame {
                border: 2px solid #76ABAE;
                background-color: #31363F;
                border-radius: 5px;
            }"""
        )
        self.__play_button.setVisible(True)
        self.__play_button.setCursor(Qt.CursorShape.ArrowCursor)
        self.__play_button.setIcon(QIcon("common/assets/play_active.svg"))
        self.__cover_label.setVisible(False)
        self.__delete_song_button.setVisible(False)
        self.__chosen = True

    def unchoose(self):
        self.__song_frame.setStyleSheet(
            """QFrame#song_frame {
                background-color: #31363F;
                border-radius: 5px;
                border: 2px solid #31363F;
            }"""
        )
        self.__play_button.setVisible(False)
        self.__play_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__play_button.setIcon(QIcon("common/assets/play_light.svg"))
        self.__cover_label.setVisible(True)
        self.__delete_song_button.setVisible(True)
        self.__chosen = False

    def __remove_song(self):
        self.__media_player.delete_song(self.__song)

    def set_song_number(self, number):
        self.__song_number = number
        self.__number_label.setText(str(number))

