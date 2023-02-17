"""
loading and saving a file
"""
import csv


class FileHandling:
    def __init__(self):
        """
        __init__ _summary_
        Args:
            filename (string.csv):
            dictionary (dict -> {key: [list]}):
        """
        self.dictionary = {}
        self.filename = None
        self.list_of_items = None

    def set_filename(self, filename):
        """sets filename"""
        self.filename = filename

    def set_dictionary(self, dictionary):
        """sets dictionary"""
        self.dictionary = dictionary

    def get_dictionary(self):
        """returns the dictionary"""
        return self.dictionary

    def get_filename(self):
        """
        get_filename returns filename to user
        """
        return self.filename

    def set_dictionary(self, dictionary):
        """sets self.vocab_dict to a dictionary"""
        self.dictionary = dictionary

    def create_list_of_items(self):
        """flattens a dictionary to a list of lists"""
        list_of_items = []
        for key, val in self.dictionary.items():
            list_of_items.append([key, *val])
        self.list_of_items = list_of_items

    def get_list_of_items(self):
        self.create_list_of_items()
        return self.list_of_items

    def save_file(self, mode="w"):
        """saves file, creates list of items first"""
        if self.filename is None:
            return False
        self.create_list_of_items()
        with open(self.filename, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerows(self.list_of_items)

    def load_file(self):
        """loads a file from drive, file needs to be in same folder as .exe or needs absolute filepath"""
        if self.filename is None:
            return False
        with open(self.filename, mode="r", encoding="utf-8-sig") as file:
            vocabulary = [item for item in csv.reader(file, delimiter=";")]
            for line in vocabulary:
                a = line.pop(0)
                self.dictionary[a] = line
    
    def delete_self(self):
        """deletes instance"""
        del self

class MistakesDict(FileHandling):
    def __init__(self, filename, dictionary):
        super().__init__()
        self.filename = filename
        self.dictionary = dictionary

    def save_mistakes_filehandler(self):
        """creates a filehandler instance for the mistakes dictionary"""
        self.save_file()
    
    def delete_self(self):
        """deletes instance"""
        del self
    

