__author__ = 'ict'

import copy
from mp_date_time import *


class Earth:
    def __init__(self, date=None, time=None, date_sep_string="-", time_sep_string=":"):
        self.__date_sep_string = date_sep_string
        self.__time_sep_string = time_sep_string
        self.__spring_equinox = None
        self.__autumnal_equinox = None
        if date is not None:
            self.set_date(date)
        else:
            self.__date = None
        if time is not None:
            self.set_time(time)
        else:
            self.__time = None

    def set_date(self, date):
        if isinstance(date, str):
            self.__date = Date(date, self.__date_sep_string)
            self.__spring_equinox = self.compute_spring_equinox()
            self.__autumnal_equinox = self.compute_autumnal_equinox()
        elif isinstance(date, Date):
            self.__date = copy.deepcopy(date)
            self.__spring_equinox = self.compute_spring_equinox()
            self.__autumnal_equinox = self.compute_autumnal_equinox()
        else:
            raise Exception("Invalid date type: %s" % str(type(date)))

    def get_date(self):
        return self.__date

    def set_time(self, time):
        if isinstance(time, str):
            self.__time = Time(time, self.__time_sep_string)
        elif isinstance(time, Time):
            self.__time = copy.deepcopy(time)
        else:
            raise Exception("Invalid time type: %s" % str(type(time)))

    def get_time(self):
        return self.__time

    def set_date_sep_string(self, sep_string):
        self.__date.set_sep_string(sep_string=sep_string)

    def set_time_sep_string(self, sep_string):
        self.__time.set_sep_string(sep_string=sep_string)

    def get_date_sep_string(self):
        return self.__date.get_sep_string()

    def get_time_sep_string(self):
        return self.__time.get_sep_string()

    def forward_second(self, s):
        overflow = self.__time.forward_second(s)
        if overflow > 0:
            self.forward_day(overflow)

    def forward_minute(self, m):
        self.__time.forward_second(m * 60)

    def forward_hour(self, h):
        self.__time.forward_second(h * 3600)

    def backward_second(self, s):
        overflow = self.__time.backward_second(s)
        if overflow < 0:
            self.backward_day(-overflow)

    def backward_minute(self, m):
        self.__time.backward_second(m * 60)

    def backward_hour(self, h):
        self.__time.backward_second(h * 3600)

    def forward_day(self, d):
        self.__date.forward_day(d)
        self.__spring_equinox = self.compute_spring_equinox()
        self.__autumnal_equinox = self.compute_autumnal_equinox()

    def forward_month(self, m):
        self.__date.forward_month(m)
        self.__spring_equinox = self.compute_spring_equinox()
        self.__autumnal_equinox = self.compute_autumnal_equinox()

    def forward_year(self, y):
        self.__date.forward_year(y)
        self.__spring_equinox = self.compute_spring_equinox()
        self.__autumnal_equinox = self.compute_autumnal_equinox()

    def backward_day(self, d):
        self.__date.backward_day(d)
        self.__spring_equinox = self.compute_spring_equinox()
        self.__autumnal_equinox = self.compute_autumnal_equinox()

    def backward_month(self, m):
        self.__date.backward_month(m)
        self.__spring_equinox = self.compute_spring_equinox()
        self.__autumnal_equinox = self.compute_autumnal_equinox()

    def backward_year(self, y):
        self.__date.backward_year(y)
        self.__spring_equinox = self.compute_spring_equinox()
        self.__autumnal_equinox = self.compute_autumnal_equinox()

    def compute_spring_equinox(self):
        y, m, d = self.__date.get_date_tuple()
        yy = y % 100
        d = int(yy * 0.2422 + 20.646) - int(yy / 4)
        m = 3
        return Date(self.__date_sep_string.join([str(y), str(m), str(d)]))

    def compute_autumnal_equinox(self):
        date = self.compute_spring_equinox()
        date.forward_day(186)
        return date