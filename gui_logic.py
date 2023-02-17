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
        f" What is: \n'{vocab_dict.get_prompt(index)}' \nauf in English? ",
        True,
        field=["label", 1],
    )

def end_gui_mode(
    gui, get_app_mode, set_app_mode_to, hold_mistakes_list, hold_success_stats, filename="", img=""
):
    gui.print_s("Quiz",type=False,field=["label",3])
    gui.clear_listbox(0)
    if get_app_mode() == "quiz":
        gui.print_s("You finished this quiz!.", False, field=["textbox", 0])
        gui.print_s(hold_mistakes_list.get_state()[0], True, field=["textbox", 0])
        gui.print_s(hold_mistakes_list.get_state()[1], True, field=["textbox", 0])
        gui.print_s(hold_success_stats.get_state()[0], True, field=["textbox", 0])
        gui.print_s(hold_success_stats.get_state()[1], True, field=["textbox", 0])
        gui.print_s("\n", True, field=["textbox", 0])
        gui.set_image_to_textbox(textbox_index=0, badge=img)
        gui.set_quizmode(action=False)
    elif get_app_mode() == "edit":
        gui.print_s("Editing finished.", False, field=["textbox", 0])
    elif get_app_mode() == "add_mode":
        gui.print_s("Successfully added vocabulary items.", False, field=["textbox", 0])
        gui.set_quizmode(action=False)
        set_app_mode_to("start")
