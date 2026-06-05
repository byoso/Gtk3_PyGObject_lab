import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject


class ClosableLabel(Gtk.Box):
    __gsignals__ = {
        "closed": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (),  # that means no argument sent with the signal
        ),
    }
    def __init__(self, text):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.label = Gtk.Label(label=text)
        self.pack_start(self.label, True, True, 0)
        self.close_button = Gtk.Button(label="X")
        self.close_button.set_size_request(20, 20)
        self.pack_start(self.close_button, False, False, 0)
        self.close_button.connect("clicked", self.on_close_clicked)

    def on_close_clicked(self, widget):
        self.emit("closed")