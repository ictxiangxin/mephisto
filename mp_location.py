import math
import mp_date_time
import mp_aster
import mp_logic
import mp_configure


def longitude_string_to_number(longitude_string, sep_string=mp_configure.location_sep_string, direction_flag=mp_configure.location_direction_flag[1]):
    direction = longitude_string[-1]
    longitude_string = longitude_string[:-1]
    d, m, s = [int(elem) for elem in longitude_string.split(sep_string)]
    if d > 180 or m > 60 or s > 60 or (d == 180 and (m > 0 or s > 0)):
        raise Exception("Invalid longitude: %s" % longitude_string)
    number = d * 3600 + 60 * m + s
    if direction == direction_flag[0]:
        return number
    elif direction == direction_flag[-1]:
        return -number
    raise Exception("Invalid direction flag: %s" % direction)


def number_to_longitude_string(number, sep_string=mp_configure.location_sep_string, direction_flag=mp_configure.location_direction_flag[0]):
    if number > 0:
        direction = direction_flag[0]
    else:
        direction = direction_flag[-1]
        number = -number
    if number > 648000:
        raise Exception("Invalid longitude number: %d" % number)
    d = int(number / 3600)
    number %= 3600
    m = int(number / 60)
    s = number % 60
    return sep_string.join([str(d), str(m), str(s)]) + direction


def latitude_string_to_number(latitude_string, sep_string=mp_configure.location_sep_string, direction_flag=mp_configure.location_direction_flag[1]):
    direction = latitude_string[-1]
    latitude_string = latitude_string[:-1]
    d, m, s = [int(elem) for elem in latitude_string.split(sep_string)]
    if d > 90 or m > 60 or s > 60 or (d == 90 and (m > 0 or s > 0)):
        raise Exception("Invalid latitude: %s" % latitude_string)
    number = d * 3600 + 60 * m + s
    if direction == direction_flag[0]:
        return number
    elif direction == direction_flag[-1]:
        return -number
    raise Exception("Invalid direction flag: %s" % direction)


def number_to_latitude_string(number, sep_string=mp_configure.location_sep_string, direction_flag=mp_configure.location_direction_flag[1]):
    if number > 0:
        direction = direction_flag[0]
    else:
        direction = direction_flag[-1]
        number = -number
    if number > 324000:
        raise Exception("Invalid latitude number: %d" % number)
    d = int(number / 3600)
    number %= 3600
    m = int(number / 60)
    s = number % 60
    return sep_string.join([str(d), str(m), str(s)]) + direction


def longitude_number_distance(longitude_number_a, longitude_number_b):
    return abs(longitude_number_a - longitude_number_b) % 1296000


def longitude_string_distance(longitude_string_a, longitude_string_b, sep_string=mp_configure.location_sep_string, direction_flag=mp_configure.location_direction_flag[0]):
    longitude_number_a = longitude_string_to_number(longitude_string_a, sep_string=sep_string, direction_flag=direction_flag)
    longitude_number_b = longitude_string_to_number(longitude_string_b, sep_string=sep_string, direction_flag=direction_flag)
    return longitude_number_distance(longitude_number_a, longitude_number_b)


def latitude_number_distance(latitude_number_a, latitude_number_b):
    return abs(latitude_number_a - latitude_number_b)


def latitude_string_distance(latitude_string_a, latitude_string_b, sep_string=mp_configure.location_sep_string, direction_flag=mp_configure.location_direction_flag[1]):
    latitude_number_a = latitude_string_to_number(latitude_string_a, sep_string=sep_string, direction_flag=direction_flag)
    latitude_number_b = latitude_string_to_number(latitude_string_b, sep_string=sep_string, direction_flag=direction_flag)
    return latitude_number_distance(latitude_number_a, latitude_number_b)


def location_arc_distance(location_a, location_b):
    longitude_distance = longitude_number_distance(location_a.get_longitude().get_longitude_number(), location_b.get_longitude().get_longitude_number())
    latitude_distance = latitude_number_distance(location_a.get_latitude().get_latitude_number(), location_b.get_latitude().get_latitude_number())
    return (longitude_distance ** 2 + latitude_distance ** 2) ** 0.5 / 3600 / 360 * 2 * math.pi


def location_distance(location_a, location_b):
    return int(location_arc_distance(location_a, location_b) * 6371393)


def location_direction(source_location, target_location):
    longitude_difference = target_location.get_longitude().get_longitude_number() - source_location.get_longitude().get_longitude_number()
    if abs(longitude_difference) > 648000:
        if longitude_difference > 0:
            longitude_difference -= 1296000
        else:
            longitude_difference += 1296000
    latitude_difference = target_location.get_latitude().get_latitude_number() - source_location.get_latitude().get_latitude_number()
    return longitude_difference, latitude_difference


