import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class ScrollableBox(Gtk.ScrolledWindow):
    """
    A Gtk.Box embedded inside a Gtk.ScrolledWindow.
    Behaves like a Box but scrollable.
    """

    def __init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=0):
        super().__init__()

        # Scroll policy
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        # Optional: smoother behavior
        self.set_overlay_scrolling(True)

        # The actual container
        self.box = Gtk.Box(orientation=orientation, spacing=spacing)
        self.box.set_homogeneous(False)

        # Important: make box expand horizontally so scroll works correctly
        self.box.set_size_request(-1, -1)

        # Add box into scroll container
        self.add(self.box)

        self.box.show()


    # --- Box-like API wrappers ---

    def pack_start(self, child, expand=True, fill=True, padding=0):
        self.box.pack_start(child, expand, fill, padding)

    def pack_end(self, child, expand=True, fill=True, padding=0):
        self.box.pack_end(child, expand, fill, padding)

    def remove(self, child):
        self.box.remove(child)

    def get_children(self):
        return self.box.get_children()

    def set_spacing(self, spacing):
        self.box.set_spacing(spacing)

    def set_orientation(self, orientation):
        self.box.set_orientation(orientation)