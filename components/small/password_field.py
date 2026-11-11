import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject


class PasswordField(Gtk.Box):
    def __init__(self, label="", folder_selector=False, placeholder="Enter a password"):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.set_can_focus(True)

        # Entry field
        self.entry = Gtk.Entry(placeholder_text=placeholder)
        self.entry.set_visibility(False)
        self.pack_start(self.entry, True, True, 0)

        # Eye button to show/hide password
        self.eye_button = Gtk.Button()
        self.eye_button.set_image(Gtk.Image.new_from_icon_name("security-high-symbolic", Gtk.IconSize.SMALL_TOOLBAR))
        self.eye_button.connect("clicked", self.toggle_visibility)
        self.pack_end(self.eye_button, False, True, 0)

    def toggle_visibility(self, widget):
        self.entry.set_visibility(not self.entry.get_visibility())
        icon_name = "security-low-symbolic" if self.entry.get_visibility() else "security-high-symbolic"
        self.eye_button.set_image(Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.SMALL_TOOLBAR))
