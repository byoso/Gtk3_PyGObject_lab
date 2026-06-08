import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GObject, Gtk

from comps.medium.folder_tree_view import FolderTreeView


class FilesCherryPicker(Gtk.Box):

    __gsignals__ = {
        "selected": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str,),  # that means one argument sent with the signal
        ),
    }

    def __init__(self, folder_path=None, short_path_length=120):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.short_path_length = short_path_length


        # 1. Use a Gtk.ScrolledWindow as the scrolling foundation
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC
        )
        self.pack_start(self.scrolled_window, True, True, 0)

        # 2. Box container inside the ScrolledWindow to hold the multiple tree views
        self.box_folder_containers = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=10
        )

        # In GTK 3, containers without native scrolling capabilities (like Gtk.Box)
        # must be added to a ScrolledWindow using a Viewport placeholder container.
        # .add() does this automatically for us behind the scenes.
        self.scrolled_window.add(self.box_folder_containers)
        if folder_path is not None:
            self.add_folder(None, folder_path)

        self.show_all()

    def add_folder(self, widget, folder_path: str):
        # Create and connect the new custom tree view component
        folder_tree_view = FolderTreeView(
            folder_path=folder_path, short_path_length=self.short_path_length
        )
        folder_tree_view.connect("selected", self.on_path_selected)
        folder_tree_view.set_margin_left(15)
        folder_tree_view.set_margin_right(25)

        # Dynamically pack it into our scrolling box layout
        self.box_folder_containers.pack_start(folder_tree_view, True, True, 0)
        self.show_all()

    def on_path_selected(self, widget, path: str):
        self.emit("selected", path)
