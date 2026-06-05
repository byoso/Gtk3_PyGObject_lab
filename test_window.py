import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


# from components.medium.files_cherry_picker import FilesCherryPicker

# from components.medium.files_lister import FileLister

from components.big.files_cherry_picker_lister import FilesCherryPickerLister


class TestButton(Gtk.Button):
    def __init__(self):
        super().__init__(label="TEST")
        self.set_size_request(100, 40)


class TestWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Test Window")
        self.set_default_size(400, 300)
        self.connect("destroy", Gtk.main_quit)
        self.working_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        # SET AREA ============================================

        # scrollable area

        # scrolled_window = Gtk.ScrolledWindow()
        # scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        # scrolled_window.add(self.working_box)
        # self.add(scrolled_window)

        # non scrollable area

        self.working_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.working_box)  # Add the non-scrollable box to the main window

        # TEST BUTTON =========================================

        # test button
        self.test_button = TestButton()
        self.test_button.connect("clicked", self.test_button_clicked)  # connecter le signal personnalisé
        self.working_box.pack_start(self.test_button, False, False, 0)

        #  ====================================================
        # TEST ZONE============================================


        self.file_cherry_picker_lister = FilesCherryPickerLister(short_path_length=35)
        self.working_box.pack_start(self.file_cherry_picker_lister, True, True, 0)


        # =====================================================


        self.show_all()

    def test_button_clicked(self, widget):
        print("Test button :")
        files = self.file_cherry_picker_lister.get_allowed_files()
        print("Selected files:", files)
