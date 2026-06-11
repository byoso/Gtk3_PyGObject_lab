#! /usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

import importlib
import os
import sys
from pathlib import Path

from preview_window import PreviewWindow
from files_extractor import extract_files
from comps.big.files_cherry_picker_lister import FilesCherryPickerLister


PROJECT_ROOT = Path("/home/byoso/Misc/Github_Projects/gtk3_lab")


def load_class_from_file(file_path, class_name, project_root):
    print(PROJECT_ROOT)
    project_root = Path(PROJECT_ROOT).resolve()

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

        print("sys.path[0] =", sys.path[0])

    rel_path = Path(file_path).resolve().relative_to(project_root)

    module_name = ".".join(rel_path.with_suffix("").parts)
    print("module_name =", module_name)

    module = importlib.import_module(module_name)
    module = importlib.reload(module)

    return getattr(module, class_name)


class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Extractor !")
        self.set_default_size(600, 600)
        self.connect("destroy", Gtk.main_quit)
        # self.set_position(Gtk.WindowPosition.CENTER)

        # HeaderBar
        header = Gtk.HeaderBar()
        header.set_title("Extractor !")
        header.set_show_close_button(True)
        # Replace the default titlebar with our custom HeaderBar
        self.set_titlebar(header)

        # open "build" button
        open_button = Gtk.Button()
        buton_icon = Gtk.Image.new_from_icon_name("folder-open-symbolic", Gtk.IconSize.BUTTON)
        open_button.set_image(buton_icon)
        open_button.connect("clicked", self.on_open_build_folder)
        header.pack_end(open_button)

        # Pixbuf icon
        icon_path = PROJECT_ROOT / "_extractor" / "icon.png"
        if icon_path.exists():
            self.set_icon_from_file(str(icon_path))

        # Create the main layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_box)

        # Create and add the FilesCherryPickerLister component
        self.cherry_picker_lister = FilesCherryPickerLister(folder_path="components", short_path_length=35)
        self.cherry_picker_lister.connect("preview", self.on_preview)
        self.cherry_picker_lister.connect("extract", self.on_extract)
        main_box.pack_start(self.cherry_picker_lister, True, True, 0)

        self.show_all()

    def on_preview(self, widget, file_path, class_name):
        print(f"Preview requested for file: {file_path}, class: {class_name}")

        print(f"Project root: {PROJECT_ROOT}")
        try:
            widget_class = load_class_from_file(file_path, class_name, PROJECT_ROOT)

            component = widget_class()

            preview_win = PreviewWindow(file_path, class_name)
            preview_win.set_preview_widget(component)
            preview_win.show_all()

        except Exception as e:
            print(f"Preview error: {e}")

    def on_extract(self, widget, selected_files):
        if not selected_files:
            return
        self.cherry_picker_lister.extract_button.set_label("Extracting...")
        extract_files(selected_files)
        self.cherry_picker_lister.extract_button.set_label("Done ✅")

        # wait 1 second asynchronously before resetting the button label
        GLib.timeout_add(1000, self.reset_extract_button)

    def reset_extract_button(self):
        self.cherry_picker_lister.extract_button.set_label("Extract Selected Files")

    def on_open_build_folder(self, widget):
        build_folder = PROJECT_ROOT / "build"
        if not build_folder.exists():
            print(f"Build folder does not exist: {build_folder}")
            return

        # Open the build folder in the file manager
        import subprocess
        subprocess.run(["xdg-open", str(build_folder)])


def main():
    win = MainWindow()
    win.show_all()
    Gtk.main()





if __name__ == "__main__":
    main()