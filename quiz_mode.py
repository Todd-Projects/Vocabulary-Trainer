from dictionary_logic import (
    is_vocab_dict,
    get_vocab_object,
    collect_data,
    refresh_stats,
    restore_app_mode,
    get_mistakes,
    save_mistakes_filehandler,
    get_success_stats,
)
from helpers import (
    get_app_mode,
    set_app_mode_to,
)
from gui_logic import (
    prepare_gui_for_quiz,
    print_result_to_gui,
    end_gui_mode,
    display_question,
)
from vocab_main import choose_dictionary
from init_app import hold_mistakes_list, hold_success_stats

from PIL import ImageTk, Image
import random
import sys


def get_quiz_type(gui, key):
    if not is_vocab_dict() or get_app_mode() != "start":
        return
    quiztype, difficulty = prepare_gui_for_quiz(gui)
    set_app_mode_to("quiz")
    start_training(gui, quiztype, get_vocab_object(), difficulty)


def start_training(gui, quiztype, vocab_dict, difficulty):
    """sets variables for learning to default values"""
    vocab_dict.initialize_session()
    loop_quiz(
        gui, initialize_loop_list(gui, quiztype, vocab_dict), vocab_dict, difficulty
    )


def initialize_loop_list(gui, quiztype, vocab_dict):
    """creates list for loop and loops through items"""
    r_list = [x for x in range(0, vocab_dict.get_dict_length())]
    random.shuffle(r_list) if quiztype == "z" else None
    gui.print_s(
        f"Quizmodus aktiviert. \nLerne {len(r_list)} Vokabeln", True, field=["label", 2]
    )
    return r_list


def check_answer(gui, index, answer, vocab_dict, difficulty):
    if vocab_dict.is_correct(index, answer, difficulty):
        print_result_to_gui(
            gui, text=f"'{answer}' ist richtig! ", boolean=True, field=["textbox", 0]
        )
    else:
        print_result_to_gui(
            gui,
            text=f"'{answer}' war leider falsch.",
            boolean=True,
            field=["textbox", 0],
        )
    print_result_to_gui(
        gui,
        text=f"{vocab_dict.get_score()} richtig von {vocab_dict.get_dict_length()}.",
        boolean=True,
        field=["label", 2],
    )


def loop_quiz(gui, r_list, vocab_dict, difficulty):
    """
    loops through items of r_list
    params: r_list (list): random or in order, list of integers
    """
    for index in r_list:
        display_question(gui, index, vocab_dict)
        answer = gui.wait_for_answer()
        gui.clear_entry_field(0)
        check_answer(gui, index, answer, vocab_dict, difficulty)
        if get_app_mode() == "exit":
            collect_data(), sys.exit()
    hold_success_stats, hold_mistakes_list = manage_mistakes()
    choose_dictionary(gui, "Wörterbuch wählen")
    #filename, img = create_badge(gui, vocab_dict)
    filename, img = "",""
    end_gui_mode(
        gui, get_app_mode, hold_mistakes_list, hold_success_stats, filename, img
    )
    refresh_stats()
    restore_app_mode(gui)
    set_app_mode_to("start")


def manage_mistakes():
    answerstring, m_dict, wrong_items = get_mistakes()
    if answerstring:
        hold_mistakes_list.set_state([answerstring, wrong_items])
        save_mistakes_filehandler(m_dict)
    else:
        hold_mistakes_list.set_state(["Perfekt!", "Keine Fehler gemacht!"])
    hold_success_stats.set_state(get_success_stats())
    return hold_success_stats, hold_mistakes_list


def create_badge(gui, vocab_dict):
    """ unused for now as I do not yet have the images """
    percent = vocab_dict.get_percents(string=False)
    filename = f"images/{grading_dict(percent)}"
    # get the image "firstplace.png" from the folder "/images"
    img = Image.open(filename)
    img = img.resize((200, 200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    return filename, img


def grading_dict(percent):
    grading_dict = {
        90: "firstplace.gif",
        80: "secondplace.gif",
        65: "thirdplace.gif",
        50: "fourthplace.gif",
        0: "noplace.gif",
    }
    grades = list(grading_dict.keys())
    for i in grades:
        if percent >= i:
            return grading_dict[i]
