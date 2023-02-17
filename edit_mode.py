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
from gui_logic import end_gui_mode


def prepare_edit_mode(gui, key):
    """
    set up app for edit mode
    change textbox to listbox
    change frame 3 for buttons and two entry fields
    get list for listbox
    """
    if get_app_mode() != "loaded":
        return
    set_app_mode_to("start")
    listbox_index, quiz_field, edit_field, divider = get_gui_variables(gui)
    id = [quiz_field, edit_field]
    if get_app_mode() == "edit":
        gui.switch_to_two_entry_fields(divider, id, create=True)
        gui.switch_to_edit_view(divider, id, create=True)
    set_app_mode_to("edit")
    gui.print_s(f"File: {get_filename()[0:-4]}", type=False, field=["label", 0])
    update_edit_listbox(gui, listbox_index, key)


def get_entry_val(gui, keyword: str) -> None:
    """function is called from the button "abschicken"
    Args:
        gui (gui-instance)
        keyword (str): name of the button ("abschicken")
    """
    if get_app_mode() == "edit":
        update_dict(gui)
    elif get_app_mode() == "add_dict":
        gui.decision.set(keyword)
    elif get_app_mode() == "quiz":
        gui.decision.set(keyword)
    elif get_app_mode() == "add_mode":
        gui.decision.set(keyword)


def prepare_entries_for_edit(gui, index, key):
    list_of_elements = get_list_of_items()
    de_key = list_of_elements[index][0]
    val = list_of_elements[index][1::]
    gui.print_s(de_key, field=["entry", 0])
    gui.print_s(",".join(val), field=["entry", 1])
    set_line_index_to(index)


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


def display_list_of_items_in_listbox(gui, listbox_index, listbox_lines, key):
    """display list of items in listbox"""
    first = "Choose entry for editing or deletion"
    second = "or add new entry"
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


def refresh_edit_gui(gui, text: str) -> None:
    refresh_listbox(gui)
    update_edit_listbox(gui, listbox_index=1, text=text)
    gui.clear_entry_field(0)
    gui.clear_entry_field(1)


def update_dict(gui):
    entries = gui.get_entry()
    index = get_line_index()
    if not index:
        return
    update_vocab_dict(entries, index)
    propagate_items()
    refresh_edit_gui(gui)
    set_line_index_to(False)


def add_word(gui, entry):
    """add entry in edit mode"""
    if get_app_mode()=="loaded":
        set_app_mode_to("start")
    if get_app_mode == "edit":
        entry = gui.get_entry()
        refresh_edit_gui(gui, text="Edit dictionary")
    add_word_to_vocab_dict(entry[0], entry[1])
    propagate_items()


def delete_entry(gui, key=None):
    if not get_line_index():
        return
    delete_vocab_dict_entry(gui.get_entry(), get_line_index())
    propagate_items()
    refresh_edit_gui(gui)


def end_edit_mode(gui, key):
    if get_app_mode()=="edit":
        gui.switch_to_edit_view(setting=False, id=[0, 1], divider=False)
    end_gui_mode(gui, get_app_mode, set_app_mode_to, hold_mistakes_list=[], hold_success_stats=[])
    if get_app_mode() == "exit":
        print("Exiting is not implemented in edt_mode yet.")
    elif get_app_mode() == "edit":
        refresh_stats()
        restore_app_mode(gui)
    elif get_app_mode() == "add_mode":
        # TODO: implementing the end of add_mode
        set_app_mode_to("start")
