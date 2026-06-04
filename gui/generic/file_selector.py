import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject


import os


class FileSelectorButton(Gtk.Button):
    """
    Emits "selected" signal when a path is selected using the file chooser dialog.
    """
    __gsignals__ = {
        "selected": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str,),  # that means one argument sent with the signal
        ),
    }
    def __init__(self, folder_selector=False):
        super().__init__()
        self.folder_selector = folder_selector
        if self.folder_selector:
            icon = Gtk.Image.new_from_icon_name("folder", Gtk.IconSize.BUTTON)
        else:
            icon = Gtk.Image.new_from_icon_name("document-open", Gtk.IconSize.BUTTON)
        self.add(icon)
        self.connect("clicked", self.on_button_clicked)


    def on_button_clicked(self, widget):
        if self.folder_selector:
            dialog = Gtk.FileChooserDialog(title="Please choose a folder",
                                            action=Gtk.FileChooserAction.SELECT_FOLDER)
        else:
            dialog = Gtk.FileChooserDialog(title="Please choose a file",
                                            action=Gtk.FileChooserAction.OPEN)

        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        if dialog.run() == Gtk.ResponseType.OK:
            path = dialog.get_filename()
        else:
            path = ""
        self.emit("selected", path)
        dialog.destroy()


class FileSelector(Gtk.Box):
    """
    Emits "selected" signal when a path is selected, either by entering it in the entry or by using the file chooser dialog.
    """
    __gsignals__ = {
        "selected": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str,),  # that means one argument sent with the signal
        ),
    }
    def __init__(self, label="", folder_selector=False, placeholder="Enter a path"):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.set_can_focus(True)
        self.folder_selector = folder_selector
        self.entry = Gtk.Entry(placeholder_text=placeholder)
        self.entry.connect("activate", self.on_entry_entered)
        self.pack_start(self.entry, True, True, 0)

        # Create a button to open the folder chooser dialog
        button = FileSelectorButton(folder_selector=folder_selector)
        button.connect("selected", self.on_button_clicked)
        self.pack_start(button, False, True, 0)

    def on_button_clicked(self, widget, path=None):
        self.entry.set_text(path if path else "")
        self.path_validation()

    def on_entry_entered(self, widget):
        self.grab_focus()
        self.path_validation()

    def path_validation(self):
        path = self.entry.get_text()
        if not os.path.exists(path):
            self.entry.set_text("")
            return
        self.emit("selected", path)

    def clear(self):
        self.entry.set_text("")
