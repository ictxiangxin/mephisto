__author__ = 'ict'

import re

token_tuple = [
    ("name",      r"[_a-zA-Z][_a-zA-Z0-9]*"),
    ("dot",       r"\."),
    ("bracket_l", r"\("),
    ("bracket_r", r"\)"),
    ("toward",    r"\->"),
    ("by",        r":"),
    ("end",       r";"),
    ("separator", r","),
    ("skip",      r"[ \t]+"),
    ("newline",   r"\n|\r\n"),
    ("invalid",   r"."),
]

token_regrex = "|".join("(?P<%s>%s)" % pair for pair in token_tuple)

terminal_index = {
    "assign":    0,
    "bracket_l": 1,
    "bracket_r": 2,
    "by":        3,
    "dot":       4,
    "end":       5,
    "name":      6,
    "separator": 7,
    "toward":    8,
    "$":         9,
}

action_table = [
    ["e",   "e",   "e",   "e",   "e",   "e",   "s1",  "e",   "e",     "e"],
    ["e",   "e",   "e",   "e",   "s6",  "e",   "e",   "e",   "e",     "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "e",   "s7",  "s8",    "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "e",   "r9",  "r9",    "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "s1",  "e",   "e",     "a"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "r12", "e",   "e",   "r12"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "s10", "e",   "e",     "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "s1",  "e",   "e",     "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "s1",  "e",   "e",     "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "r13", "e",   "e",   "r13"],
    ["e",   "e",   "r8",  "r8",  "e",   "e",   "e",   "r8",  "r8",    "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "e",   "r10", "r10",   "e"],
    ["e",   "e",   "e",   "s13", "e",   "e",   "e",   "e",   "e",     "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "s14", "e",   "e",     "e"],
    ["e",   "s16", "e",   "e",   "e",   "e",   "e",   "e",   "e",     "e"],
    ["e",   "e",   "e",   "e",   "e",   "s17", "e",   "e",   "e",     "e"],
    ["e",   "e",   "r4",  "e",   "e",   "e",   "s19", "r4",  "e",     "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "r11", "e",   "e",   "r11"],
    ["e",   "e",   "r2",  "e",   "e",   "e",   "e",   "r2",  "e",     "e"],
    ["s23", "e",   "r6",  "e",   "s6",  "e",   "e",   "r6",  "e",     "e"],
    ["e",   "e",   "r14", "e",   "e",   "e",   "e",   "r14", "e",     "e"],
    ["e",   "e",   "r5",  "e",   "e",   "e",   "e",   "r5",  "e",     "e"],
    ["e",   "e",   "s25", "e",   "e",   "e",   "e",   "s24", "e",     "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "s26", "e",   "e",     "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "s19", "e",   "e",     "e"],
    ["e",   "e",   "e",   "e",   "e",   "r7",  "e",   "e",   "e",     "e"],
    ["e",   "e",   "r6",  "e",   "s6",  "e",   "e",   "r6",  "e",     "e"],
    ["e",   "e",   "r1",  "e",   "e",   "e",   "e",   "r1",  "e",     "e"],
    ["e",   "e",   "r3",  "e",   "e",   "e",   "e",   "r3",  "e",     "e"],
]

non_terminal_index = {
    "argument":      0,
    "argument_list": 1,
    "data":          2,
    "function":      3,
    "item":          4,
    "item_list":     5,
    "line":          6,
    "logic":         7,
}

goto_table = [
    [-1, -1, -1, -1, 3,  2,  5,   4],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, 3,  2,  9,  -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, 11, -1, -1, -1],
    [-1, -1, -1, -1, 12, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, 15, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [18, 22, 20, -1, 21, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, 27, -1, 21, -1, -1, -1],
    [28, -1, 20, -1, 21, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
]

reduce_symbol_sum = {
    0:  1,
    1:  3,
    2:  1,
    3:  3,
    4:  0,
    5:  1,
    6:  1,
    7:  4,
    8:  3,
    9:  1,
    10: 3,
    11: 6,
    12: 1,
    13: 2,
    14: 1,
}

reduce_to_non_terminal = {
    0:  "start",
    1:  "argument",
    2:  "argument_list",
    3:  "argument_list",
    4:  "argument_list",
    5:  "data",
    6:  "data",
    7:  "function",
    8:  "item",
    9:  "item_list",
    10: "item_list",
    11: "line",
    12: "logic",
    13: "logic",
    14: "argument",
}


def parse(filename):
    with open(filename, "r") as fp:
        text = fp.read().lower()
        token_list = tokenize(text)
        tree_list = grammar_analysis(token_list)
        return tree_list


def tokenize(string):
    token_list = list()
    line_number = 1
    for one_token in re.finditer(token_regrex, string):
        token_class = one_token.lastgroup
        token_string = one_token.group(token_class)
        if token_class == "skip":
            pass
        elif token_class == "newline":
            line_number += 1
        elif token_class == "invalid":
            raise RuntimeError("[Line: %d] Invalid token: %s" % (line_number, token_string))
        else:
            token_list.append((token_class, token_string, line_number))
    token_list.append(("$", "", line_number))
    return token_list


def grammar_analysis(token_list):
    logic = []
    symbol_stack = []
    one_logic = {}
    line_start_record = {}
    stack = [0]
    token_index = 0
    while token_index < len(token_list):
        token = token_list[token_index]
        token_type = token[0]
        token_line = token[2]
        if token_line not in line_start_record:
            line_start_record[token_line] = token_index
        now_state = stack[-1]
        operation = action_table[now_state][terminal_index[token_type]]
        operation_flag = operation[0]
        if operation_flag == "e":
            error_line = token[2]
            error_code = ""
            offset = 0
            for i in range(line_start_record[error_line], len(token_list)):
                if token_list[i][2] == error_line:
                    error_code += " " + token_list[i][1]
                    if i < token_index:
                        offset += len(token_list[i][1]) + 1
            error_message_head = "\nGrammar error [line %d]:" % error_line
            error_message = error_message_head + error_code + "\n"
            error_message += " " * (len(error_message_head) + offset) + "^" * len(token[1])
            raise Exception(error_message)
        elif operation_flag == "s":
            operation_number = int(operation[1:])
            stack.append(operation_number)
            token_index += 1
            if token_type in ["name"]:
                symbol_stack.append(token[1])
        elif operation_flag == "r":
            operation_number = int(operation[1:])
            reduce_sum = reduce_symbol_sum[operation_number]
            for _ in range(reduce_sum):
                stack.pop()
            now_state = stack[-1]
            now_non_terminal_index = non_terminal_index[reduce_to_non_terminal[operation_number]]
            goto_next_state = goto_table[now_state][now_non_terminal_index]
            if goto_next_state == -1:
                raise Exception("Invalid goto action: state=%d, non-terminal=%d" % (now_state, now_non_terminal_index))
            stack.append(goto_table[now_state][now_non_terminal_index])
            if operation_number == 0:
                # start -> logic
                pass
            elif operation_number == 1:
                # argument -> name assign data
                pass
            elif operation_number == 2:
                # argument_list -> argument
                argument = symbol_stack.pop()
                symbol_stack.append([argument])
            elif operation_number == 3:
                # argument_list -> argument_list separator argument
                argument = symbol_stack.pop()
                argument_list = symbol_stack.pop()
                symbol_stack.append(argument_list + [argument])
            elif operation_number == 4:
                # argument_list -> ~
                symbol_stack.append([])
            elif operation_number == 5:
                # data -> item
                pass
            elif operation_number == 6:
                # data -> name
                pass
            elif operation_number == 7:
                # function -> name bracket_l argument_list bracket_r
                argument_list = symbol_stack.pop()
                name = symbol_stack.pop()
                symbol_stack.append((name, argument_list))
            elif operation_number == 8:
                # item -> name dot name
                name2 = symbol_stack.pop()
                name1 = symbol_stack.pop()
                symbol_stack.append((name1, name2))
            elif operation_number == 9:
                # item_list -> item
                item = symbol_stack.pop()
                symbol_stack.append([item])
            elif operation_number == 10:
                # item_list -> item_list separator item
                item = symbol_stack.pop()
                item_list = symbol_stack.pop()
                symbol_stack.append(item_list + [item])
            elif operation_number == 11:
                # line -> item_list toward item by function end
                function = symbol_stack.pop()
                item = symbol_stack.pop()
                item_list = symbol_stack.pop()
                one_logic["condition"] = item_list
                one_logic["result"] = item
                one_logic["function"] = function
                logic.append(one_logic)
                one_logic = {}
            elif operation_number == 12:
                # logic -> line
                pass
            elif operation_number == 13:
                # logic -> logic line
                pass
            elif operation_number == 14:
                # argument -> data
                data = symbol_stack.pop()
                symbol_stack.append(data)
            else:
                raise Exception("Invalid reduce number: %d" % operation_number)
        elif operation_flag == "a":
            return logic
        else:
            raise Exception("Invalid action: %s" % operation)


class MephistoLogic:
    def __init__(self, filename):
        logic_tree_list = parse(filename)
        self.__logic = {}
        for logic_tree in logic_tree_list:
            condition = logic_tree["condition"]
            result = logic_tree["result"]
            function = logic_tree["function"]
            if len(condition) == 1:
                single_condition = condition[0]
                if single_condition not in self.__logic:
                    self.__logic[single_condition] = {}
                self.__logic[single_condition][result] = ("single", function)
            else:
                for i in range(len(condition)):
                    multi_condition = condition[i]
                    if multi_condition not in self.__logic:
                        self.__logic[multi_condition] = {}
                    temp_others = []
                    for j in range(len(condition)):
                        if i == j:
                            continue
                        temp_others.append(condition[j])
                    self.__logic[multi_condition][result] = ("multi", temp_others, function)

    def decide_attribute(self, attribute):
        if attribute not in self.__logic:
            return None
        result = {"single": [], "multi": []}
        for d_attribute, d_function in self.__logic[attribute].items():
            if d_function[0] == "single":
                result["single"].append(d_attribute)
            elif d_function[0] == "multi":
                result["multi"].append((d_attribute, d_function[1]))
        return result
