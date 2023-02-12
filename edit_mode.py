from helpers import (
    set_app_mode_to,
    get_app_mode,
    set_line_index_to,
    get_line_index,
)
from dictionary_logic import (
    get_list_of_items,
    restore_app_mode,
    add_word_to_vocab_dict,
    delete_vocab_dict_entry,
    update_vocab_dict,
    propagate_items,
    refresh_stats,
    get_filename,
)
from gui_logic import end_gui_mode, clear_entry_field, set_label_to


def get_entry_val(gui, keyword):
    if get_app_mode() == "edit":
        update_dict(gui)
    elif get_app_mode() == "add dict":
        prepare_edit_mode(gui, "Wörterbuch bearbeiten")
    elif get_app_mode() == "quiz":
        gui.decision.set(keyword)


def prepare_entries_for_edit(gui, index, key):
    list_of_elements = get_list_of_items()
    de_key = list_of_elements[index][0]
    val = list_of_elements[index][1::]
    gui.print_s(de_key, field=["entry", 0])
    gui.print_s(",".join(val), field=["entry", 1])
    set_line_index_to(index)


def prepare_edit_mode(gui, key):
    """
    set up app for edit mode
    change textbox to listbox
    change frame 3 for buttons and entry fields
    get list for listbox
    """
    if get_app_mode() != "start":
        return
    listbox_index, quiz_field, edit_field, divider = get_gui_variables(gui)
    change_gui_for_edit_mode(
        gui, divider, id=[quiz_field, edit_field], create=True
    ) if get_app_mode() != "edit" else None
    set_app_mode_to("edit")
    set_label_to(gui, f"File: {get_filename()[0:-4]}", 0)
    update_edit_listbox(gui, listbox_index, key)


def update_edit_listbox(gui, listbox_index, key):
    list_of_items = create_entry_lines([])
    display_list_of_items_in_listbox(gui, listbox_index, list_of_items, key)


def get_gui_variables(gui):
    """get gui variables"""
    funcs = gui.get_funcs()
    gui_dict = gui.get_gui_dict()
    listbox_index = funcs["Wörterbuch bearbeiten"][2]
    quiz_field = gui_dict["entry_fields"][0]["quiz"]
    edit_field = gui_dict["entry_fields"][1]["edit"]
    divider = funcs["dividers"][-1]

    return listbox_index, quiz_field, edit_field, divider


def change_gui_for_edit_mode(gui, divider, id, create):
    """
    set up gui for edit mode
    parameter create: True for entering edit mode
    parameter create: False for leaving edit mode
    """
    gui.switch_to_edit_view(divider, id, create)
    gui.manage_entry_fields(key=id[0], choice="unpack", function="quiz")
    gui.manage_entry_fields(key=id[1], choice="unpack", function="edit")
    gui.pack_entry_field(divider, key=id[0], state=True)
    gui.pack_entry_field(divider, key=id[1], state=True)


def display_list_of_items_in_listbox(gui, listbox_index, listbox_lines, key):
    """display list of items in listbox"""
    first = "Eintrag zum Bearbeiten oder Löschen auswählen"
    second = "oder neue Einträge hinzufügen."
    gui.populate_listbox(
        listbox_lines, key, listbox_index, first_line=first, second_line=second
    )


def create_entry_lines(list_of_items):
    for i, elements in enumerate(get_list_of_items()):
        entry_line = [f"[{i:>3}] {elements[0]}: " + ", ".join(elements[1::])]
        list_of_items.append(entry_line[0])
    return list_of_items


def refresh_listbox(gui):
    """refresh listbox"""
    gui.clear_listbox(1)


def refresh_edit_gui(gui):
    refresh_listbox(gui)
    update_edit_listbox(gui, 1, "Wörterbuch bearbeiten")
    clear_entry_field(gui)


def update_dict(gui):
    entries = gui.get_entry()
    index = get_line_index()
    update_vocab_dict(entries, index)
    propagate_items()
    refresh_edit_gui(gui)


def add_word(gui, keyword):
    """add entry in edit mode"""
    entry = gui.get_entry()
    add_word_to_vocab_dict(entry[0], entry[1])
    propagate_items()
    refresh_edit_gui(gui)


def delete_entry(gui, key=None):
    delete_vocab_dict_entry(gui.get_entry(), get_line_index())
    propagate_items()
    refresh_edit_gui(gui)


def end_edit_mode(gui, key):
    gui.switch_to_edit_view(setting=False, id=[0, 1], divider=False)
    end_gui_mode(gui, get_app_mode, hold_mistakes_list=[], hold_success_stats=[])
    if get_app_mode == "exit":
        print("Exiting is not implemented in edt_mode yet.")
    refresh_stats()
    restore_app_mode(gui)
