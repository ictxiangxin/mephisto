__author__ = 'ict'


def is_leap_year(y):
    leap_year = False
    if y % 100 == 0:
        if y % 400 == 0:
            leap_year = True
    elif y % 4 == 0:
        leap_year = True
    return leap_year


def year_to_number(y):
    number = 0
    for i in range(1, y):
        if is_leap_year(i):
            number += 366
        else:
            number += 365
    return number


def month_days_number(m, leap_year=False):
    if m == 1:
        return 31
    elif m == 2:
        if leap_year:
            return 29
        else:
            return 28
    elif m == 3:
        return 31
    elif m == 4:
        return 30
    elif m == 5:
        return 31
    elif m == 6:
        return 30
    elif m == 7:
        return 31
    elif m == 8:
        return 31
    elif m == 9:
        return 30
    elif m == 10:
        return 31
    elif m == 11:
        return 30
    elif m == 12:
        return 31
    raise Exception("Invalid month: %d" % m)


def month_to_number(m, leap_year=False):
    number = 0
    for i in range(1, m):
        number += month_days_number(i, leap_year)
    return number


def date_string_to_number(date_string, sep_string="-"):
    y, m, d = [int(elem) for elem in date_string.split(sep_string)]
    if y < 1 or m < 1 or m > 12:
        raise Exception("Invalid date: %s" % date_string)
    leap_year = is_leap_year(y)
    year_number = year_to_number(y)
    month_number = month_to_number(m, leap_year)
    if d < 1 or d > month_days_number(m, leap_year):
        raise Exception("Invalid date: %s" % date_string)
    return year_number + month_number + d


def number_to_date_string(number, sep_string="-"):
    y, m, d = 1, 1, 0
    leap_year = False
    while (not leap_year and number > 365) or (leap_year and number > 366):
        if leap_year:
            number -= 366
        else:
            number -= 365
        y += 1
        leap_year = is_leap_year(y)
    while number > 0:
        m_days = month_days_number(m, leap_year)
        if number > m_days:
            number -= m_days
            m += 1
        else:
            d = number
            break
    return sep_string.join([str(y), str(m), str(d)])


def time_string_to_number(time_string, sep_string=":"):
    h, m, s = [int(elem) for elem in time_string.split(sep_string)]
    if h > 24 or m > 60 or s > 60:
        raise Exception("Invalid time: %s" % time_string)
    return h * 3600 + m * 60 + s


def number_to_time_string(number, sep_string=":"):
    if number > 86400:
        raise Exception("Invalid time number: %d" % number)
    h = int(number / 3600)
    number %= 3600
    m = int(number / 60)
    s = number % 60
    return sep_string.join([str(h), str(m), str(s)])


def date_string_distance(date_string_a, date_string_b, sep_string="-"):
    return abs(date_string_to_number(date_string_a, sep_string=sep_string) -
               date_string_to_number(date_string_b, sep_string=sep_string))


def time_string_distance(time_string_a, time_string_b, sep_string=":"):
    return abs(time_string_to_number(time_string_a, sep_string=sep_string) -
               time_string_to_number(time_string_b, sep_string=sep_string))


