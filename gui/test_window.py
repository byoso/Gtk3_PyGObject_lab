import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from gui.generic.file_selector import FileSelector
from gui.custom.files_cherry_picker import FilesCherryPicker


class TestButton(Gtk.Button):
    def __init__(self):
        super().__init__(label="Test Button")


class TestWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Test Window")
        self.set_default_size(400, 300)
        self.connect("destroy", Gtk.main_quit)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        # scrollable area
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.box)
        self.add(scrolled_window)

        # test button
        self.test_button = TestButton()
        self.test_button.connect("clicked", self.test_button_clicked)  # connecter le signal personnalisé
        self.box.pack_start(self.test_button, True, True, 0)

        #  ========================================

        self.file_cherry_picker = FilesCherryPicker()
        self.box.pack_start(self.file_cherry_picker, True, True, 0)



        # =========================================



        self.show_all()
    def on_path_selected(self, widget):
        path = self.file_cherry_picker.folder_selector.entry.get_text()
        print("Selected path:", path)

    def test_button_clicked(self, widget):
        print("Test button :")
        path = self.file_cherry_picker.folder_selector.entry.get_text()
        print("Selected path :", path)
