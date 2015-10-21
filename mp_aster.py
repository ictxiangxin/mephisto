from mp_date_time import *
from mp_location import *


class Earth:
    def __init__(self, date=None, time=None, date_sep_string="-", time_sep_string=":", location_sep_string=".", direction_flag=(("E", "W"), ("N", "S"))):
        self.__date_sep_string = date_sep_string
        self.__time_sep_string = time_sep_string
        self.__location_sep_string = location_sep_string
        self.__direction_flag = direction_flag
        self.__spring_equinox = None
        self.__autumnal_equinox = None
        self.__declination = None
        if date is not None:
            self.set_date(date)
        else:
            self.__date = None
        if time is not None:
            self.set_time(time)
        else:
            self.__time = None

    def compute_date_time_related_attribute(self):
        self.__spring_equinox = self._compute_spring_equinox()
        self.__autumnal_equinox = self._compute_autumnal_equinox()
        self.__declination = self._compute_declination()

    def set_date(self, date):
        if isinstance(date, str):
            self.__date = Date(date, self.__date_sep_string)
            self.compute_date_time_related_attribute()
        elif isinstance(date, Date):
            self.__date = copy.deepcopy(date)
            self.compute_date_time_related_attribute()
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
        self.compute_date_time_related_attribute()

    def forward_month(self, m):
        self.__date.forward_month(m)
        self.compute_date_time_related_attribute()

    def forward_year(self, y):
        self.__date.forward_year(y)
        self.compute_date_time_related_attribute()

    def backward_day(self, d):
        self.__date.backward_day(d)
        self.compute_date_time_related_attribute()

    def backward_month(self, m):
        self.__date.backward_month(m)
        self.compute_date_time_related_attribute()

    def backward_year(self, y):
        self.__date.backward_year(y)
        self.compute_date_time_related_attribute()

    def _compute_spring_equinox(self):
        y, m, d = self.__date.get_date_tuple()
        yy = y % 100
        d = int(yy * 0.2422 + 20.646) - int(yy / 4)
        m = 3
        return Date(self.__date_sep_string.join([str(y), str(m), str(d)]))

    def get_spring_equinox(self):
        return self.__spring_equinox

    def _compute_autumnal_equinox(self):
        date = self._compute_spring_equinox()
        date.forward_day(186)
        return date

    def get_autumnal_equinox(self):
        return self.__autumnal_equinox

    def _compute_declination(self):
        y, m, d = self.__date.get_date_tuple()
        ordinal_number = month_to_number(m) + d
        b = 2 * math.pi * (ordinal_number - 1) / 365
        delta = 0.006918
        delta -= 0.399912 * math.cos(b) + 0.006758 * math.cos(2 * b) + 0.002697 * math.cos(3 * b)
        delta += 0.070257 * math.sin(b) + 0.000907 * math.sin(2 * b) + 0.001480 * math.sin(3 * b)
        return Latitude(int(648000 / math.pi * delta),
                        sep_string=self.__location_sep_string, direction_flag=self.__direction_flag[-1])

    def get_declination(self):
        return self.__declination