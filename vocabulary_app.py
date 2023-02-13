""" initializing a class for a vocabulary instance """
import copy
import re


class stat_counter:
    """class to count the number of correct and wrong answers"""

    def __init__(self):
        self.correct = 0
        self.wrong = 0
        self.item = 0
        self.percentage = 0
        self.wrong_pair = {}

    def get_correct(self):
        return self.correct

    def get_wrong(self):
        return self.wrong

    def get_item(self):
        return self.item

    def get_wrong_pair(self):
        return self.wrong_pair

    def get_percentage(self):
        return round(self.percentage)

    def add_correct(self):
        self.correct += 1

    def add_wrong(self):
        self.wrong += 1

    def add_item(self):
        self.item += 1

    def add_wrong_pair(self, dictionary):
        self.wrong_pair.update(dictionary)

    def add_percentage(self):
        self.percentage = self.correct / self.item * 100

    def reset(self):
        self.correct = 0
        self.wrong = 0


# wc: word_counter
wc = stat_counter()


class Vocab:
    """
    holds, validates, and manipulates a dictionary
    """

    def __init__(self, v_dict=None, *args, **kwargs):
        self.log_dict = {}
        self.keep_score_val = 0
        self.mistakes_dict = {}
        if v_dict is not None:
            self.integrate_new_vocab_dict(v_dict)
        else:
            print(
                "Vocab instance created without a dictionary.\nmethods that require a dictionary will not work.\nuse integrate_new_vocab_dict() to add a dictionary to the instance"
            )

    def integrate_new_vocab_dict(self, dictionary):
        """
        integrate new dict into existing dict
        needs to be run if new instance is created without a dict
        """
        self.set_dict(dictionary)
        self.make_key_list()
        self.dict_length = len(self.v_dict)

    def set_dict(self, dict):
        """sets the dictionary"""
        self.v_dict = dict

    def get_dict(self):
        """returns the dictionary"""
        return self.v_dict

    def make_key_list(self):
        """helper function for ease of use - creates a list of the keys"""
        self.key_list = list(self.v_dict.keys())

    def get_dict_length(self):
        """returns int for length of dictionary"""
        return self.dict_length

    def is_new_dict_key(self, dict_key):
        """checks if key is new or already in the dict"""
        return False if dict_key in self.v_dict.keys() else True

    def is_val_list(self, dict_vals):
        """checks if vals are of type list or not"""
        return False if not isinstance(dict_vals, list) else True

    def remove_whitespaces(self, list_of_vals):
        """when new items are added to the dictionary, superfluous whitespaces are trimmed (before, inside, end)"""
        new_vals = []
        for i, item in enumerate(list_of_vals):
            new_vals.append(
                re.sub(" +", " ", item.strip())
            )  # trims first and last whitespaces
        return new_vals


class VocabManipulation(Vocab):
    """manipulates the dictionary"""

    def __init__(self, v_dict=None, *args, **kwargs):
        super().__init__(v_dict, *args, **kwargs)

    def check_for_difficulty(self, dict_index, user_input, difficulty):
        if difficulty == "h":
            ele = [x for x in self.v_dict[self.key_list[dict_index]]]
        elif difficulty == "e":
            ele = [x.lower() for x in self.v_dict[self.key_list[dict_index]]]
            user_input = user_input.lower()
        return ele, user_input

    def initialize_session(self):
        self.words_per_quiz = 0
        self.mistakes_per_quiz = 0
        self.mistakes_per_quiz_dict = {}
        self.correct_per_quiz = 0

    def add_dict_items(self, dict_key, dict_vals):
        """
        adds key / vals pair to dict
        params: dict_key: str
        dict_vals: list
        """
        trimmed_vals = self.remove_whitespaces(dict_vals)
        self.v_dict[dict_key] = trimmed_vals
        self.log_dict[dict_key] = f"added: {trimmed_vals}"

    def delete_dict_item(self, dict_key):
        """deletes key / vals pair"""
        self.v_dict.pop(dict_key)
        self.log_dict[dict_key] = "deleted"

    def is_correct(self, dict_index, user_input, difficulty):
        """
        checks if the answer is correct
        params: dict_index: int
        user_input: str
        """
        is_correct = []
        # extract list of vals from dict-key
        ele, user_input = self.check_for_difficulty(dict_index, user_input, difficulty)
        for val in ele:
            is_correct.append(True) if user_input == val else is_correct.append(False)
        if True in is_correct:
            last_score = self.set_score(answer=True, dict_index=dict_index, vals=ele)
        else:
            last_score = self.set_score(answer=False, dict_index=dict_index, vals=ele)
        return last_score

    def set_score(self, answer, dict_index=False, vals=False):
        if answer:
            self.correct_per_quiz += 1
            wc.add_correct()
            last_score = True
        else:
            self.mistakes_per_quiz += 1
            wc.add_wrong()
            self.mistakes_per_quiz_dict[self.key_list[dict_index]] = vals
            last_score = False
        return last_score

    def get_mistakes(self):
        if self.mistakes_per_quiz_dict:
            answerstring = (
                ", ".join([str(elem) for elem in self.mistakes_per_quiz_dict.keys()])
                + f" hattest du noch nicht richtig.{self.correct_per_quiz} aber schon.\nHier sind die richtigen Antworten:"
            )
            wc.add_wrong_pair(self.mistakes_per_quiz_dict)
            return (
                answerstring,
                self.mistakes_per_quiz_dict,
                self.mistakes_dict_string(),
            )
        return False, False, False

    def mistakes_dict_string(self):
        word, a = "", ""
        complete_list = []
        string1 = [ele for ele in list(self.mistakes_per_quiz_dict.keys())]
        string2 = [ele for ele in list(self.mistakes_per_quiz_dict.values())]

        for i, val in enumerate(string2):
            word = string1[i] + ": "
            for val in string2[i]:
                complete_list.append("")
                word += val + ", "
            complete_list[i] = f"{word}"[0:-2]

        a = ".".join(complete_list) + " "
        return a if a else False

    def get_success_stats(self):
        return [
            f"Du hattest {self.correct_per_quiz} von {self.dict_length} Wörtern richtig, das sind:",
            self.get_percents(),
        ]

    def get_percents(self, string=True):
        wc.add_percentage()
        return (
            str((self.correct_per_quiz / self.dict_length) * 100)[0:4] + "%"
            if string == True
            else round((self.correct_per_quiz / self.dict_length) * 100)
        )

    def return_score_values(self):
        return self.correct_per_quiz

    def get_prompt(self, dict_index):
        """returns a new prompt for index"""
        self.words_per_quiz += 1
        wc.add_item()
        return False if dict_index >= self.dict_length else self.key_list[dict_index]

    def update_entry(self, first_l, second_l, dict_index):
        temp_key_list = copy.deepcopy(self.key_list)
        temp_key_list[dict_index] = first_l
        temp_dict = dict(zip(temp_key_list, self.v_dict.values()))
        temp_dict[first_l] = second_l
        del self.v_dict, self.key_list
        self.v_dict = temp_dict
        self.key_list = temp_key_list

    def delete_entry(self, first_l, second_l, dict_index):
        self.log_dict[first_l] = [second_l, "deleted"]
        self.v_dict.pop(first_l, False)

    def collect_stats(self):
        return [
            wc.get_item(),
            wc.get_correct(),
            wc.get_wrong(),
            wc.get_wrong_pair(),
            wc.get_percentage(),
        ]
