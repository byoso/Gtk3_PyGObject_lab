import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from gui.generic.file_selector import FileSelector
from gui.custom.folder_tree_view import FolderTreeView


class FilesCherryPicker(Gtk.Box):
    """
    Reminder:
        - folder_selector.button: clicked
        - folder_selector.entry: activate -> entry.get_text()
    """
    __gsignals__ = {
        "selected": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str,),  # that means one argument sent with the signal
        ),
    }
    def __init__(self, folders=None, short_path_length=120):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        if folders is None:
            self.folders: list[str] = []
        else:
            self.folders = folders
        self.short_path_length = short_path_length
        self.viewport = Gtk.Viewport()
        self.add(self.viewport)
        self.scrollable_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.viewport.add(self.scrollable_box)
        self.selector_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.folder_selector = FileSelector(folder_selector=True, placeholder="Add a folder")
        self.selector_box.pack_start(self.folder_selector, True, True, 0)
        self.scrollable_box.pack_start(self.selector_box, True, True, 0)
        self.folder_selector.connect("selected", self.add_folder)
        self.box_folder_containers = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.scrollable_box.pack_start(self.box_folder_containers, True, True, 0)

        self.build_folder_containers()

    def add_folder(self, widget, path: str):
        self.folder_selector.clear()
        if path in self.folders:
            return
        self.folders.append(path)
        self.build_folder_containers()

    def build_folder_containers(self):
        for child in self.box_folder_containers.get_children():
            self.box_folder_containers.remove(child)  # Clear existing folder containers
        for folder_path in self.folders:
            folder_tree_view = FolderTreeView(folder=folder_path, short_path_length=self.short_path_length)
            folder_tree_view.connect("selected", self.on_path_selected)
            self.box_folder_containers.pack_start(folder_tree_view, True, True, 0)

    def on_path_selected(self, widget, path: str):
        print(path)
        self.emit("selected", path)

    def get_selection(self) -> list[str]:
        return self.selection

    def clear_selection(self):
        self.selection.clear()