import mp_location
import mp_date_time
import mp_logic
import mp_configure


class Earth:
    def __init__(self, date=None, time=None, date_sep_string=mp_configure.date_sep_string, time_sep_string=mp_configure.time_sep_string, location_sep_string=mp_configure.location_sep_string, direction_flag=mp_configure.location_direction_flag):
        self.__date_sep_string = date_sep_string
        self.__time_sep_string = time_sep_string
        self.__location_sep_string = location_sep_string
        self.__direction_flag = direction_flag
        self.__date = None
        self.__time = None
        self.__spring_equinox = None
        self.__autumnal_equinox = None
        self.__declination = None
        self.__bind_location = []
        self.__name_object_get = {
            "date": self.get_date,
            "time": self.get_time,
            "spring_equinox": self.get_spring_equinox,
            "autumnal_equinox": self.get_autumnal_equinox,
            "declination": self.get_declination,
            "bind_location": self.get_bind_location,
        }
        self.__name_object_set = {
            "date": self.set_date,
            "time": self.set_time,
            "spring_equinox": self.set_spring_equinox,
            "autumnal_equinox": self.set_autumnal_equinox,
            "declination": self.set_declination,
            "bind_location": self.add_bind_location
        }
        self.__static_attribute = {
            "date": False,
            "time": False,
            "spring_equinox": False,
            "autumnal_equinox": False,
            "declination": False,
            "bind_location": False
        }
        if date is not None:
            self.set_date(date)
        if time is not None:
            self.set_time(time)

    def __str__(self):
        return " ".join([str(self.get_date()), str(self.get_time())])

    def __repr__(self):
        return self.__str__()

    def get_by_name(self, name):
        if name not in self.__name_object_get:
            return None
        else:
            return self.__name_object_get[name]()

    def set_by_name(self, name, data):
        if name in self.__name_object_set:
            self.__name_object_set[name](data)

    def static_attribute(self, name):
        if name not in self.__static_attribute:
            return False
        return self.__static_attribute[name]

    def set_static_attribute(self, name):
        if name in self.__static_attribute:
            self.__static_attribute[name] = True

    def unset_static_attribute(self, name):
        if name in self.__static_attribute:
            self.__static_attribute[name] = False

    def get_available_name_list(self):
        available_name_list = []
        name_list = ["name", "spring_equinox", "autumnal_equinox", "declination"]
        for name in name_list:
            if self.get_by_name(name):
                available_name_list.append(name)
        return available_name_list

    def only_set_date(self, date):
        self.__date = mp_date_time.Date(date)

    def set_date(self, date):
        self.only_set_date(date)
        mp_logic.mp_logic.change_linkage(self, ("earth", "date"))

    def get_date(self):
        return self.__date

    def only_set_time(self, time):
        self.__time = mp_date_time.Time(time)

    def set_time(self, time):
        self.only_set_time(time)
        mp_logic.mp_logic.change_linkage(self, ("earth", "time"))

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
        mp_logic.mp_logic.change_linkage(self, ("earth", "time"))

    def forward_minute(self, m):
        self.__time.forward_second(m * 60)
        mp_logic.mp_logic.change_linkage(self, ("earth", "time"))

    def forward_hour(self, h):
        self.__time.forward_second(h * 3600)
        mp_logic.mp_logic.change_linkage(self, ("earth", "time"))

    def backward_second(self, s):
        overflow = self.__time.backward_second(s)
        if overflow < 0:
            self.backward_day(-overflow)
        mp_logic.mp_logic.change_linkage(self, ("earth", "time"))

    def backward_minute(self, m):
        self.__time.backward_second(m * 60)
        mp_logic.mp_logic.change_linkage(self, ("earth", "time"))

    def backward_hour(self, h):
        self.__time.backward_second(h * 3600)
        mp_logic.mp_logic.change_linkage(self, ("earth", "time"))

    def forward_day(self, d):
        self.__date.forward_day(d)
        mp_logic.mp_logic.change_linkage(self, ("earth", "date"))

    def forward_month(self, m):
        self.__date.forward_month(m)
        mp_logic.mp_logic.change_linkage(self, ("earth", "date"))

    def forward_year(self, y):
        self.__date.forward_year(y)
        mp_logic.mp_logic.change_linkage(self, ("earth", "date"))

    def backward_day(self, d):
        self.__date.backward_day(d)
        mp_logic.mp_logic.change_linkage(self, ("earth", "date"))

    def backward_month(self, m):
        self.__date.backward_month(m)
        mp_logic.mp_logic.change_linkage(self, ("earth", "date"))

    def backward_year(self, y):
        self.__date.backward_year(y)
        mp_logic.mp_logic.change_linkage(self, ("earth", "date"))

    def only_set_spring_equinox(self, date):
        self.__spring_equinox = mp_date_time.Date(date)

    def set_spring_equinox(self, date):
        self.only_set_spring_equinox(date)

    def get_spring_equinox(self):
        return self.__spring_equinox

    def only_set_autumnal_equinox(self, date):
        self.__autumnal_equinox = mp_date_time.Date(date)

    def set_autumnal_equinox(self, date):
        self.only_set_autumnal_equinox(date)

    def get_autumnal_equinox(self):
        return self.__autumnal_equinox

    def only_set_declination(self, latitude):
        self.__declination = mp_location.Latitude(latitude)

    def set_declination(self, latitude):
        self.only_set_declination(latitude)
        mp_logic.mp_logic.change_linkage(self, ("earth", "declination"))

    def get_declination(self):
        return self.__declination

    def add_bind_location(self, location, from_location=False):
        self.__bind_location.append(location)
        if not from_location:
            location.set_bind_earth(self, from_earth=True)

    def get_bind_location(self):
        return self.__bind_location
