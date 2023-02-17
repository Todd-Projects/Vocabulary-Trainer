"""creates classes and objects for keeping options, settings and the like"""


class Vars:
    def __init__(self):
        self.vars = None

    def set_state(self, var):
        self.vars = var

    def get_state(self):
        return self.vars

    def append_state(self, var):
        if type(self.vars) != list:
            return f"{var} is not a list"
        self.vars.append(var)

    def remove_state(self, var):
        if type(self.vars) != list:
            return f"{var} is not a list"
        self.vars.remove(var)

    def delete_instance(self):
        del self

    def __repr__(self):
        return f"{self.vars} is of type {type(self.vars)}"


# all current variables
(
    mistake_dict_counter,
    stats_holder,
    dict_obj,
    file_obj,
    app_mode,
    file_list,
    line_index,
    hold_success_stats,
    hold_mistakes_list,
    app_mode_list,
) = (Vars(), Vars(), Vars(), Vars(), Vars(), Vars(), Vars(), Vars(), Vars(), Vars())

stats_holder.set_state([])
mistake_dict_counter.set_state(0)
dict_obj.set_state("")
file_obj.set_state("")
app_mode_list.set_state(
    ["start", "quiz", "add_dict", "edit", "exit", "add_mode", "add", "delete","loaded"]
)
app_mode.set_state("start")  # modes: "start", "quiz", "edit", "add", "loaded","delete","loaded"
file_list.set_state([])
line_index.set_state(0)
hold_success_stats.set_state([])
hold_mistakes_list.set_state([])

# delete all variables
def delete_all_variables():
    mistake_dict_counter.set_state(0)
    stats_holder.set_state([])
    dict_obj.set_state("")
    file_obj.set_state("")
    app_mode.set_state("start")
    file_list.set_state("")
    line_index.set_state(0)
