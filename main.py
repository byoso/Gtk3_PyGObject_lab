#! /usr/bin/env python3

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk



from test_window import TestWindow



if __name__ == "__main__":
    window = TestWindow()
    Gtk.main()