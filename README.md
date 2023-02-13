Vocabulary-Trainer
Vocabulary learning app coded purely in python

This app enables users to:

load dictionaries (first-language - second-language) as csv files
add dictionaries as csv files
edit dictionaries
(auto)save dictionaries
train / learn the words from the dictionaries
The app automatically creates a statistics file for future use, e.g. to gain insights into learning behaviour

main dependency: TKinter

Main structure:

classes
vocabulary_gui.py contains a stylesheet in dictionaries contains two classes for the GUI
vocabulary_app.py contains two classes to create dictionary objects and to do basic CRUD actions on them additionally the second class enables the operations for quizzes, stats
filehandling.py class for loading and saving the dicts
class Vars: creates simple objects for storing temporary data like appmodes or states
modules
there are several more files that are related to the individual functions:

adding a dict
quiz
editing
choosing a dict
