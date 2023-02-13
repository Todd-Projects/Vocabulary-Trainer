from tkinter import *
from tkinter import Tk
from helpers import longest_key
from vocab_main import (
    pass_line_index_to_loading,
    choose_dictionary,
    get_app_mode,
    set_app_mode_to,
    exit_app,
)
from quiz_mode import get_quiz_type
from edit_mode import (
    prepare_edit_mode,
    end_edit_mode,
    add_word,
    prepare_entries_for_edit,
    delete_entry,
    add_word,
    get_entry_val,
)
from add_dict import add_dict

tk = Tk()
# could these be defined as global variables somewhere else?
entry_var = ""
first_lg_var = ""
# this variable is used to store the value of the radio button, but this is a strange place to define it
radio_button_var = StringVar()
radio_button2_var = StringVar()
# these two variables form the basis for the app's logic
gui_dict = {}
funcs = {}


def set_gui_dict():
    """sets menu items and function-calls for the app, as well as colors, fonts and geometry"""
    # funcs sets menu items and function-calls for the app, integers refer to the frame they are placed in
    # last integer refers to frame again, when there is an associated frame to the function of the button
    global funcs
    funcs = {
        "Wörterbuch wählen": [choose_dictionary, 1, 0, "pack", "choose"],
        "abfragen": [get_quiz_type, 1, 3, "pack", "quiz"],
        "neues Wörterbuch anlegen": [add_dict, 1, None, "pack", "add_dict"],
        "Wörterbuch bearbeiten": [prepare_edit_mode, 1, 1, "pack", "edit"],
        "beenden": [None, 1, None, "pack", "exit"],
        "abschicken": [get_entry_val, 3, 1, "unpack"],
        "zum Wörterbuch hinzufügen": [add_word, 3, None, "unpack", "add"],
        "löschen": [delete_entry, 3, None, "unpack", "delete"],
        "bearbeiten beenden": [end_edit_mode, 3, None, "unpack"],
        "neu": [add_word, 3, None, "nopack"],
        "dividers": [None, None, None, "nopack", 5],
    }

    gui_dict["colors"] = {
        "dark": "#444444",
        "light": "#878683",
        "font_light": "#ffffff",
        "accent": "#eead0e",
        "disabled_bg": "#373737",
        "special": "#22ee0e",
        "mid": "#5E5D5B",
    }

    gui_dict["fonts"] = {
        "regular": "Tahoma 11",
        "large": "Tahoma 12 bold",
        "mono": "Consolas 11",
        "headline": ("Tahoma", 14, "bold", "italic"),
        "body": ("Tahoma", 12, "normal", "roman"),
        "regular_large": "Tahoma 12",
        "quiz": "Tahoma 14 bold",
    }

    gui_dict["container"] = {
        "title": "MyVocabulary Trainer",
        "width": 800,
        "height": 700,
        "background": "dark",
        "foreground": "light",
    }
    # "frames":["relwidth","relheight","relx","rely","headline for label"]
    gui_dict["frames"] = {
        0: [0.6, 0.4, 0, 0, "Choose a dictionary"],
        1: [0.4, 0.4, 0.6, 0, "Choose a function"],
        2: [0.6, 0.6, 0, 0.4, "Infos"],
        3: [0.4, 0.6, 0.6, 0.4, "Quiz"],
    }

    gui_dict["geometry"] = {
        "screen_x": int(
            (tk.winfo_screenwidth() / 2) - (gui_dict["container"]["width"] / 2)
        ),
        "screen_y": int(
            (tk.winfo_screenheight() / 2) - (gui_dict["container"]["height"] / 2)
        ),
    }

    gui_dict["placement"] = {
        "position": f"{gui_dict['container']['width']}x{gui_dict['container']['height']}+{gui_dict['geometry']['screen_x']}+{gui_dict['geometry']['screen_y']}"
    }

    gui_dict["text_widget"] = {
        0: {
            "frame": 2,
            "background": "dark",
            "foreground": "font_light",
            "font": "regular",
            "text": "Wörterbuch auswählen, um zu beginnen",
            "width": 30,
            "height": 20,
            "state": "disabled",
            "highlightthickness": 0,
        }
    }

    gui_dict["listboxes"] = {
        0: {
            "frame": funcs["Wörterbuch wählen"][2],
            "label": "Choose a dictionary",
            "yscrollbar": True,
            "background": "dark",
            "foreground": "font_light",
            "name": "dict_listbox",
        }
    }

    gui_dict["check_button"] = {
        0: {
            "frame": 1,
            "label": "zufällige Reihenfolge",
            "default": "random",
            "var": radio_button_var,
            "background": "dark",
            "foreground": "font_light",
            "highlightbackground": "mid",
            "highlightforeground": "dark",
            "disabledforeground": "dark",
            "selectcolor": "dark",
            "offvalue": 0,
            "onvalue": 1,
        },
        1: {
            "frame": 1,
            "label": "strenge Auswertung",
            "default": "mild",
            "var": radio_button2_var,
            "background": "dark",
            "foreground": "font_light",
            "highlightbackground": "mid",
            "highlightforeground": "dark",
            "disabledforeground": "dark",
            "selectcolor": "dark",
            "offvalue": 0,
            "onvalue": 1,
        },
    }

    gui_dict["keys_for_widgets"] = {
        "sorting": 0,
        "vocab_entry": 0,
        "german_entry": 1,
        "difficulty": 1,
    }

    gui_dict["labels"] = {
        0: {
            "frame": funcs["abfragen"][2],
            "background": "dark",
            "foreground": "accent",
            "font": "regular",
            "text": "Übersetze das folgende Wort:",
            "default": "",
        },
        1: {
            "frame": funcs["abfragen"][2],
            "background": "dark",
            "foreground": "font_light",
            "font": "regular_large",
            "text": "",
            "default": "",
        },
        2: {
            "frame": funcs["abfragen"][2],
            "background": "dark",
            "foreground": "font_light",
            "font": "regular_large",
            "text": "",
            "default": "",
        },
    }

    # "return" mirrors the function call from funcs, integer refers to its own key (e.g. 0)
    gui_dict["entry_fields"] = {
        0: {
            "var": entry_var,
            "frame": 3,
            "background": "dark",
            "foreground": "light",
            "default": "",
            "return": ["abschicken", 0],
            "state": "unpack",
            "function": "quiz",
            "height": 1,
            "font": "quiz",
            "quiz": 0,
        },
        1: {
            "var": first_lg_var,
            "frame": 3,
            "background": "dark",
            "foreground": "light",
            "default": "",
            "return": ["abschicken", 0],
            "state": "unpack",
            "function": "edit",
            "height": 2,
            "font": "quiz",
            "edit": 1,
        },
    }
    longest_button = longest_key(funcs)
    return gui_dict, funcs, longest_button


