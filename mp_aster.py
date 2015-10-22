from mp_location import *
import mp_logic
import mp_configure


class Earth:
    def __init__(self, date=None, time=None, date_sep_string=mp_configure.date_sep_string, time_sep_string=mp_configure.time_sep_string, location_sep_string=mp_configure.location_sep_string, direction_flag=mp_configure.location_direction_flag):
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

    def __str__(self):
        return " ".join([str(self.get_date()), str(self.get_time())])

    def get_by_name(self, name):
        name_object = {
            "date": self.__date,
            "spring_equinox": self.__spring_equinox,
            "autumnal_equinox": self.__autumnal_equinox,
            "declination": self.__declination,
        }
        if name not in name_object:
            return None
        else:
            return name_object[name]

    def only_set_date(self, date):
        if isinstance(date, str):
            self.__date = Date(date, self.__date_sep_string)
        elif isinstance(date, Date):
            self.__date = copy.deepcopy(date)
        else:
            raise Exception("Invalid date type: %s" % str(type(date)))

    def set_date(self, date):
        self.only_set_date(date)
        mp_logic.mp_logic.change_linkage(self, ("earth", "date"))

    def get_date(self):
        return self.__date

    def only_set_time(self, time):
        if isinstance(time, str):
            self.__time = Time(time, self.__time_sep_string)
        elif isinstance(time, Time):
            self.__time = copy.deepcopy(time)
        else:
            raise Exception("Invalid time type: %s" % str(type(time)))

    def set_time(self, time):
        self.only_set_time(time)

    def get_time(self):
        return self.__time

    def set_date_sep_string(self, sep_string):
        self.__date_sep_string = sep_string
        if self.__date is not None:
            self.__date.set_sep_string(sep_string=sep_string)

    def set_time_sep_string(self, sep_string):
        self.__time_sep_string = sep_string
        if self.__time is not None:
            self.__time.set_sep_string(sep_string=sep_string)

    def set_location_sep_string(self, sep_string):
        self.__location_sep_string = sep_string

    def set_direction_flag(self, direction_flag):
        self.__direction_flag = direction_flag

    def get_date_sep_string(self):
        return self.__date_sep_string

    def get_time_sep_string(self):
        return self.__time_sep_string

    def get_location_sep_string(self):
        return self.__location_sep_string

    def get_direction_flag(self):
        return self.__direction_flag

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
        mp_logic.mp_logic.change_linkage(self, "date")

    def forward_month(self, m):
        self.__date.forward_month(m)
        mp_logic.mp_logic.change_linkage(self, "date")

    def forward_year(self, y):
        self.__date.forward_year(y)
        mp_logic.mp_logic.change_linkage(self, "date")

    def backward_day(self, d):
        self.__date.backward_day(d)
        mp_logic.mp_logic.change_linkage(self, "date")

    def backward_month(self, m):
        self.__date.backward_month(m)
        mp_logic.mp_logic.change_linkage(self, "date")

    def backward_year(self, y):
        self.__date.backward_year(y)
        mp_logic.mp_logic.change_linkage(self, "date")

    def set_spring_equinox(self, date):
        self.__spring_equinox = date

    def get_spring_equinox(self):
        return self.__spring_equinox

    def set_autumnal_equinox(self, date):
        self.__autumnal_equinox = date

    def get_autumnal_equinox(self):
        return self.__autumnal_equinox

    def set_declination(self, latitude):
        self.__declination = latitude

    def get_declination(self):
        return self.__declination
