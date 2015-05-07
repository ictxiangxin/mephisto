__author__ = 'ict'

from mp_date_time import *


class Earth:
    def __init__(self, date_string, time_string, date_sep_string="-", time_sep_string=":"):
        self.__date = Date(date_string, date_sep_string)
        self.__time = Time(time_string, time_sep_string)
        self.__date_sep_string = date_sep_string
        self.__time_sep_string = time_sep_string

    def get_date_string(self):
        return self.__date.get_date_string()

    def get_date_number(self):
        return self.__date.get_date_number()

    def get_time_string(self):
        return self.__time.get_time_string()

    def get_time_number(self):
        return self.__time.get_time_number()

    def set_date_sep_string(self, sep_string):
        self.__date.set_sep_string(sep_string=sep_string)

    def set_time_sep_string(self, sep_string):
        self.__time.set_sep_string(sep_string=sep_string)

    def get_date_sep_string(self):
        return self.__date.get_sep_string()

    def get_time_sep_string(self):
        return self.__time.get_sep_string()

    def forward_second(self, s):
        self.__time.forward_second(s)

    def forward_minute(self, m):
        self.__time.forward_minute(m)

    def forward_hour(self, h):
        self.__time.forward_hour(h)

    def forward_day(self, d):
        self.__date.forward_day(d)

    def forward_month(self, m):
        self.__date.forward_month(m)

    def forward_year(self, y):
        self.__date.forward_year(y)

    def backward_second(self, s):
        self.__time.backward_second(s)

    def backward_minute(self, m):
        self.__time.backward_minute(m)

    def backward_hour(self, h):
        self.__time.backward_hour(h)

    def backward_day(self, d):
        self.__date.backward_day(d)

    def backward_month(self, m):
        self.__date.backward_month(m)

    def backward_year(self, y):
        self.__date.backward_year(y)

    def spring_equinox(self):
        y, m, d = self.__date.get_date_tuple()
        yy = y % 100
        d = int(yy * 0.2422 + 20.646) - int(yy / 4)
        m = 3
        return Date(self.__date_sep_string.join([str(y), str(m), str(d)]))

    def autumnal_equinox(self):
        date = self.spring_equinox()
        date.forward_day(186)
        return date