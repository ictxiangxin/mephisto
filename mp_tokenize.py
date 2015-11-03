import re
import mp_data

token_tuple = [
    ("phenomenon",      r"日影最短|极昼|极夜|圆月"),
    ("attribute",       r"经度|纬度|经纬度|昼长|夜长|正午太阳高度"),
    ("time_attribute",  r"日出|日落"),
    ("time",            r"[0-9]+(时|点)([0-9]+分){0,1}([0-9]+秒){0,1}|[0-9]{1,2}:[0-9]{1,2}(:[0-9]{1,2}){0,1}"),
    ("time_lapse",      r"[0-9]+小时([0-9]+分){0,1}([0-9]+秒){0,1}"),
    ("time_literal",    r"时间|地区时|区时|地方时"),
    ("time_zone",       r"(东|西)[一二三四五六七八1-8]{1}区"),
    ("date",            r"([0-9]+年){0,1}[0-9]+月[0-9]+日"),
    ("longitude",       r"[0-9\.]+°([0-9\.]+′){0,1}([0-9\.]+″){0,1}(E|W)"),
    ("latitude",        r"[0-9\.]+°([0-9\.]+′){0,1}([0-9\.]+″){0,1}(S|N)"),
    ("degree",          r"[0-9\.]+°([0-9\.]+′){0,1}([0-9\.]+″){0,1}"),
    ("number",          r"[0-9]+"),
    ("earth_attr",      r"春分|秋分"),
    ("earth_name",      r"北极点|南极点|北极圈|南极圈|北回归线|南回归线"),
    ("geo",             r"位于|越过|抵达"),
    ("metric",          r"距离"),
    ("normal_question", r"是？|为？|？"),
    ("judge",           r"正确|错误"),
    ("city",            r"|".join(list(mp_data.mp_city_to_coordinate))),
    ("anonymous",       r"[a-zA-Z甲乙丙丁戊己庚辛壬癸][点地]"),
    ("separator",       r"[，。；]"),
    ("invalid",         r"."),
]

token_regular = "|".join("(?P<%s>%s)" % pair for pair in token_tuple)


def tokenize(string):
    token_list = list()
    current_class = None
    for one_token in re.finditer(token_regular, string):
        token_class = one_token.lastgroup 
        token_string = one_token.group(token_class)
        if token_class == "invalid":
            pass
        else:
            if current_class is None and token_class == "separator":
                continue
            if token_class == current_class:
                token_list.pop()
            else:
                current_class = token_class
            token_list.append((token_class, token_string))
    token_list.append(("$", ""))
    return token_list