class Date:
    def __init__(self, date_string, sep_string="-"):
        self.__date_number = 0
        self.__date_string = sep_string.join(["1"] * 3)
        self.__sep_string = sep_string
        if len(date_string) != 0:
            self.set_date_string(date_string)

    def get_date_tuple(self):
        return (int(elem) for elem in self.__date_string.split(self.__sep_string))

    def set_date_string(self, date_string):
        self.__date_number = date_string_to_number(date_string, sep_string=self.__sep_string)
        self.__date_string = date_string

    def get_date_string(self):
        return self.__date_string

    def set_date_number(self, date_number):
        self.__date_string = number_to_date_string(date_number, sep_string=self.__sep_string)
        self.__date_number = date_number

    def get_date_number(self):
        return self.__date_number

    def set_sep_string(self, sep_string):
        self.__sep_string = sep_string
        self.__date_string = number_to_date_string(self.__date_number, sep_string=self.__sep_string)

    def get_sep_string(self):
        return self.__sep_string

    def forward_day(self, day):
        self.__date_number += day
        self.__date_string = number_to_date_string(self.__date_number, sep_string=self.__sep_string)

    def backward_day(self, day):
        if self.__date_number < day:
            raise Exception("No more days: %d" % self.__date_number)
        self.__date_number -= day
        self.__date_string = number_to_date_string(self.__date_number, sep_string=self.__sep_string)

    def forward_month(self, month):
        y, m, d = [int(elem) for elem in self.__date_string.split(self.__sep_string)]
        m += month
        y += int((m - 1) / 12)
        m = (m - 1) % 12 + 1
        self.__date_string = self.__sep_string.join([str(y), str(m), str(d)])
        self.__date_number = date_string_to_number(self.__date_string, sep_string=self.__sep_string)

    def backward_month(self, month):
        y, m, d = [int(elem) for elem in self.__date_string.split(self.__sep_string)]
        m += (y - 1) * 12
        if m < month:
            raise Exception("No more month: %d" % m)
        m -= month
        y = int((m - 1) / 12) + 1
        m = (m - 1) % 12 + 1
        self.__date_string = self.__sep_string.join([str(y), str(m), str(d)])
        self.__date_number = date_string_to_number(self.__date_string, sep_string=self.__sep_string)

    def forward_year(self, year):
        y, m, d = [int(elem) for elem in self.__date_string.split(self.__sep_string)]
        y += year
        self.__date_string = self.__sep_string.join([str(y), str(m), str(d)])
        self.__date_number = date_string_to_number(self.__date_string, sep_string=self.__sep_string)

    def backward_year(self, year):
        y, m, d = [int(elem) for elem in self.__date_string.split(self.__sep_string)]
        if y < year:
            raise Exception("No more year: %d" % y)
        y -= year
        self.__date_string = self.__sep_string.join([str(y), str(m), str(d)])
        self.__date_number = date_string_to_number(self.__date_string, sep_string=self.__sep_string)


class Time:
    def __init__(self, time_string, sep_string=":"):
        self.__time_number = 0
        self.__time_string = sep_string.join(["0"] * 3)
        self.__sep_string = sep_string
        if len(time_string) != 0:
            self.set_time_string(time_string)

    def get_time_tuple(self):
        return (int(elem) for elem in self.__time_string.split(self.__sep_string))

    def set_time_string(self, time_string):
        self.__time_number = time_string_to_number(time_string, sep_string=self.__sep_string)
        self.__time_string = time_string

    def get_time_string(self):
        return self.__time_string

    def set_time_number(self, time_number):
        if time_number > 86400:
            raise Exception("Invalid time number: %d" % time_number)
        self.__time_string = number_to_time_string(time_number, sep_string=self.__sep_string)
        self.__time_number = time_number

    def get_time_number(self):
        return self.__time_number

    def set_sep_string(self, sep_string):
        self.__sep_string = sep_string
        self.__time_string = number_to_time_string(self.__time_number, sep_string=self.__sep_string)

    def get_sep_string(self):
        return self.__sep_string

    def forward_second(self, second):
        self.__time_number += second
        self.__time_string = number_to_time_string(self.__time_number, sep_string=self.__sep_string)

    def backward_second(self, second):
        if self.__time_number < second:
            raise Exception("No more seconds: %d" % self.__time_number)
        self.__time_number -= second
        self.__time_string = number_to_time_string(self.__time_number, sep_string=self.__sep_string)

    def forward_minute(self, minute):
        h, m, s = [int(elem) for elem in self.__time_string.split(self.__sep_string)]
        m += minute
        h += int(m / 60)
        m %= 60
        self.__time_string = self.__sep_string.join([str(h), str(m), str(s)])
        self.__time_number = time_string_to_number(self.__time_string, sep_string=self.__sep_string)

    def backward_minute(self, minute):
        h, m, s = [int(elem) for elem in self.__time_string.split(self.__sep_string)]
        m += h * 60
        if m < minute:
            raise Exception("No more minutes: %d" % m)
        m -= minute
        h = int(m / 60)
        m %= 60
        self.__time_string = self.__sep_string.join([str(h), str(m), str(s)])
        self.__time_number = time_string_to_number(self.__time_string, sep_string=self.__sep_string)

    def forward_hour(self, hour):
        h, m, s = [int(elem) for elem in self.__time_string.split(self.__sep_string)]
        h += hour
        self.__time_string = self.__sep_string.join([str(h), str(m), str(s)])
        self.__time_number = time_string_to_number(self.__time_string, sep_string=self.__sep_string)

    def backward_hour(self, hour):
        h, m, s = [int(elem) for elem in self.__time_string.split(self.__sep_string)]
        if h < hour:
            raise Exception("No more hour: %d" % h)
        h -= hour
        self.__time_string = self.__sep_string.join([str(h), str(m), str(s)])
        self.__time_number = time_string_to_number(self.__time_string, sep_string=self.__sep_string)