class MainGui:
    """
    creates the basis for the GUI
    """

    def __init__(self, **kwargs):
        gui_dict, funcs, self.longest_button = set_gui_dict()
        self.funcs = funcs
        self.frames = {}
        self.holder = []
        self.var = StringVar()
        self.frame_holder = []
        self.label_holder = []
        self.frame_label_holder = []
        self.buttons_holder = []
        self.entry_holder = []
        self.check_holder = []
        self.textbox_holder = []
        self.decision = StringVar()
        self.frames = gui_dict["frames"]
        self.bg = gui_dict["container"]["background"]
        self.fonts = gui_dict["fonts"]
        self.colors = gui_dict["colors"]
        self.font_color = gui_dict["colors"]["light"]
        self.headline_color = gui_dict["colors"]["accent"]
        self.create_main_window()

    def create_main_window(self):
        """creates the main container for the frames"""
        tk.title(gui_dict["container"]["title"])
        tk.geometry(gui_dict["placement"]["position"])
        tk.configure(bg=self.colors[self.bg])
        self.create_frames()
        self.create_listboxes()
        self.create_labels()
        self.create_entry_fields()
        self.create_buttons()
        self.create_textboxes()
        self.create_check_button()
        tk.protocol("WM_DELETE_WINDOW", lambda m="beenden": self.clicked(keyword=m))

    def create_frames(self):
        """creates the main frames of the app"""
        for i, val in enumerate(self.frames):
            self.frame_holder.append("")
            self.frame_holder[i] = Frame(tk, bg=self.colors[self.bg])
            self.frame_holder[i].place(
                relwidth=self.frames[i][0],
                relheight=self.frames[i][1],
                relx=self.frames[i][2],
                rely=self.frames[i][3],
            )
            self.label_holder.append("")
            self.label_holder[i] = Label(
                self.frame_holder[i],
                text=self.frames[i][4],
                bg=self.colors[self.bg],
                fg=self.headline_color,
                font=self.fonts["headline"],
            )
            self.label_holder[i].pack(padx=5, pady=5)

    def create_listboxes(self):
        self.lb_scrollbar_holder = []
        for key in gui_dict["listboxes"]:
            self.holder.append("")
            self.lb_scrollbar_holder.append("")
            res = list(gui_dict["listboxes"].keys()).index(key)
            self.holder[res] = Listbox(
                self.frame_holder[gui_dict["listboxes"][key]["frame"]],
                bg=self.colors[gui_dict["listboxes"][key]["background"]],
                fg=self.colors[gui_dict["listboxes"][key]["foreground"]],
                font=self.fonts["regular"],
            )
            self.holder[res].pack(fill=BOTH, expand=1, padx=10, pady=5)
            self.holder[res].bind("<<ListboxSelect>>", self.onselect)
            self.lb_scrollbar_holder[res] = Scrollbar(
                self.holder[res], orient="vertical", width=12
            )
            self.lb_scrollbar_holder[res].config(command=self.holder[res].yview)
            self.holder[res]["yscrollcommand"] = self.lb_scrollbar_holder[res].set
            self.lb_scrollbar_holder[res].pack(side=RIGHT, fill=Y)

    def create_textboxes(self):
        self.tb_scrollbar_holder = []
        for key in gui_dict["text_widget"]:
            self.textbox_holder.append("")
            self.tb_scrollbar_holder.append("")
            self.textbox_holder[key] = Text(
                self.frame_holder[gui_dict["text_widget"][key]["frame"]],
                bg=self.colors[gui_dict["text_widget"][key]["background"]],
                fg=self.colors[gui_dict["text_widget"][key]["foreground"]],
                font=self.fonts[gui_dict["text_widget"][key]["font"]],
                width=gui_dict["text_widget"][key]["width"],
                height=gui_dict["text_widget"][key]["height"],
                highlightthickness=gui_dict["text_widget"][key]["highlightthickness"],
                wrap="word",
            )
            self.textbox_holder[key].insert(END, gui_dict["text_widget"][key]["text"])
            self.textbox_holder[key].config(state=gui_dict["text_widget"][key]["state"])
            self.textbox_holder[key].pack(fill=BOTH, expand=1, padx=10, pady=5)
            self.tb_scrollbar_holder[key] = Scrollbar(
                self.textbox_holder[key], orient="vertical", width=12
            )
            self.tb_scrollbar_holder[key].config(command=self.textbox_holder[key].yview)
            self.textbox_holder[key]["yscrollcommand"] = self.tb_scrollbar_holder[
                key
            ].set
            self.tb_scrollbar_holder[key].pack(side=RIGHT, fill=Y)

    def create_edit_view(self):
        res = list(gui_dict["listboxes"].keys()).index(0)
        self.holder.append("")
        self.holder[1] = Listbox(
            self.frame_holder[2],
            bg=self.colors[gui_dict["listboxes"][0]["background"]],
            fg=self.colors[gui_dict["listboxes"][0]["foreground"]],
            font=self.fonts["regular"],
        )
        self.holder[1].pack(fill=BOTH, expand=1, padx=10, pady=5)
        self.holder[1].bind("<<ListboxSelect>>", self.onselect)
        self.ev_scrollbar = Scrollbar(self.holder[-1], orient="vertical", width=12)
        self.ev_scrollbar.config(command=self.holder[-1].yview)
        self.holder[1]["yscrollcommand"] = self.ev_scrollbar.set
        self.ev_scrollbar.pack(side=RIGHT, fill=Y)
        for i, key in enumerate(list(self.funcs.keys())):
            self.pack_if_condition(i, key, "unpack")

    def pack_if_condition(self, i, key, condition):
        self.buttons_holder[i].pack(pady=5, padx=5) if self.funcs[key][
            3
        ] == condition else None

    def unpack_buttons_after_edit(self):
        for i, key in enumerate(list(self.funcs.keys())):
            self.buttons_holder[i].pack_forget() if self.funcs[key][
                3
            ] == "unpack" else None

    def create_buttons(self):
        """creates the buttons for the app"""
        for i, key in enumerate(list(self.funcs.keys())):
            if self.funcs[key][3] != "nopack":
                self.buttons_holder.append("")
                self.buttons_holder[i] = Button(
                    self.frame_holder[self.funcs[key][1]],
                    text=key,
                    bg=self.colors["dark"],
                    fg=self.colors["font_light"],
                    command=lambda m=key: self.clicked(keyword=m),
                    width=self.longest_button,
                )
                self.pack_if_condition(i, key, "pack")

    def create_entry_fields(self):
        for key in gui_dict["entry_fields"]:
            gui_dict["entry_fields"][key]["var"] = StringVar()
            self.entry_holder.append("")
            res = list(gui_dict["entry_fields"].keys()).index(key)
            self.entry_holder[res] = Entry(
                self.frame_holder[gui_dict["entry_fields"][key]["frame"]],
                textvariable=gui_dict["entry_fields"][key]["var"],
                background=self.colors[gui_dict["entry_fields"][key]["background"]],
                foreground=self.colors[gui_dict["entry_fields"][key]["foreground"]],
                width=self.longest_button,
                font=self.fonts[gui_dict["entry_fields"][key]["font"]],
            )
            self.entry_holder[res].bind("<Return>", self.set_decision)
            self.entry_holder[res].bind(
                "<Button-1>", lambda event, index=key: self.onclick(event, index)
            )
            self.entry_holder[res].bind(
                "<FocusIn>", lambda event, index=key: self.onclick(event, index)
            )
            self.manage_entry_fields(key, choice="pack", function="start")

    def manage_entry_fields(self, key, choice, function):

        if (
            gui_dict["entry_fields"][key]["state"] == choice
            and gui_dict["entry_fields"][key]["function"] == function
        ):
            self.entry_holder[key].pack(fill=X, pady=5, padx=5)
            self.entry_holder[key].insert(0, gui_dict["entry_fields"][key]["default"])
        return

    def create_check_button(self):
        for i, key in enumerate(list(gui_dict["check_button"])):
            gui_dict["check_button"][key]["var"] = IntVar()
            self.check_holder.append("")
            self.check_holder[i] = Checkbutton(
                self.frame_holder[gui_dict["check_button"][key]["frame"]],
                text=gui_dict["check_button"][key]["label"],
                variable=gui_dict["check_button"][key]["var"],
                bg=self.colors[gui_dict["check_button"][key]["background"]],
                offvalue=gui_dict["check_button"][key]["offvalue"],
                onvalue=gui_dict["check_button"][key]["onvalue"],
                fg=self.colors[gui_dict["check_button"][key]["foreground"]],
                highlightcolor=self.colors[
                    gui_dict["check_button"][key]["highlightbackground"]
                ],
                disabledforeground=self.colors[
                    gui_dict["check_button"][key]["disabledforeground"]
                ],
                selectcolor=self.colors[gui_dict["check_button"][key]["selectcolor"]],
            )
            self.check_holder[i].pack(pady=5, padx=5)

    def create_labels(self):
        # create labels
        for i, key in enumerate(list(gui_dict["labels"])):
            self.label_holder.append("")
            self.label_holder[i] = Label(
                self.frame_holder[gui_dict["labels"][key]["frame"]],
                text=gui_dict["labels"][key]["default"],
                bg=self.colors[gui_dict["labels"][key]["background"]],
                fg=self.colors[gui_dict["labels"][key]["foreground"]],
                font=self.fonts["regular"],
                wraplength=500,
            )
            self.label_holder[i].pack(fill=X, expand=True, pady=5, padx=5)

    def set_accent_color(self, keyword):
        for i, key in enumerate(list(self.funcs.keys())):
            if self.funcs[key][3] != "pack":
                continue
            self.buttons_holder[i].config(
                fg=self.colors["font_light"]
            ) if key != keyword else self.buttons_holder[i].config(
                fg=self.colors["accent"]
            )

    def onselect(self, key):
        if get_app_mode() != "edit":
            for i in self.holder[0].curselection():
                pass_line_index_to_loading(self, i - 2) if (i - 2 >= 0) else None
        elif get_app_mode() == "edit":
            for i in self.holder[1].curselection():
                prepare_entries_for_edit(self, i - 2, "abschicken") if i > 1 else None

    def clicked(self, evt=None, keyword="", wherefrom=""):
        if keyword == "beenden":
            set_app_mode_to("exit")
            self.decision.set("")
            exit_app()
        elif keyword == "Wörterbuch bearbeiten" and wherefrom == "add_dict":
            self.set_accent_color(keyword)
            self.clear_textbox(0)
            self.change_return_binding()
            self.funcs[keyword][0](self, keyword, wherefrom)
        elif keyword == "abfragen":
            self.entry_holder[0].focus_set()
            self.forward_click(keyword)
        else:
            self.forward_click(keyword)

    def forward_click(self, keyword=""):
        self.set_accent_color(keyword)
        self.clear_textbox(0)
        self.funcs[keyword][0](self, keyword)

    def change_return_binding(self):
        # TODO: set return binding to the button "zum Wörterbuch hinzufügen"
        # if in edit mode coming from add_dict, so that the user can add
        # the word to the dictionary by pressing return after entering
        # the word and the translation, instead of having to click the
        # button
        return

    def onclick(self, event, index):
        if get_app_mode() != "edit":
            self.entry_holder[index].config(foreground="white")
            self.entry_holder[index].delete(0, END)
        elif get_app_mode() == "edit":
            self.entry_holder[index].config(foreground="white")

    def set_decision(self, key=None):
        self.decision.set(key)
        return

    def clear_entry_field(self, index):
        self.entry_holder[index].delete(0, END)

    def clear_label(self, index):
        self.label_holder[index].config(text="")

    def clear_textbox(self, index=0):
        self.textbox_holder[index].config(state=NORMAL)
        self.textbox_holder[index].delete(1.0, END)
        self.textbox_holder[index].config(state=DISABLED)

    def clear_listbox(self, index, text=""):
        self.holder[index].config(state=NORMAL)
        self.holder[index].delete(0, END)
        self.holder[index].insert(0, text) if text else None
        self.holder[index].config(state=DISABLED)

    def pack_entry_field(self, btn_num=None, key=1, state=True):
        if state == True:
            self.entry_holder[key].pack(
                before=self.buttons_holder[btn_num], fill=X, pady=5, padx=5
            )
        elif state == False:
            self.entry_holder[key].pack_forget()

    @staticmethod
    def get_gui_dict():
        return gui_dict

    @staticmethod
    def get_funcs():
        return funcs