def location_eight_party_by_direction_tuple(direction_tuple, direction_flag=mp_configure.location_direction_flag):
    longitude_difference = direction_tuple[0]
    latitude_difference = direction_tuple[1]
    if longitude_difference == 0 and latitude_difference == 0:
        return direction_flag[0][0] + direction_flag[0][-1] + direction_flag[-1][0] + direction_flag[-1][-1]
    elif longitude_difference == 0:
        if latitude_difference > 0:
            return direction_flag[-1][0]
        else:
            return direction_flag[-1][-1]
    elif latitude_difference == 0:
        if latitude_difference > 0:
            return direction_flag[0][0]
        else:
            return direction_flag[0][-1]
    else:
        cot = abs(longitude_difference / latitude_difference)
        if 0.4142135623730951 <= cot <= 2.414213562373095:
            direction_str = ""
            if longitude_difference > 0:
                direction_str += direction_flag[0][0]
            else:
                direction_str += direction_flag[0][-1]
            if latitude_difference > 0:
                direction_str += direction_flag[-1][0]
            else:
                direction_str += direction_flag[-1][-1]
            return direction_str
        elif cot > 2.414213562373095:
            if longitude_difference > 0:
                return direction_flag[0][0]
            else:
                return direction_flag[0][-1]
        elif cot < 0.4142135623730951:
            if latitude_difference > 0:
                return direction_flag[-1][0]
            else:
                return direction_flag[-1][-1]


def location_eight_party(source_location, target_location, direction_flag=mp_configure.location_direction_flag):
    direction_tuple = location_direction(source_location, target_location)
    return location_eight_party_by_direction_tuple(direction_tuple, direction_flag)


class Longitude:
    def __init__(self, longitude, sep_string=mp_configure.location_sep_string, direction_flag=mp_configure.location_direction_flag[0]):
        self.__longitude_number = 0
        self.__longitude_string = sep_string.join(["0"] * 3) + direction_flag[0]
        self.__sep_string = sep_string
        self.__direction_flag = direction_flag
        if isinstance(longitude, str):
            self.set_longitude_string(longitude)
        elif isinstance(longitude, int):
            self.set_longitude_number(longitude)
        elif isinstance(longitude, Longitude):
            self.set_longitude_number(longitude.get_longitude_number())
        else:
            raise Exception("Invalid longitude type: %s" % str(type(longitude)))

    def __str__(self):
        return self.get_longitude_string()

    def get_longitude_tuple(self):
        return (int(elem) for elem in self.__longitude_string.split(self.__sep_string))

    def get_longitude_arc(self):
        return self.__longitude_number / 1296000 * 2 * math.pi

    def set_longitude_string(self, longitude_string):
        self.__longitude_number = longitude_string_to_number(longitude_string, sep_string=self.__sep_string, direction_flag=self.__direction_flag)
        self.__longitude_string = number_to_longitude_string(self.__longitude_number)

    def get_longitude_string(self):
        return self.__longitude_string

    def set_longitude_number(self, longitude_number):
        if abs(longitude_number) > 648000:
            raise Exception("Invalid longitude number: %d" % longitude_number)
        self.__longitude_string = number_to_longitude_string(longitude_number, sep_string=self.__sep_string, direction_flag=self.__direction_flag)
        self.__longitude_number = longitude_number

    def get_longitude_number(self):
        return self.__longitude_number

    def set_sep_string(self, sep_string):
        self.__sep_string = sep_string
        self.__longitude_string = number_to_longitude_string(self.__longitude_number, sep_string=self.__sep_string, direction_flag=self.__direction_flag)

    def get_sep_string(self):
        return self.__sep_string

    def set_direction_flag(self, direction_flag):
        if len(direction_flag) < 2:
            raise Exception("Invalid direction flag: %s" % str(direction_flag))
        self.__direction_flag = direction_flag
        self.__longitude_string = number_to_longitude_string(self.__longitude_number, sep_string=self.__sep_string, direction_flag=self.__direction_flag)

    def get_direction_flag(self):
        return self.__direction_flag

    def east_move_second(self, second):
        second %= 1296000
        self.__longitude_number += second
        self.__longitude_number += 648000
        self.__longitude_number %= 1296000
        self.__longitude_number -= 648000
        self.__longitude_string = number_to_longitude_string(self.__longitude_number, sep_string=self.__sep_string, direction_flag=self.__direction_flag)

    def west_move_second(self, second):
        self.east_move_second(-second)

    def east_move_minute(self, minute):
        self.east_move_second(minute * 60)

    def west_move_minute(self, minute):
        self.west_move_second(minute * 60)

    def east_move_degree(self, degree):
        self.east_move_second(degree * 3600)

    def west_move_degree(self, degree):
        self.west_move_second(degree * 3600)


