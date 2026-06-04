import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os

from gui.generic.file_selector import FileSelector


class SelectibleListItem(Gtk.ListBoxRow):
    def __init__(self, text):
        super().__init__()
        self.selected: bool = False
        self.label = Gtk.Label(label=text)
        self.add(self.label)

        self.connect("activate", self.on_activate)
    def on_activate(self, widget):
        print(f"Item '{self.label.get_text()}' activated")


class SelectibleListBox(Gtk.ListBox):
    def __init__(self):
        super().__init__()
        self.data: dict[str, bool] = {}  #  {path: selected}



class FilesCherryPicker(Gtk.Box):
    """
    Reminder:
        - folder_selector.button: clicked
        - folder_selector.entry: activate -> entry.get_text()
    """
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.folders: list[str] = []
        self.files: dict[str, bool] = {}  #  {path: selected}
        self.viewport = Gtk.Viewport()
        self.add(self.viewport)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.viewport.add(self.box)
        self.selector_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.folder_selector = FileSelector(folder_selector=True)
        self.selector_box.pack_start(self.folder_selector, True, True, 0)
        self.box.pack_start(self.selector_box, True, True, 0)
        self.folder_selector.entry.connect("activate", self.on_path_validated)

    def on_path_validated(self, widget):
        path = self.folder_selector.entry.get_text()
        if os.path.exists(path) and path not in self.folders:
            self.folders.append(path)
            self.add_folder(path)
        else:
            self.folder_selector.entry.set_text("")

    def add_folder(self, path: str):
        print((f"Adding folder: {path}"))
        folder_item = SelectibleListItem(path)
        self.box.pack_start(folder_item, False, True, 0)
        self.show_all()

def path_exists(path: str) -> bool:
    import os
    return os.path.exists(path)