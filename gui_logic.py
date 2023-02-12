def clear_entry_field(gui):
    gui.clear_entry_field(0)
    gui.clear_entry_field(1)


def display_all_items_in_editbox(gui, key, index, list_of_items):
    """
    function: get_list_of_items() returns a list of items in dictionary from FileHandler
    format: [[de, [en1, en2, en3]][de, [en1, en2, en3]]]
    params: gui (class): gui object
    params: key (str): takes the name of the button pressed (Wörterbuch bearbeiten)
    params: index (int): index of listbox in self.holder[index]
    """
    gui.clear_listbox(index)
    gui.populate_listbox(
        list_of_items,
        key,
        listbox_index=index,
        first_line="Choose entry from list",
        second_line="-----click here for new entry-------",
    )


def prepare_gui_for_quiz(gui):
    gui.set_quizmode(action=True)
    quiztype, difficulty = gui.get_quiztype()
    return quiztype, difficulty


def display_question(gui, index, vocab_dict):
    gui.print_s(
        f" Wie heißt: \n'{vocab_dict.get_prompt(index)}' \nauf Englisch? ",
        True,
        field=["label", 1],
    )


def print_result_to_gui(gui, text, boolean, field):
    gui.print_s(text, boolean, field)


def end_gui_mode(
    gui, get_app_mode, hold_mistakes_list, hold_success_stats, filename="", img=""
):
    gui.set_label_to("Quiz", 3)
    gui.clear_listbox(0)
    if get_app_mode() == "quiz":
        gui.print_s("Quiz beendet.", False, field=["textbox", 0])
        gui.print_s(hold_mistakes_list.get_state()[0], True, field=["textbox", 0])
        gui.print_s(hold_mistakes_list.get_state()[1], True, field=["textbox", 0])
        gui.print_s(hold_success_stats.get_state()[0], True, field=["textbox", 0])
        gui.print_s(hold_success_stats.get_state()[1], True, field=["textbox", 0])
        gui.print_s("\n", True, field=["textbox", 0])
        # TODO: create five gif files that represent the success of the student
        # following lines are commented out as the images have yet to be created
        #gui.set_image_to_textbox(textbox_index=0, badge=img)
        #gui.set_quizmode(action=False)
    elif get_app_mode() == "edit":
        gui.print_s("Bearbeitung beendet.", False, field=["textbox", 0])
    elif get_app_mode() == "add":
        gui.print_s("Vokabeln hinzugefügt.", False, field=["textbox", 0])
        gui.set_quizmode(action=False)


def set_label_to(gui, string, frame):
    gui.set_label_to(string, frame)
