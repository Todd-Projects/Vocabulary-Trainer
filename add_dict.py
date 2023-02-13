from helpers import (
    get_app_mode,
    set_app_mode_to,
)
from dictionary_logic import (
    create_new_dict,
    check_if_file_is_already_in_folder,
    check_filename_validity,
)


def add_dict(gui, key):
    if get_app_mode() != "start":
        return
    create_add_dict_gui(gui, key)

def create_add_dict_gui(gui, key):
    set_app_mode_to("add_dict")
    gui.set_quizmode(action=True)
    gui.set_label_to("Wörterbuch hinzufügen", 3)
    gui.set_label_to("Gebe einen Namen \nfür das Wörterbuch ein\n[name.csv]:", 1)
    gui.clear_entry_field(0)
    get_new_filename(gui,key)

def get_new_filename(gui,key):
    filename = gui.wait_for_answer()
    gui.clear_entry_field(0)
    if check_if_file_is_already_in_folder(filename):
        gui.print_s(
            "Wörterbuch existiert bereits.\nGebe einen anderen Namen ein.",
            True,
            field=["textbox", 0],
        )
        set_app_mode_to("start")
        add_dict(gui, key)
    elif filename == "":
        set_app_mode_to("start")
        add_dict(gui, key)
    checked_name = check_filename_validity(filename, ".csv")
    if not checked_name:
        set_app_mode_to("start"), add_dict(gui, key)
    set_app_mode_to("start")
    create_new_dict(checked_name, {})
    gui.clear_label(3)
    gui.clear_label(1)
    gui.clear_textbox(0)
    gui.clear_listbox(0)
    gui.clicked(keyword="Wörterbuch bearbeiten",wherefrom = "add_dict")
