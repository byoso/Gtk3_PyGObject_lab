import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk



class FileSelector(Gtk.Box):
    """
    Reminder:
        - button: clicked
        - entry: activate, change -> entry.get_text()
    """
    def __init__(self, label="", folder_selector=False, placeholder="Enter a path"):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.set_can_focus(True)
        self.folder_selector = folder_selector
        self.entry = Gtk.Entry(placeholder_text=placeholder)
        self.entry.connect("activate", self.on_entry_changed)
        self.pack_start(self.entry, True, True, 0)

        # Create a button to open the folder chooser dialog
        button = Gtk.Button()
        if self.folder_selector:
            icon = Gtk.Image.new_from_icon_name("folder", Gtk.IconSize.BUTTON)
        else:
            icon = Gtk.Image.new_from_icon_name("document-open", Gtk.IconSize.BUTTON)
        button.add(icon)

        button.connect("clicked", self.on_button_clicked)

        self.pack_start(button, False, True, 0)

    def on_entry_changed(self, widget):
        self.grab_focus()

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
            chemin = dialog.get_filename()
            self.entry.set_text(chemin)
        else:
            chemin = ""
        self.entry.activate()
        dialog.destroy()
