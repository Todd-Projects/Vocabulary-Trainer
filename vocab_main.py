"""contains main logic for the vocabulary trainer"""


from helpers import get_filelist, set_app_mode_to, get_app_mode
from file_handling import FileHandling

# import all functions from dictionary_logic.py that are used in vocab_main.py
from dictionary_logic import (
    collect_data,
    handle_loading_dict,
)
from init_app import *
import sys


def choose_dictionary(gui, key):
    """
    sets app mode to "start" and populates listbox with filenames
    """
    if get_app_mode() != "start":
        return
    set_app_mode_to("start")
    clear_listbox(gui, 0)
    gui.populate_listbox(
        get_filelist(),
        key,
        listbox_index=0,
        first_line="Choose a dictionary",
        second_line="------------------------------------",
    )


def clear_listbox(gui, index, text=""):
    """
    clears the listbox at the given index
    """
    gui.clear_listbox(index, text)


def pass_line_index_to_loading(gui, index):
    """
    gets the content of a line in the listbox and passes it to the loading function
    """
    filename = get_filelist()[index]
    clear_listbox(gui, 0, f"File '{filename}' loaded.")
    handle_loading_dict(filename, index)


def exit_app():
    collect_data()
    sys.exit()
