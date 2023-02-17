from datetime import datetime
import glob, re
from init_app import app_mode_list, app_mode, line_index


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


def is_user_stats():
    stats_list = []
    for x in glob.glob("user_stats.stats", recursive=True):
        stats_list.append(x)
    return True if stats_list else False


def longest_key(dictionary):
    """returns the longest key in a dictionary"""
    return len(max([x for x in dictionary.keys()], key=len))


def check_digits(string):
    """checks if string is a digit, if so, returns int, else returns False"""
    if string.isdigit():
        return int(string)
    else:
        return False


def check_dict_validity(dictionary: dict) -> bool:
    """checks if dictionary in instance is of type dict, if not, returns False"""
    return True if isinstance(dictionary, dict) else False


def set_app_mode_to(mode: str) -> None:
    """
    sets app_mode to mode:
    "start", "quiz","add_dict","edit","exit", "add_mode", "add","delete","loaded"
    """
    # check if mode is in app_mode_list, primarily for debugging
    if mode not in app_mode_list.get_state():
        print("invalid mode")
        return False
    app_mode.set_state(mode)


def get_app_mode():
    return app_mode.get_state()


def set_line_index_to(index):
    line_index.set_state(index)


def get_line_index():
    return line_index.get_state()


def clear_line_index():
    line_index.set_state(False)


def check_filename_validity(filename=None, ending=None):
    if filename.endswith(ending) and filename.count(".") == 1:
        return filename
    elif filename.count(".") == 0:
        filename = f"{filename}{ending}"
        return filename
    else:
        return False


def check_filename(filename, ending: str) -> any:
    pattern = "^[\w,\s-]+"
    endingslist = [".csv", ".txt", ".stats", ".tmp"]

    if ending not in endingslist:
        return False
    a = filename.split(".")
    x = re.search(pattern, a[0])
    return f"{a[0]}{ending}" if x else False
