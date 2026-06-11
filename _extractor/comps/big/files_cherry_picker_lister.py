import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject


from comps.medium.files_cherry_picker import FilesCherryPicker
from comps.medium.files_lister import FileLister



class FilesCherryPickerLister(Gtk.Box):
    __gsignals__ = {
        "preview": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str, str),  # Emits the absolute path of the file and the class name to preview
        ),
        "extract": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (object,),  # Emits a list of selected file paths for extraction
        ),

    }
    def __init__(self, folder_path=None, short_path_length=120):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.short_path_length = short_path_length


        # files lister
        self.file_lister = FileLister(short_path_length=self.short_path_length)
        self.file_lister.set_size_request(-1, 150)
        self.pack_start(self.file_lister, True, True, 0)
        self.file_lister.connect("preview", self.on_row_preview)

        # files cherry picker
        self.file_cherry_picker = FilesCherryPicker(folder_path=folder_path, short_path_length=self.short_path_length)
        self.pack_start(self.file_cherry_picker, True, True, 0)
        self.file_cherry_picker.set_size_request(-1, 200)
        self.file_cherry_picker.connect("selected", self.file_picked)

        # Extract selected files button
        self.extract_button = Gtk.Button(label="Extract Selected Files")
        self.extract_button.set_size_request(-1, 40)
        self.extract_button.connect("clicked", self.on_extract_clicked)
        self.pack_start(self.extract_button, False, False, 0)

    def on_row_preview(self, widget, file_path, class_name):
        """ Emits a 'preview' signal with the file path and class name when the preview button is clicked """
        self.emit("preview", file_path, class_name)


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

    def on_extract_clicked(self, widget):
        selected_files = self.get_selected_files()
        self.emit("extract", selected_files)