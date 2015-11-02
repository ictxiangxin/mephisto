import re
import mp_data

token_tuple = [
    ("phenomenon",      r"日影最短|极昼|极夜|圆月"),
    ("attribute",       r"日出|日落|昼长|夜长|正午太阳高度"),
    ("time",            r"[0-9]+(时|点)[0-9]+分|[0-9]+(时|点)|[0-9]+:[0-9]+"),
    ("time_literal",    r"时间|地区时|区时|地方时"),
    ("time_zone",       r"(东|西)[一二三四五六七八1-8]{1}区"),
    ("date",            r"[0-9]+月[0-9]+日|[0-9]+年[0-9]+月[0-9]+日"),
    ("longitude",       r"[0-9\.]+°([0-9\.]+′){0,1}(E|W)"),
    ("latitude",        r"[0-9\.]+°([0-9\.]+′){0,1}(S|N)"),
    ("earth_attr",      r"春分|秋分"),
    ("earth_name",      r"北极点|南极点|北极圈|南极圈|北回归线|南回归线"),
    ("geo_question",    r"位于？|接近？|坐标？"),
    ("metric_question", r"范围？|距离？"),
    ("normal_question", r"是？|为？"),
    ("judge",           r"正确|错误"),
    ("city",            r"|".join(list(mp_data.mp_city_to_coordinate))),
    ("invalid",         r"."),
]

token_regular = "|".join("(?P<%s>%s)" % pair for pair in token_tuple)


def tokenize(string):
    token_list = list()
    for one_token in re.finditer(token_regular, string):
        token_class = one_token.lastgroup 
        token_string = one_token.group(token_class)
        if token_class == "invalid":
            pass
        else:
            token_list.append((token_class, token_string))
    token_list.append(("$", ""))
    return token_list
