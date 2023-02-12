from vocabulary_app import VocabManipulation
from file_handling import FileHandling, csv
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
)


def check_if_file_is_already_in_folder(file, index=None):
    if file in FileHandling.keep_count:
        return True
    return False


def check_filename_validity(filename=None, ending=None):
    if filename is None:
        return False
    if filename.endswith(ending) and filename.count(".") == 1:
        return filename
    else:
        filename = f"{filename}{ending}"
    return filename


def set_stats_holder():
    stats_holder.set_state(get_vocab_object().collect_stats())


def get_stats_holder():
    return stats_holder.get_state()


def save_stats(stats):
    if not check_filename_validity("user_stats.stats", ".stats"):
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
                "wrong_words_per_session\n",
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


def save_mistakes_filehandler(m_dict):
    """creates a filehandler instance for the mistakes dictionary"""
    num = check_for_mistakes_file()
    num += 1 if num else 1
    if num < 10:
        num = f"0{num}"
    create_new_file_object()
    set_filename_to_file_object(
        f"{get_todays_date().replace('.','-')}-{str(num)}-mistakes.csv"
    )
    set_outside_dictionary_to_file_instance(m_dict)
    save_file_object_instance()


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
    used to delete instances from lists now unused, but might be used again in the future
    """
    pass


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


def collect_data():
    if not is_vocab_dict():
        return
    date = get_todays_date()
    stats = get_stats_holder()
    if not stats:
        print("no stats available in collect data")
        return
    stats.insert(0, date)
    save_stats(stats)


def restore_app_mode(gui):
    set_app_mode_to("start")
    set_outside_dictionary_to_file_instance(dict_obj.get_state().get_dict())
    save_file_object_instance()
    delete_instances()
    gui.revert_to_start()


def refresh_stats():
    set_stats_holder()