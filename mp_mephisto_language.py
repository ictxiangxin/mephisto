import re


boson_token_tuple = [
    ("operator",      r"[_a-z][_a-z]*"),
    ("string",        r"\".*?[^\\]\"|\"\""),
    ("bracket_left",  r"\("),
    ("bracket_right", r"\)"),
    ("comma",         r"\,"),
    ("skip",          r"\t|\ "),
    ("newline",       r"\r\n|\n"),
    ("boson_invalid", r"."),
]

boson_ignore = {
    "skip",
}

boson_error = {
    "boson_invalid",
}

boson_token_regular_expression = "|".join("(?P<%s>%s)" % pair for pair in boson_token_tuple)


terminal_index = {
    "bracket_left":  0,
    "bracket_right": 1,
    "comma":         2,
    "operator":      3,
    "string":        4,
    "$":             5,
}

action_table = [
    ["s2",  "e",   "e",   "e",   "e",    "e"],
    ["r1",  "e",   "e",   "e",   "e",   "r1"],
    ["e",   "e",   "e",   "s4",  "e",    "e"],
    ["s2",  "e",   "e",   "e",   "e",    "a"],
    ["e",   "e",   "e",   "e",   "s6",   "e"],
    ["r2",  "e",   "e",   "e",   "e",   "r2"],
    ["e",   "r4",  "r4",  "e",   "e",    "e"],
    ["e",   "s8",  "s9",  "e",   "e",    "e"],
    ["r3",  "e",   "e",   "e",   "e",   "r3"],
    ["e",   "e",   "e",   "e",   "s10",  "e"],
    ["e",   "r5",  "r5",  "e",   "e",    "e"],
]

non_terminal_index = {
    "instruction":      0,
    "instruction_list": 1,
    "string_list":      2,
}

goto_table = [
    [1,  3,  -1],
    [-1, -1, -1],
    [-1, -1, -1],
    [5,  -1, -1],
    [-1, -1,  7],
    [-1, -1, -1],
    [-1, -1, -1],
    [-1, -1, -1],
    [-1, -1, -1],
    [-1, -1, -1],
    [-1, -1, -1],
]

reduce_symbol_sum = {
    0: 1,
    1: 1,
    2: 2,
    3: 4,
    4: 1,
    5: 3,
}

reduce_to_non_terminal = {
    0: "start",
    1: "instruction_list",
    2: "instruction_list",
    3: "instruction",
    4: "string_list",
    5: "string_list",
}


def mephisto_language_lexical(text):
    boson_token_list = []
    line_number = 1
    for one_token in re.finditer(boson_token_regular_expression, text):
        token_class = one_token.lastgroup
        token_text = one_token.group(token_class)
        if token_class in boson_ignore:
            continue
        elif token_class == "newline":
            line_number += 1
        elif token_class in boson_error:
            raise Exception("Invalid token: (%s, \"%s\")" % (token_class, token_text))
        else:
            boson_token_list.append((token_class, token_text, line_number))
    boson_token_list.append(("$", "", line_number))
    return boson_token_list


def mephisto_language_grammar(token_list):
    symbol_stack = []
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
            if token_type in {"operator", "string"}:
                symbol_stack.append(token)
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
                pass
            elif operation_number == 1:
                instruction = symbol_stack.pop()
                boson_reduce = [instruction]
                symbol_stack.append(boson_reduce)
            elif operation_number == 2:
                instruction = symbol_stack.pop()
                instruction_list = symbol_stack.pop()
                boson_reduce = instruction_list + [instruction]
                symbol_stack.append(boson_reduce)
            elif operation_number == 3:
                string_list = symbol_stack.pop()
                operator = symbol_stack.pop()
                boson_reduce = (operator, tuple(string_list))
                symbol_stack.append(boson_reduce)
            elif operation_number == 4:
                string = symbol_stack.pop()
                boson_reduce = [string]
                symbol_stack.append(boson_reduce)
            elif operation_number == 5:
                string = symbol_stack.pop()
                string_list = symbol_stack.pop()
                boson_reduce = string_list + [string]
                symbol_stack.append(boson_reduce)
            else:
                raise Exception("Invalid reduce number: %d" % operation_number)
        elif operation_flag == "a":
            break
        else:
            raise Exception("Invalid action: %s" % operation)
    return symbol_stack[0]
