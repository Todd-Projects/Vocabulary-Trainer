from datetime import datetime
import glob
from init_app import app_mode, line_index


def get_todays_date():
    """
    param: None
    return: str: today's date
    """
    today = datetime.now()
    return today.strftime("%d.%m.%Y")


def get_filelist():
    """gets all .csv files from root folder"""
    filelist = []
    for x in glob.glob("*.csv", recursive=True):
        filelist.append(x)
    return filelist


def longest_key(dictionary):
    """returns the longest key in a dictionary"""
    return len(max([x for x in dictionary.keys()], key=len))


def check_digits(string):
    """checks if string is a digit, if so, returns int, else returns False"""
    if string.isdigit():
        return int(string)
    else:
        return False


def check_dict_validity(dictionary):
    """checks if dictionary in instance is of type dict, if not, returns False"""
    return True if isinstance(dictionary, dict) else False


def set_app_mode_to(mode):
    """
    sets app_mode to mode:
    "start", "quiz","add_dict","edit","exit"
    """
    app_mode.set_state(mode)


def get_app_mode():
    return app_mode.get_state()


def set_line_index_to(index):
    line_index.set_state(index)


def get_line_index():
    return line_index.get_state()
