import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject



class FilesList(Gtk.Box):
    __gsignals__ = {
        "selected": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str,),  # that means one argument sent with the signal
        ),
    }
    def __init__(self, files=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        if files is None:
            self.files: list[str] = []
        else:
            self.files = files
        self.viewport = Gtk.Viewport()
        self.add(self.viewport)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.viewport.add(self.box)