"""contains main logic for the vocabulary trainer"""

from init_app import file_list
from helpers import get_filelist, set_app_mode_to, get_app_mode
from file_handling import FileHandling

# import all functions from dictionary_logic.py that are used in vocab_main.py
from dictionary_logic import (
    collect_data,
    handle_loading_dict,
    check_if_file_is_already_in_folder,
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
    gui.clear_listbox(0)
    file_list.set_state([x for x in get_filelist()])
    gui.populate_listbox(
        file_list.get_state(),
        key,
        listbox_index=0,
        first_line="Choose a dictionary",
        second_line="------------------------------------",
    )


def pass_line_index_to_loading(index):
    """
    gets the content of a line in the listbox and passes it to the loading function
    """
    filename = file_list.get_state()[index]
    if check_if_file_is_already_in_folder(filename, index):
        return
    handle_loading_dict(filename, index)


def exit_app():
    collect_data()
    sys.exit()
