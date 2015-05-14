__author__ = 'ict'

import re

# L -> E '->' A : F
# E -> '(' G ')' | A
# G -> A ',' G | A
# A -> name '.' name
# F -> A '(' U ')' | A '(' ')'
# U -> name ',' U | name


class LogicLanguage:
    def __init__(self, filename):
        token_tuple = [
            ("NAME",      r"[_a-zA-Z]+"),
            ("MEMBER",    r"\."),
            ("BRACKET_L", r"\("),
            ("BRACKET_R", r"\)"),
            ("TOWARD",    r"\->"),
            ("FUNCTION",  r":"),
            ("END",       r";"),
            ("COMMA",     r","),
            ("SKIP",      r"[ \t]+"),
            ("NEWLINE",   r"\n|\r\n"),
            ("INVALID",   r"."),
        ]
        self.__token_regrex = "|".join("(?P<%s>%s)" % pair for pair in token_tuple)
        self.__action_table = {
            1: {
                "TOWARD":    "s5",
                "BRACKET_L": "s15",
                "NAME":      "s22",
            },
            2: {
                "TOWARD": "s3",
            },
            3: {
                "NAME": "s25",
            },
            4: {
                "FUNCTION": "s5",
            },
            5: {
                "NAME": "s25",
            },
            6: {
                "END": "s7",
            },
            7: {
                "$": "accept",
            },
            8: {
                "BRACKET_L": "s9",
            },
            9: {
                "NAME":      "s10",
                "BRACKET_R": "s26"
            },
            10: {
                "BRACKET_R": "r9",
                "COMMA": "s11",
            },
            11: {
                "NAME": "s10",
            },
            12: {
                "BRACKET_R": "r8",
            },
            13: {
                "BRACKET_R": "s14",
            },
            14: {
                "END": "r7",
            },
            15: {
                "NAME": "s25",
            },
            16: {
                "BRACKET_R": "s18",
            },
            17: {
                "BRACKET_R": "r5",
                "COMMA":     "s19",
            },
            18: {
                "TOWARD": "r2",
            },
            19: {
                "NAME": "s25",
            },
            20: {
                "BRACKET_R": "r4",
            },
            21: {
                "TOWARD": "r3",
                "BRACKET_R": "r5",
                "COMMA": "s19",
            },
            22: {
                "BRACKET_L": "s9",
                "BRACKET_R": "r9",
                "COMMA":     "s11",
                "MEMBER":    "s23",
            },
            23: {
                "NAME": "s24",
            },
            24: {
                "FUNCTION":  "r6",
                "COMMA":     "r6",
                "TOWARD":    "r6",
                "BRACKET_L": "r6",
                "BRACKET_R": "r6",
            },
            25: {
                "MEMBER": "s23",
            },
            26: {
                "END": "r10",
            }
        }
        self.__goto_table = {
            1: {
                "E": 2,
                "A": 21,
            },
            3: {
                "A": 4,
            },
            5: {
                "A": 8,
                "F": 6,
            },
            9: {
                "U": 13,
            },
            11: {
                "U": 12,
            },
            15: {
                "A": 17,
                "G": 16,
            },
            19: {
                "A": 17,
                "G": 20,
            },
        }
        self.__reduce_number = {
            2:  3,
            3:  1,
            4:  3,
            5:  1,
            6:  3,
            7:  4,
            8:  3,
            9:  1,
            10: 3,
        }
        self.__reduce_table = {
            2:  "E",
            3:  "E",
            4:  "G",
            5:  "G",
            6:  "A",
            7:  "F",
            8:  "U",
            9:  "U",
            10: "F",
        }
        self.__filename = ""
        self.parse(filename)

    def parse(self, filename):
        self.__filename = filename
        with open(filename, "r") as fp:
            token_list = self.tokenize(fp.read().lower())
            tree_list = self.grammar_slr(token_list)
            for tree in tree_list:
                print(tree)

    def tokenize(self, string):
        token_list = list()
        line_number = 1
        temp_list = list()
        for one_token in re.finditer(self.__token_regrex, string):
            token_class = one_token.lastgroup
            token_string = one_token.group(token_class)
            if token_class == "SKIP":
                pass
            elif token_class == "NEWLINE":
                temp_list.append(("$", ""))
                token_list.append(temp_list)
                temp_list = list()
                line_number += 1
            elif token_class == "INVALID":
                raise RuntimeError("[Line: %d] Invalid token: %s" % (line_number, token_string))
            else:
                temp_list.append((token_class, token_string))
        return token_list

    def grammar_slr(self, token_list):
        tree_list = []
        for line in token_list:
            stack = [1]
            grammar_tree = []
            token_index = 0
            while token_index < len(line):
                op_dict = self.__action_table[stack[-1]]
                token = line[token_index]
                if token[0] not in op_dict:
                    raise Exception("Grammar error: " + " ".join([e[1] for e in line]))
                op = op_dict[token[0]]
                if op[0] == "s":
                    stack.append(int(op[1:]))
                    grammar_tree.append(token)
                    token_index += 1
                elif op[0] == "r":
                    op_number = int(op[1:])
                    if op_number not in self.__reduce_number:
                        raise Exception("SLR error no such reduce: %d" % op_number)
                    reduce_number = self.__reduce_number[op_number]
                    reduce_symbol = self.__reduce_table[op_number]
                    temp_list = list()
                    for i in range(reduce_number):
                        temp_list.append(grammar_tree.pop())
                        stack.pop()
                    grammar_tree.append((reduce_symbol, temp_list))
                    stack.append(self.__goto_table[stack[-1]][reduce_symbol])
                elif op[0] == "a":
                    tree_list.append(("root", grammar_tree))
                    break
        return tree_list