class Latitude:
    def __init__(self, latitude, sep_string=".", direction_flag=("N", "S")):
        self.__latitude_number = 0
        self.__latitude_string = sep_string.join(["0"] * 3) + direction_flag[0]
        self.__sep_string = sep_string
        self.__direction_flag = direction_flag
        if isinstance(latitude, str):
            self.set_latitude_string(latitude)
        elif isinstance(latitude, int):
            self.set_latitude_number(latitude)
        elif isinstance(latitude, Latitude):
            self.set_latitude_number(latitude.get_latitude_number())
        else:
            raise Exception("Invalid latitude type: %s" % str(type(latitude)))

    def __str__(self):
        return self.get_latitude_string()

    def get_latitude_tuple(self):
        return (int(elem) for elem in self.__latitude_string.split(self.__sep_string))

    def get_latitude_arc(self):
        return self.__latitude_number / 1296000 * 2 * math.pi

    def set_latitude_string(self, latitude_string):
        self.__latitude_number = latitude_string_to_number(latitude_string, sep_string=self.__sep_string, direction_flag=self.__direction_flag)
        self.__latitude_string = number_to_latitude_string(self.__latitude_number)

    def get_latitude_string(self):
        return self.__latitude_string

    def set_latitude_number(self, latitude_number):
        if abs(latitude_number) > 324000:
            raise Exception("Invalid latitude number: %d" % latitude_number)
        self.__latitude_string = number_to_latitude_string(latitude_number, sep_string=self.__sep_string, direction_flag=self.__direction_flag)
        self.__latitude_number = latitude_number

    def get_latitude_number(self):
        return self.__latitude_number

    def set_sep_string(self, sep_string):
        self.__sep_string = sep_string
        self.__latitude_string = number_to_latitude_string(self.__latitude_number, sep_string=self.__sep_string, direction_flag=self.__direction_flag)

    def get_sep_string(self):
        return self.__sep_string

    def set_direction_flag(self, direction_flag):
        if len(direction_flag) < 2:
            raise Exception("Invalid direction flag: %s" % str(direction_flag))
        self.__direction_flag = direction_flag
        self.__latitude_string = number_to_latitude_string(self.__latitude_number, sep_string=self.__sep_string, direction_flag=self.__direction_flag)

    def get_direction_flag(self):
        return self.__direction_flag

    def north_move_second(self, second):
        second %= 1296000
        self.__latitude_number += second
        self.__latitude_number += 324000
        self.__latitude_number %= 1296000
        if self.__latitude_number > 648000:
            self.__latitude_number = 1296000 - self.__latitude_number
        self.__latitude_number -= 324000
        self.__latitude_string = number_to_latitude_string(self.__latitude_number, sep_string=self.__sep_string, direction_flag=self.__direction_flag)

    def south_move_second(self, second):
        self.north_move_second(second)

    def north_move_minute(self, minute):
        self.north_move_second(minute * 60)

    def south_move_minute(self, minute):
        self.south_move_second(minute * 60)

    def north_move_degree(self, degree):
        self.north_move_second(degree * 3600)

    def south_move_degree(self, degree):
        self.south_move_second(degree * 3600)


