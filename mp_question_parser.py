terminal_index = {
    "anonymous":       0,
    "attribute":       1,
    "city":            2,
    "date":            3,
    "degree":          4,
    "geo":             5,
    "latitude":        6,
    "longitude":       7,
    "metric":          8,
    "normal_question": 9,
    "number":          10,
    "phenomenon":      11,
    "time":            12,
    "time_attribute":  13,
    "time_lapse":      14,
    "time_literal":    15,
    "$":               16,
}

action_table = [
    ["s2",  "e",   "s6",  "e",   "e",   "s10", "e",   "e",   "e",   "e",   "e",   "s4",  "e",   "e",   "s1",  "s7",    "e"],
    ["r1",  "e",   "r1",  "e",   "e",   "r1",  "e",   "e",   "e",   "e",   "e",   "r1",  "e",   "e",   "r1",  "r1",   "r1"],
    ["r12", "r12", "r12", "r12", "e",   "r12", "r12", "r12", "r12", "r12", "e",   "r12", "r12", "r12", "e",   "r12",   "e"],
    ["r3",  "e",   "r3",  "e",   "e",   "r3",  "e",   "e",   "e",   "e",   "e",   "r3",  "e",   "e",   "r3",  "r3",   "r3"],
    ["r21", "e",   "r21", "e",   "e",   "r21", "e",   "e",   "e",   "e",   "e",   "r21", "e",   "e",   "r21", "r21", "r21"],
    ["r4",  "e",   "r4",  "e",   "e",   "r4",  "e",   "e",   "e",   "e",   "e",   "r4",  "e",   "e",   "r4",  "r4",   "r4"],
    ["r13", "r13", "r13", "r13", "e",   "r13", "r13", "r13", "r13", "r13", "e",   "r13", "r13", "r13", "e",   "r13",   "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "r35", "e",   "e",   "e",   "e",   "e",   "e",     "e"],
    ["s2",  "e",   "s6",  "e",   "e",   "s10", "e",   "e",   "e",   "e",   "e",   "s4",  "e",   "e",   "s1",  "s7",    "a"],
    ["r5",  "e",   "r5",  "e",   "e",   "r5",  "e",   "e",   "e",   "e",   "e",   "r5",  "e",   "e",   "r5",  "r5",   "r5"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "s17", "s16", "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",     "e"],
    ["r2",  "e",   "r2",  "e",   "e",   "r2",  "e",   "e",   "e",   "e",   "e",   "r2",  "e",   "e",   "r2",  "r2",   "r2"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "s19", "e",   "e",   "e",   "e",   "e",   "e",     "e"],
    ["s2",  "s20", "s6",  "s30", "e",   "s27", "s17", "s16", "s26", "e",   "e",   "s23", "s25", "s28", "e",   "s24",   "e"],
    ["r22", "e",   "r22", "e",   "e",   "r22", "e",   "e",   "e",   "e",   "e",   "r22", "e",   "e",   "r22", "r22", "r22"],
    ["r23", "e",   "r23", "e",   "e",   "r23", "e",   "e",   "e",   "e",   "e",   "r23", "e",   "e",   "r23", "r23", "r23"],
    ["r25", "e",   "r25", "e",   "e",   "r25", "s31", "e",   "e",   "e",   "e",   "r25", "e",   "e",   "r25", "r25", "r25"],
    ["r24", "e",   "r24", "e",   "e",   "r24", "e",   "e",   "e",   "e",   "e",   "r24", "e",   "e",   "r24", "r24", "r24"],
    ["r36", "e",   "r36", "e",   "e",   "r36", "e",   "e",   "e",   "e",   "e",   "r36", "e",   "e",   "r36", "r36", "r36"],
    ["r27", "e",   "r27", "e",   "e",   "r27", "e",   "e",   "e",   "e",   "e",   "r27", "e",   "e",   "r27", "r27", "r27"],
    ["e",   "e",   "e",   "e",   "s35", "e",   "s17", "s16", "e",   "r28", "s33", "e",   "e",   "e",   "e",   "e",     "e"],
    ["r16", "e",   "r16", "e",   "e",   "r16", "e",   "e",   "e",   "e",   "e",   "r16", "e",   "e",   "r16", "r16", "r16"],
    ["r15", "e",   "r15", "e",   "e",   "r15", "e",   "e",   "e",   "e",   "e",   "r15", "e",   "e",   "r15", "r15", "r15"],
    ["r20", "e",   "r20", "e",   "e",   "r20", "e",   "e",   "e",   "e",   "e",   "r20", "e",   "e",   "r20", "r20", "r20"],
    ["e",   "e",   "e",   "s30", "e",   "e",   "e",   "e",   "e",   "r34", "e",   "e",   "s25", "e",   "e",   "e",     "e"],
    ["r11", "e",   "r11", "e",   "e",   "r11", "e",   "e",   "e",   "e",   "e",   "r11", "e",   "e",   "r11", "r11", "r11"],
    ["s2",  "e",   "s6",  "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",     "e"],
    ["s2",  "e",   "s6",  "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",     "e"],
    ["e",   "e",   "s39", "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "s41", "e",   "e",   "s40",   "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "s42", "e",   "e",   "e",   "e",   "e",   "e",   "e",     "e"],
    ["r9",  "e",   "r9",  "e",   "e",   "r9",  "e",   "e",   "e",   "e",   "e",   "r9",  "s43", "e",   "r9",  "r9",   "r9"],
    ["r26", "e",   "r26", "e",   "e",   "r26", "e",   "e",   "e",   "e",   "e",   "r26", "e",   "e",   "r26", "r26", "r26"],
    ["r14", "e",   "r14", "e",   "e",   "r14", "e",   "e",   "e",   "e",   "e",   "r14", "e",   "e",   "r14", "r14", "r14"],
    ["r7",  "e",   "r7",  "e",   "e",   "r7",  "e",   "e",   "e",   "e",   "e",   "r7",  "e",   "e",   "r7",  "r7",   "r7"],
    ["r8",  "e",   "r8",  "e",   "e",   "r8",  "e",   "e",   "e",   "e",   "e",   "r8",  "e",   "e",   "r8",  "r8",   "r8"],
    ["r6",  "e",   "r6",  "e",   "e",   "r6",  "e",   "e",   "e",   "e",   "e",   "r6",  "e",   "e",   "r6",  "r6",   "r6"],
    ["r19", "e",   "r19", "e",   "e",   "r19", "e",   "e",   "e",   "e",   "e",   "r19", "e",   "e",   "r19", "r19", "r19"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "r31", "e",   "e",   "e",   "e",   "e",   "e",     "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "r29", "e",   "e",   "e",   "e",   "e",   "e",     "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "s44",   "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "r33", "e",   "e",   "s45", "e",   "e",   "e",     "e"],
    ["r17", "e",   "r17", "e",   "e",   "r17", "e",   "e",   "e",   "e",   "e",   "r17", "e",   "e",   "r17", "r17", "r17"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "r30", "e",   "e",   "e",   "e",   "e",   "e",     "e"],
    ["r10", "e",   "r10", "e",   "e",   "r10", "e",   "e",   "e",   "e",   "e",   "r10", "e",   "e",   "r10", "r10", "r10"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "r32", "e",   "e",   "e",   "e",   "e",   "e",     "e"],
    ["r18", "e",   "r18", "e",   "e",   "r18", "e",   "e",   "e",   "e",   "e",   "r18", "e",   "e",   "r18", "r18", "r18"],
]

non_terminal_index = {
    "action":              0,
    "atom":                1,
    "data":                2,
    "datetime":            3,
    "location":            4,
    "location_attribute":  5,
    "location_phenomenon": 6,
    "phrase":              7,
    "position":            8,
    "question":            9,
    "question_body":       10,
}

goto_table = [
    [11, 14, -1, -1, 13, 3,  5,  8,  -1, 9,  12],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [11, 15, -1, -1, 13, 3,  5,  -1, -1, 9,  12],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, 18, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, 22, 29, -1, -1, -1, 21, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, 32, -1, -1, -1, -1, -1, 34, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, 36, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, 37, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, 38, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
]

reduce_symbol_sum = {
    0:  1,
    1:  1,
    2:  1,
    3:  1,
    4:  1,
    5:  1,
    6:  1,
    7:  1,
    8:  1,
    9:  1,
    10: 2,
    11: 1,
    12: 1,
    13: 1,
    14: 3,
    15: 2,
    16: 2,
    17: 3,
    18: 4,
    19: 3,
    20: 2,
    21: 1,
    22: 1,
    23: 2,
    24: 1,
    25: 1,
    26: 2,
    27: 2,
    28: 2,
    29: 3,
    30: 3,
    31: 3,
    32: 4,
    33: 3,
    34: 2,
    35: 1,
    36: 2,
}

reduce_to_non_terminal = {
    0:  "start",
    1:  "action",
    2:  "atom",
    3:  "atom",
    4:  "atom",
    5:  "atom",
    6:  "data",
    7:  "data",
    8:  "data",
    9:  "datetime",
    10: "datetime",
    11: "datetime",
    12: "location",
    13: "location",
    14: "location_attribute",
    15: "location_attribute",
    16: "location_attribute",
    17: "location_attribute",
    18: "location_attribute",
    19: "location_attribute",
    20: "location_phenomenon",
    21: "location_phenomenon",
    22: "phrase",
    23: "phrase",
    24: "position",
    25: "position",
    26: "position",
    27: "question",
    28: "question_body",
    29: "question_body",
    30: "question_body",
    31: "question_body",
    32: "question_body",
    33: "question_body",
    34: "question_body",
    35: "question_body",
    36: "action",
}


def mephisto_question_grammar(token_list):
    import mp_helper
    symbol_stack = []
    stack = [0]
    token_index = 0
    while token_index < len(token_list):
        token = token_list[token_index]
        token_type = token[0]
        now_state = stack[-1]
        operation = action_table[now_state][terminal_index[token_type]]
        operation_flag = operation[0]
        if operation_flag == "e":
            raise Exception("Grammar error: " + " ".join([t[1] for t in token_list]))
        elif operation_flag == "s":
            operation_number = int(operation[1:])
            stack.append(operation_number)
            token_index += 1
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
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = ("lapse", mp_helper.normalize_time_lapse(boson_sentence[0][1]))
                symbol_stack.append(boson_reduce)
            elif operation_number == 2:
                pass
            elif operation_number == 3:
                pass
            elif operation_number == 4:
                pass
            elif operation_number == 5:
                pass
            elif operation_number == 6:
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = mp_helper.normalize_degree(boson_sentence[0][1])
                symbol_stack.append(boson_reduce)
            elif operation_number == 7:
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = int(boson_sentence[0][1])
                symbol_stack.append(boson_reduce)
            elif operation_number == 8:
                pass
            elif operation_number == 9:
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = mp_helper.normalize_date(boson_sentence[0][1])
                symbol_stack.append(boson_reduce)
            elif operation_number == 10:
                boson_sentence = []
                for boson_i in range(2):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = (mp_helper.normalize_date(boson_sentence[0][1]), mp_helper.normalize_time(boson_sentence[1][1]))
                symbol_stack.append(boson_reduce)
            elif operation_number == 11:
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = mp_helper.normalize_time(boson_sentence[0][1])
                symbol_stack.append(boson_reduce)
            elif operation_number == 12:
                pass
            elif operation_number == 13:
                pass
            elif operation_number == 14:
                boson_sentence = []
                for boson_i in range(3):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = ("set", mp_helper.normalize_attribute(boson_sentence[1][1]), boson_sentence[0], boson_sentence[2])
                symbol_stack.append(boson_reduce)
            elif operation_number == 15:
                boson_sentence = []
                for boson_i in range(2):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = ("set", "datetime", boson_sentence[0], boson_sentence[1])
                symbol_stack.append(boson_reduce)
            elif operation_number == 16:
                boson_sentence = []
                for boson_i in range(2):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = ("set", "position", boson_sentence[0], boson_sentence[1])
                symbol_stack.append(boson_reduce)
            elif operation_number == 17:
                boson_sentence = []
                for boson_i in range(3):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = ("set", mp_helper.normalize_attribute(boson_sentence[1][1]), boson_sentence[0], mp_helper.normalize_time(boson_sentence[2][1]))
                symbol_stack.append(boson_reduce)
            elif operation_number == 18:
                boson_sentence = []
                for boson_i in range(4):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = ("set", mp_helper.normalize_attribute(boson_sentence[1][1]), boson_sentence[0], mp_helper.normalize_time(boson_sentence[3][1]))
                symbol_stack.append(boson_reduce)
            elif operation_number == 19:
                boson_sentence = []
                for boson_i in range(3):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = ("set", "datetime", boson_sentence[0], boson_sentence[2])
                symbol_stack.append(boson_reduce)
            elif operation_number == 20:
                boson_sentence = []
                for boson_i in range(2):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = ("event", boson_sentence[0], mp_helper.normalize_phenomenon(boson_sentence[1][1]))
                symbol_stack.append(boson_reduce)
            elif operation_number == 21:
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = ("event", ("!", "!"), mp_helper.normalize_phenomenon(boson_sentence[0][1]))
                symbol_stack.append(boson_reduce)
            elif operation_number == 22:
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = [boson_sentence[0]]
                symbol_stack.append(boson_reduce)
            elif operation_number == 23:
                boson_sentence = []
                for boson_i in range(2):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = boson_sentence[0] + [boson_sentence[1]]
                symbol_stack.append(boson_reduce)
            elif operation_number == 24:
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = mp_helper.normalize_latitude(boson_sentence[0][1])
                symbol_stack.append(boson_reduce)
            elif operation_number == 25:
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = mp_helper.normalize_longitude(boson_sentence[0][1])
                symbol_stack.append(boson_reduce)
            elif operation_number == 26:
                boson_sentence = []
                for boson_i in range(2):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = (mp_helper.normalize_longitude(boson_sentence[0][1]), mp_helper.normalize_latitude(boson_sentence[1][1]))
                symbol_stack.append(boson_reduce)
            elif operation_number == 27:
                boson_sentence = []
                for boson_i in range(2):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = boson_sentence[0]
                symbol_stack.append(boson_reduce)
            elif operation_number == 28:
                boson_sentence = []
                for boson_i in range(2):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = ("get", boson_sentence[0], boson_sentence[1][1])
                symbol_stack.append(boson_reduce)
            elif operation_number == 29:
                boson_sentence = []
                for boson_i in range(3):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = ("geo", mp_helper.normalize_geo(boson_sentence[1][1]), boson_sentence[0], boson_sentence[2])
                symbol_stack.append(boson_reduce)
            elif operation_number == 30:
                boson_sentence = []
                for boson_i in range(3):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = ("metric", mp_helper.normalize_metric(boson_sentence[2][1]), boson_sentence[0], boson_sentence[1])
                symbol_stack.append(boson_reduce)
            elif operation_number == 31:
                boson_sentence = []
                for boson_i in range(3):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = ("metric", mp_helper.normalize_metric(boson_sentence[1][1]), boson_sentence[0], boson_sentence[2])
                symbol_stack.append(boson_reduce)
            elif operation_number == 32:
                boson_sentence = []
                for boson_i in range(4):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = ("indirect", boson_sentence[0], boson_sentence[1][1], boson_sentence[2][1])
                symbol_stack.append(boson_reduce)
            elif operation_number == 33:
                boson_sentence = []
                for boson_i in range(3):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = ("get", boson_sentence[0], mp_helper.normalize_attribute(boson_sentence[1][1]))
                symbol_stack.append(boson_reduce)
            elif operation_number == 34:
                boson_sentence = []
                for boson_i in range(2):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = ("get", boson_sentence[0], "local_time")
                symbol_stack.append(boson_reduce)
            elif operation_number == 35:
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = ("get", ("!", "!"), "local_time")
                symbol_stack.append(boson_reduce)
            elif operation_number == 36:
                boson_sentence = []
                for boson_i in range(2):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = ("move", boson_sentence[1])
                symbol_stack.append(boson_reduce)
            else:
                raise Exception("Invalid reduce number: %d" % operation_number)
        elif operation_flag == "a":
            break
        else:
            raise Exception("Invalid action: %s" % operation)
    return symbol_stack[0]
