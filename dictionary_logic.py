from vocabulary_app import VocabManipulation
from file_handling import FileHandling, csv
from file_handling import MistakesDict
from init_app import (
    stats_holder,
    delete_all_variables,
    dict_obj,
    file_obj,
)
from helpers import (
    get_todays_date,
    get_filelist,
    set_app_mode_to,
    is_user_stats,
)


def collect_data():
    if not is_vocab_dict():
        return
    stats = stats_holder.get_state()
    if not stats:
        return
    date = get_todays_date()
    stats.insert(0, date)
    save_stats(stats)


def set_stats_holder():
    stats_holder.set_state(get_vocab_object().collect_stats())


def save_stats(stats):
    if not is_user_stats():
        create_stats_file()
    with open("user_stats.stats", mode="a", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(stats)
    file.close()


def create_stats_file():
    with open("user_stats.stats", mode="w", newline="\n", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            [
                "day_of_session",
                "number_of_words_per_session",
                "correct_per_session",
                "mistakes_per_session",
                "wrong_words_per_session",
                "percentages_of_correct_answers",
            ]
        )
    file.close()


def create_new_dict(filename, dictionary):
    """
    handle_newly_created_dict gets information about the newly created dictionary and updates:
    - the list of dictionaries (dictionaries)
    - the list of vocabularies (vocab_dict)
    operates from main menu > Wörterbuch anlegen
    Args:
        vocab_dict (list): _description_
        dict_choice (list): _description_
        dictionary (list): _description_
    """
    delete_instances()
    create_new_vocab_dict(dictionary)
    create_new_file_object()
    set_filename_to_file_object(filename)
    set_outside_dictionary_to_file_instance(dictionary)
    save_file_object_instance()


def handle_loading_dict(filename, index=None):  # index is currently not used
    """handles loading a dictionary from file"""
    # deletes all variables that were created in init_app.py
    # this made to avoid errors when creating a new dictionary
    delete_all_variables()
    create_new_file_object()
    set_filename_to_file_object(filename)
    load_dictionary()
    create_new_vocab_dict(get_dictionary())
    set_app_mode_to("loaded")


def save_mistakes_filehandler(m_dict):
    """creates a filehandler instance for the mistakes dictionary"""
    delete_instances()
    num = check_for_mistakes_file()
    num += 1 if num else 1
    if num < 10:
        num = f"0{num}"
    mistakes_file = MistakesDict(f"{get_todays_date().replace('.','-')}-{str(num)}-mistakes.csv",m_dict)
    mistakes_file.save_mistakes_filehandler()
    mistakes_file.delete_self()
    del mistakes_file


def check_for_mistakes_file():
    """checks if there is already a mistakes file for today"""
    nums = []
    for file in get_filelist():
        if file.startswith(get_todays_date().replace(".", "-")) and file.endswith(
            "-mistakes.csv"
        ):
            nums.append(int(file[11:13:]))
    return max(nums) if nums else False


def save_new_words():
    set_dictionary_to_file_instance()
    save_file_object_instance()


def delete_instances():
    """
    TODO: check if this works
    """
    dict_obj.get_state().delete_self()
    dict_obj.delete_instance()
    file_obj.get_state().delete_self()
    file_obj.delete_instance()


def add_word_to_vocab_dict(first_lang, second_lang):
    dict_obj.get_state().add_dict_items(first_lang, second_lang)


def create_new_vocab_dict(dictionary):
    dict_obj.set_state(VocabManipulation(dictionary))


def create_new_file_object():
    file_obj.set_state(FileHandling())


def set_filename_to_file_object(filename):
    file_obj.get_state().set_filename(filename)


def get_filename():
    return file_obj.get_state().get_filename()


def set_dictionary_to_file_instance():
    file_obj.get_state().set_dictionary(dict_obj.get_state().get_dict())


def set_outside_dictionary_to_file_instance(dictionary):
    file_obj.get_state().set_dictionary(dictionary)


def save_file_object_instance():
    file_obj.get_state().save_file()


def load_dictionary():
    file_obj.get_state().load_file()


def get_dictionary():
    return file_obj.get_state().get_dictionary()


def get_vocab_object():
    # TODO: is this syntax correct?
    return dict_obj.get_state()


def get_list_of_items():
    return file_obj.get_state().get_list_of_items()


def is_vocab_dict():
    return False if dict_obj.get_state() == "" else True


def update_vocab_dict(entries, index):
    first_l = entries[0]
    second_l = entries[1]
    dict_obj.get_state().update_entry(first_l, second_l, index)


def delete_vocab_dict_entry(entries, index):
    first_l = entries[0]
    second_l = entries[1]
    dict_obj.get_state().delete_entry(first_l, second_l, index)


def propagate_items():
    set_dictionary_to_file_instance()
    save_file_object_instance()


def get_mistakes():
    return dict_obj.get_state().get_mistakes()


def get_success_stats():
    return dict_obj.get_state().get_success_stats()


def restore_app_mode(gui):
    set_app_mode_to("start")
    set_outside_dictionary_to_file_instance(dict_obj.get_state().get_dict())
    save_file_object_instance()
    delete_instances()
    gui.revert_to_start()


def refresh_stats():
    set_stats_holder()