class Location:
    def __init__(self, longitude=None, latitude=None, sep_string=mp_configure.location_sep_string, direction_flag=mp_configure.location_direction_flag):
        self.__sep_string = sep_string
        self.__longitude_direction_flag = direction_flag[0]
        self.__latitude_direction_flag = direction_flag[-1]
        self.__longitude = None
        self.__latitude = None
        self.__time_zone = None
        self.__local_date = None
        self.__local_time = None
        self.__bind_earth = None
        self.__noon_sun_height = None
        self.__day_length = None
        self.__sunrise_time = None
        self.__sunset_time = None
        self.__name_object_get = {
            "longitude": self.get_longitude,
            "latitude": self.get_latitude,
            "time_zone": self.get_time_zone,
            "local_date": self.get_local_date,
            "local_time": self.get_local_time,
            "bind_earth": self.get_bind_earth,
            "noon_sun_height": self.get_noon_sun_height,
            "day_length": self.get_day_length,
            "sunrise_time": self.get_sunrise_time,
            "sunset_time": self.get_sunset_time,
        }
        self.__name_object_set = {
            "longitude": self.set_longitude,
            "latitude": self.set_latitude,
            "time_zone": self.set_time_zone,
            "local_date": self.set_local_date,
            "local_time": self.set_local_time,
            "bind_earth": self.bind_earth,
            "noon_sun_height": self.set_noon_sun_height,
            "day_length": self.set_day_length,
            "sunrise_time": self.set_sunrise_time,
            "sunset_time": self.set_sunset_time,
        }
        if longitude is not None:
            self.set_longitude(longitude)
        if latitude is not None:
            self.set_latitude(latitude)

    def __str__(self):
        return "(" + ", ".join([str(self.get_longitude()), str(self.get_latitude())]) + ")"

    def get_by_name(self, name):
        if name not in self.__name_object_get:
            return None
        else:
            return self.__name_object_get[name]()

    def set_by_name(self, name, data):
        if name in self.__name_object_set:
            self.__name_object_set[name](data)

    def only_set_longitude(self, longitude):
        self.__longitude = Longitude(longitude)

    def set_longitude(self, longitude):
        self.only_set_longitude(longitude)
        mp_logic.mp_logic.change_linkage(self, ("location", "longitude"))

    def get_longitude(self):
        return self.__longitude

    def only_set_latitude(self, latitude):
        self.__latitude = Latitude(latitude)

    def set_latitude(self, latitude):
        self.only_set_latitude(latitude)
        mp_logic.mp_logic.change_linkage(self, ("location", "latitude"))

    def get_latitude(self):
        return self.__latitude

    def only_set_time_zone(self, time_zone_second):
        if time_zone_second < -43200 or time_zone_second > 43200:
            raise Exception("Invalid time zone: %d" % time_zone_second)
        self.__time_zone = time_zone_second

    def set_time_zone(self, time_zone_second):
        self.only_set_time_zone(time_zone_second)
        mp_logic.mp_logic.change_linkage(self, ("location", "time_zone"))

    def get_time_zone(self):
        return self.__time_zone

    def only_set_local_date(self, date):
        self.__local_date = mp_date_time.Date(date)

    def set_local_date(self, date):
        self.only_set_local_date(date)
        mp_logic.mp_logic.change_linkage(self, ("location", "local_date"))

    def get_local_date(self):
        return self.__local_date

    def only_set_local_time(self, time):
        self.__local_time = mp_date_time.Time(time)

    def set_local_time(self, time):
        self.only_set_local_time(time)
        mp_logic.mp_logic.change_linkage(self, ("location", "local_time"))

    def get_local_time(self):
        return self.__local_time

    def bind_earth(self, earth, from_earth=False):
        if not isinstance(earth, mp_aster.Earth):
            raise Exception("Must input Earth instance: %s" % str(type(earth)))
        self.__bind_earth = earth
        if not from_earth:
            earth.add_bind_location(self, from_location=True)
        for name in self.__bind_earth.get_available_name_list():
            mp_logic.mp_logic.change_linkage(self.__bind_earth, ("earth", name))

    def get_bind_earth(self):
        return self.__bind_earth

    def compute_greenwich_mean_time(self, time):
        time.backward_second(self.get_time_zone())

    def compute_arc_distance(self, target_location):
        return location_arc_distance(self, target_location)

    def compute_distance(self, target_location):
        return location_distance(self, target_location)

    def compute_direction(self, target_location):
        return location_direction(self, target_location)

    def compute_direction_eight_party(self, target_location):
        return location_eight_party(self, target_location)

    def only_set_noon_sun_height(self, latitude):
        self.__noon_sun_height = Latitude(latitude)

    def set_noon_sun_height(self, latitude):
        self.only_set_day_length(latitude)
        mp_logic.mp_logic.change_linkage(self, ("location", "noon_sun_height"))

    def get_noon_sun_height(self):
        return self.__noon_sun_height

    def only_set_day_length(self, time):
        self.__day_length = mp_date_time.Time(time)

    def set_day_length(self, time):
        self.only_set_day_length(time)
        mp_logic.mp_logic.change_linkage(self, ("location", "day_length"))

    def get_day_length(self):
        return self.__day_length

    def only_set_sunrise_time(self, time):
        self.__sunrise_time = mp_date_time.Time(time)

    def set_sunrise_time(self, time):
        self.only_set_sunrise_time(time)
        mp_logic.mp_logic.change_linkage(self, ("location", "sunrise_time"))

    def get_sunrise_time(self):
        return self.__sunrise_time

    def only_set_sunset_time(self, time):
        self.__sunset_time = mp_date_time.Time(time)

    def set_sunset_time(self, time):
        self.only_set_sunset_time(time)
        mp_logic.mp_logic.change_linkage(self, ("location", "sunset_time"))

    def get_sunset_time(self):
        return self.__sunset_time
