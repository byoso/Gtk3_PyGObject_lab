import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


from components.medium.files_cherry_picker import FilesCherryPicker
from components.medium.files_lister import FileLister
from components.small.checkable_label import CheckableLabel



class FilesCherryPickerLister(Gtk.Box):
    def __init__(self, short_path_length=120):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.short_path_length = short_path_length

        self.state = False  # for checkable label

        # checkable button
        self.checkable_label = CheckableLabel(text="Send")
        self.pack_start(self.checkable_label, False, False, 0)
        self.checkable_label.connect("toggled", self.on_check_toggled)

        # files lister
        self.file_lister = FileLister(short_path_length=35)
        self.file_lister.set_size_request(-1, 150)
        self.pack_start(self.file_lister, True, True, 0)

        # files cherry picker
        self.file_cherry_picker = FilesCherryPicker(short_path_length=35)
        self.pack_start(self.file_cherry_picker, True, True, 0)
        self.file_cherry_picker.set_size_request(-1, 200)
        self.file_cherry_picker.connect("selected", self.file_picked)

    def on_check_toggled(self, widget):
        self.state = self.checkable_label.check_button.get_active()


    def file_picked(self, widget, path: str):
        self.file_lister.add_file(path)


    def short_path(self, path: str) -> str:
        if len(path) <= self.short_path_length:
            return path
        else:
            return "..." + path[-(self.short_path_length-3):]

    def get_selected_files(self) -> list[str]:
        return self.file_lister.get_selected_files()

    def get_allowed_files(self) -> list[str]:
        if self.state:
            return self.file_lister.get_selected_files()
        else:
            return []

    @classmethod
    def preview_instance(cls):
        instance = cls(short_path_length=35)
        return instance