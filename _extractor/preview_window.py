import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk



class PreviewWindow(Gtk.Window):

    def __init__(self, file_path, class_name):
        super().__init__(title=f"Preview: {class_name}")


        self.box = Gtk.Box()
        self.box.set_border_width(100)
        self.add(self.box)

    def set_preview_widget(self, widget):
        self.box.pack_start(widget, True, True, 0)