class GuiActions(MainGui):
    def __init__(self):
        super().__init__()

    def get_gui(self):
        return self

    def set_quizmode(self, action=True):
        if action is True:
            self.pack_if_condition(
                list(self.funcs.keys()).index("abschicken"), "abschicken", "unpack"
            )
            self.pack_entry_field(btn_num=5, key=0, state=True)
        elif action is False:
            self.unpack_buttons_after_edit()
            for i, val in enumerate(self.entry_holder):
                self.pack_entry_field(key=i, state=False)

    def switch_to_edit_view(self, divider, id, setting):
        if setting is True:
            self.textbox_holder[0].pack_forget()
            self.create_edit_view()
            self.pack_entry_field(divider, id[0], state=True)
        elif setting is False:
            self.holder[-1].pack_forget()
            self.holder[-1].destroy()
            del self.holder[-1]
            self.unpack_buttons_after_edit()
            self.pack_entry_field(divider, id[0], state=False)
            self.pack_entry_field(divider, id[1], state=False)
            self.create_textboxes()
            self.holder[0].delete(0, END)

    def set_label_to(self, string, frame):
        self.label_holder[frame].config(text=string)

    def populate_listbox(
        self, listbox_lines, key, listbox_index, first_line="", second_line=""
    ):
        self.holder[listbox_index].config(state=NORMAL)
        listbox_index = self.funcs[key][2]
        self.holder[listbox_index].insert(END, first_line)
        self.holder[listbox_index].insert(END, second_line)
        for item in listbox_lines:
            self.holder[listbox_index].insert(END, item)

    def process_line(self, value, index):
        if index > 1 and index < self.holder[0].size():
            pass_line_index_to_loading(value, index - 2)

    def get_entry(self):
        if get_app_mode() == "exit":
            return
        if get_app_mode() == "quiz":
            return gui_dict["entry_fields"][0]["var"].get()
        elif get_app_mode() == "edit":
            fl_keys = gui_dict["entry_fields"][0]["var"].get()
            sl_keys = gui_dict["entry_fields"][1]["var"].get().split(",")
            return [fl_keys, sl_keys]
        elif get_app_mode() == "add_dict":
            return gui_dict["entry_fields"][0]["var"].get()

    def wait_for_answer(self):
        tk.wait_variable(self.decision)
        return self.get_entry()

    def get_quiztype(self):
        sorting_key = gui_dict["keys_for_widgets"]["sorting"]
        difficulty_key = gui_dict["keys_for_widgets"]["difficulty"]
        sort = "z" if gui_dict["check_button"][sorting_key]["var"].get() else "n"
        diff = "h" if gui_dict["check_button"][difficulty_key]["var"].get() else "e"
        return sort, diff

    def print_s(self, string, type=False, field=["label", 1]):
        """prints a string to label with index field
        if type is True, it will append the string to the label
        if field[0] is textbox or label, it will print to the textbox or label with list-index field[1]
        if type is False, it will clear the textbox before printing"""
        if field[0] == "label" and get_app_mode != "quiz":
            self.label_holder[field[1]].config(text=string)
        if field[0] == "label" and get_app_mode() == "quiz":
            self.label_holder[field[1]].config(
                text=string, font=self.fonts[get_app_mode()]
            )
        elif field[0] == "textbox" and type == False:
            self.textbox_holder[field[1]].config(state=NORMAL)
            self.textbox_holder[field[1]].delete(1.0, END)
            self.textbox_holder[field[1]].insert(END, string)
            self.textbox_holder[field[1]].config(state=DISABLED)
        elif field[0] == "textbox" and type == True:
            self.textbox_holder[field[1]].config(state=NORMAL)
            self.textbox_holder[field[1]].insert(END, f"\n{string}")
            self.textbox_holder[field[1]].config(state=DISABLED)
        elif field[0] == "entry":
            self.entry_holder[field[1]].delete(0, END)
            self.entry_holder[field[1]].insert(0, string)
        return

    def set_image_to_textbox(self, textbox_index, badge):
        self.textbox_holder[textbox_index].image_create(END, image=badge)
        self.textbox_holder[textbox_index].image = badge

    def revert_to_start(self):
        self.label_holder[0].config(text=gui_dict["labels"][0]["default"])
        self.label_holder[1].config(text=gui_dict["labels"][1]["default"])
        self.label_holder[2].config(text=gui_dict["labels"][2]["default"])
        self.entry_holder[0].delete(0, END)
        self.entry_holder[0].config(
            foreground=self.colors[gui_dict["entry_fields"][0]["foreground"]]
        )
        self.entry_holder[0].insert(0, gui_dict["entry_fields"][0]["default"])
        self.entry_holder[0].pack_forget()


global gui
gui = GuiActions()
set_app_mode_to("start")
tk.mainloop()
