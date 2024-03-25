from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMenuBar, QMenu, QWidgetAction
from pyqt6_plugins.examplebutton import QtWidgets


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        with open("./pyqt/elements/menuBar/menuBar.css", "r") as file:
            self.styles = file.read()
        self.setStyleSheet(self.styles)
        self._createActions()
        self._createMenu()

    def _createMenu(self):
        fileMenu = QMenu("&Plik", self)
        fileMenu.setStyleSheet(self.styles)
        fileMenu.addAction(self.addFileAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

        playbackMenu = QMenu("&Odtwarzanie", self)
        playbackMenu.setStyleSheet(self.styles)
        playbackMenu.addAction(self.playAction)
        fileMenu.addSeparator()
        playbackMenu.addAction(self.prevAction)
        playbackMenu.addAction(self.nextAction)
        fileMenu.addSeparator()
        playbackMenu.addAction(self.shuffleAction)
        playbackMenu.addAction(self.repeatListAction)
        fileMenu.addSeparator()
        playbackMenu.addAction(self.quietAction)
        playbackMenu.addAction(self.loudAction)

        aboutMenu = QMenu("&Opis", self)
        aboutMenu.setStyleSheet(self.styles)
        self.addMenu(fileMenu)
        self.addMenu(playbackMenu)
        self.addMenu(aboutMenu)

    def _createActions(self):
        self.addFileAction = QWidgetAction(self)
        
        self.exitAction = QAction(QIcon("pyqt/assets/exit.svg"), "&Wyjdź", self)
        self.stopAction = QAction(QIcon("pyqt/assets/pause.svg"), "&Pauza", self)
        self.playAction = QAction("&Odtwarzaj", self)
        self.prevAction = QAction("&Poprzednia", self)
        self.nextAction = QAction("&Następna", self)
        self.shuffleAction = QAction("&Przetasowanie", self)
        self.stopShuffleAction = QAction("&?", self)
        self.repeatListAction = QAction("&Powtarzaj listę", self)
        self.repeatSingleAction = QAction("&Powtarzaj jedną", self)
        self.stopRepeatAction = QAction("&Nie powtarzaj", self)
        self.quietAction = QAction("&Ciszej", self)
        self.loudAction = QAction("&Głośniej", self)

