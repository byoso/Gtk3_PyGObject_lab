#! /usr/bin/env python3

import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject


from comps.small.closable_label import ClosableLabel




NOT_WANTED_DIRS = {"containers", "__pycache__", "venv", "env", ".git"}


def eligible_file(file_name):
    return file_name.endswith(".py") and not file_name.startswith("_") and not file_name.startswith(".")

def eligible_dir(path):
    name = os.path.basename(path)
    return (
        os.path.isdir(path)
        and not name.startswith(".")
        and not name.startswith("_")
        and name not in NOT_WANTED_DIRS
    )

class FolderTreeView(Gtk.Box):
    """
    Emits "selected" + path: str on double-click or Enter on an item.
    """
    __gsignals__ = {
        "selected": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str,),  # that means one argument sent with the signal
        ),
    }
    def __init__(self, folder_path="", short_path_length=120):
        super().__init__()
        self.dir_cache = {}
        self.set_size_request(-1, 300)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.short_path_length = short_path_length


        # 1. THE MODEL: A TreeStore
        # Column 0: String (Displayed name), Column 1: String (Absolute path), Column 2: Icon name
        self.store = Gtk.TreeStore(str, str, str)

        # Fill the model with a test folder (e.g., your user folder)
        root_path = os.path.expanduser(folder_path)
        self.populate_tree(root_path, None)

        # 2. THE VIEW: The TreeView connected to the model
        self.tree_view = Gtk.TreeView(model=self.store)

        # 3. THE RENDERING: Create the display column (sort of title)
        column = Gtk.TreeViewColumn(self.short_path(folder_path))

        # Renderer for the icon
        icon_renderer = Gtk.CellRendererPixbuf()
        column.pack_start(icon_renderer, False)
        column.add_attribute(icon_renderer, "icon-name", 2) # Takes the data from column 2 of the store

        # Renderer for the text
        text_renderer = Gtk.CellRendererText()
        column.pack_start(text_renderer, True)
        column.add_attribute(text_renderer, "text", 0) # Takes the data from column 0 of the store

        self.tree_view.append_column(column)


        # Make the view scrollable
        scroll = Gtk.ScrolledWindow()
        scroll.add(self.tree_view)
        self.pack_start(scroll, True, True, 0)

        # Listen for double-click or Enter on an item
        self.tree_view.connect("row-activated", self.on_row_activated)

        self.show_all()


    def on_row_activated(self, tree_view, path, column):
        """ Callback triggered on double-click """
        model = tree_view.get_model()
        tree_iter = model.get_iter(path)

        # Retrieve the data of the selected row
        absolute_path = model.get_value(tree_iter, 1)

        self.emit("selected", absolute_path)

    def short_path(self, path: str) -> str:
        if len(path) > self.short_path_length:
            return f"...{path[-(self.short_path_length-3):]}"
        return path

    def populate_tree(self, path, parent_iter):
        """Recursive function to populate the TreeStore"""
        try:
            for item in sorted(os.listdir(path)):

                # skip hidden / private files early
                if item.startswith(".") or item.startswith("_"):
                    continue

                full_path = os.path.join(path, item)

                is_dir = os.path.isdir(full_path)

                # -------------------------
                # FILTERING LOGIC
                # -------------------------

                if is_dir:
                    if not eligible_dir(full_path):
                        continue
                else:
                    if not eligible_file(item):
                        continue

                # icon selection
                icon_name = "folder" if is_dir else "document"

                # add node
                current_iter = self.store.append(
                    parent_iter,
                    [item, full_path, icon_name]
                )

                # recurse only into valid directories
                if is_dir:
                    try:
                        if os.getenv("GTK_LAB_DEEP_SCAN") or len(self.store) < 200:
                            self.populate_tree(full_path, current_iter)
                    except PermissionError:
                        pass

        except PermissionError:
            pass
