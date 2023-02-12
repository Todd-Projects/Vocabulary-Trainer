""" initializing a class for a vocabulary instance """
import copy
import re


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

    correct_per_session = 0
    mistakes_per_session = 0
    mistakes_per_session_dict = {}
    percents_per_session = []

    """ manipulates a dictionary """

    def __init__(self, v_dict=None, *args, **kwargs):
        super().__init__(v_dict, *args, **kwargs)

    def initialize_session(self):
        self.mistakes_dict = {}
        self.keep_score_val = 0
        self.mistakes_no = 0

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
        is_wrong = []
        # extract list of vals from dict-key
        ele, user_input = self.check_for_difficulty(dict_index, user_input, difficulty)
        for val in ele:
            is_wrong.append(True) if user_input == val else is_wrong.append(False)
        if True in is_wrong:
            self.set_score(answer=True, dict_index=dict_index, vals=ele)
            return self.set_score
        else:
            last_score = self.set_score(answer=False, dict_index=dict_index, vals=ele)
            return last_score

    def check_for_difficulty(self, dict_index, user_input, difficulty):
        if difficulty == "h":
            ele = [x for x in self.v_dict[self.key_list[dict_index]]]
        elif difficulty == "e":
            ele = [x.lower() for x in self.v_dict[self.key_list[dict_index]]]
            user_input = user_input.lower()
        return ele, user_input

    def set_score(self, answer, dict_index=False, vals=False):
        if answer:
            self.keep_score_val += 1
            last_score = True
            return
        else:
            self.mistakes_no += 1
            self.mistakes_dict[self.key_list[dict_index]] = vals
            last_score = False
        return last_score

    def get_mistakes(self):
        if self.mistakes_dict:
            answerstring = (
                ", ".join([str(elem) for elem in self.mistakes_dict.keys()])
                + " hattest du noch nicht richtig. \nHier sind die richtigen Antworten:"
            )
            VocabManipulation.mistakes_per_session_dict.update(self.mistakes_dict)
            return answerstring, self.mistakes_dict, self.mistakes_dict_string()
        return False, False, False

    def mistakes_dict_string(self):
        word, a = "", ""
        gesamtliste = []
        string1 = [ele for ele in list(self.mistakes_dict.keys())]
        string2 = [ele for ele in list(self.mistakes_dict.values())]

        for i, val in enumerate(string2):
            word = string1[i] + ": "
            for val in string2[i]:
                gesamtliste.append("")
                word += val + ", "
            gesamtliste[i] = f"{word}"[0:-2]

        a = ".".join(gesamtliste) + " "
        return a if a else False

    def get_success_stats(self):
        return [
            f"Du hattest {self.keep_score_val} von {self.dict_length} Wörtern richtig, das sind:",
            self.get_percents(),
        ]

    def get_percents(self,string=True):
        return str((self.keep_score_val / self.dict_length) * 100)[0:4] + "%" if string==True else round((self.keep_score_val / self.dict_length) * 100)

    def get_score(self):
        VocabManipulation.correct_per_session += self.keep_score_val
        VocabManipulation.mistakes_per_session += self.mistakes_no
        VocabManipulation.percents_per_session.append(self.get_percents(string=True))
        return self.keep_score_val

    def get_prompt(self, dict_index):
        """returns a new prompt for index"""
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

    @staticmethod
    def collect_stats():
        return [
            VocabManipulation.correct_per_session
            + VocabManipulation.mistakes_per_session,
            VocabManipulation.correct_per_session,
            VocabManipulation.mistakes_per_session,
            VocabManipulation.mistakes_per_session_dict,
            VocabManipulation.percents_per_session,
        ]
