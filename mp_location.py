import copy
import math
from mp_date_time import Date, Time
import mp_logic


def longitude_string_to_number(longitude_string, sep_string=".", direction_flag=("E", "W")):
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


def number_to_longitude_string(number, sep_string=".", direction_flag=("E", "W")):
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


def latitude_string_to_number(latitude_string, sep_string=".", direction_flag=("N", "S")):
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


def number_to_latitude_string(number, sep_string=".", direction_flag=("N", "S")):
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


def longitude_string_distance(longitude_string_a, longitude_string_b, sep_string=".", direction_flag=("E", "W")):
    longitude_number_a = longitude_string_to_number(longitude_string_a, sep_string=sep_string,
                                                    direction_flag=direction_flag)
    longitude_number_b = longitude_string_to_number(longitude_string_b, sep_string=sep_string,
                                                    direction_flag=direction_flag)
    return longitude_number_distance(longitude_number_a, longitude_number_b)


def latitude_number_distance(latitude_number_a, latitude_number_b):
    return abs(latitude_number_a - latitude_number_b)


def latitude_string_distance(latitude_string_a, latitude_string_b, sep_string=".", direction_flag=("N", "S")):
    latitude_number_a = latitude_string_to_number(latitude_string_a, sep_string=sep_string,
                                                  direction_flag=direction_flag)
    latitude_number_b = latitude_string_to_number(latitude_string_b, sep_string=sep_string,
                                                  direction_flag=direction_flag)
    return latitude_number_distance(latitude_number_a, latitude_number_b)


def location_arc_distance(location_a, location_b):
    longitude_distance = longitude_number_distance(location_a.get_longitude().get_longitude_number(),
                                                   location_b.get_longitude().get_longitude_number())
    latitude_distance = latitude_number_distance(location_a.get_latitude().get_latitude_number(),
                                                 location_b.get_latitude().get_latitude_number())
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


def location_eight_party_by_direction_tuple(direction_tuple, direction_flag=(("E", "W"), ("N", "S"))):
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


def location_eight_party(source_location, target_location, direction_flag=(("E", "W"), ("N", "S"))):
    direction_tuple = location_direction(source_location, target_location)
    return location_eight_party_by_direction_tuple(direction_tuple, direction_flag)


class Longitude:
    def __init__(self, longitude, sep_string=".", direction_flag=("E", "W")):
        self.__longitude_number = 0
        self.__longitude_string = sep_string.join(["0"] * 3) + direction_flag[0]
        self.__sep_string = sep_string
        self.__direction_flag = direction_flag
        if isinstance(longitude, str):
            self.set_longitude_string(longitude)
        elif isinstance(longitude, int):
            self.set_longitude_number(longitude)
        else:
            raise Exception("Invalid longitude type: %s" % str(type(longitude)))

    def get_longitude_tuple(self):
        return (int(elem) for elem in self.__longitude_string.split(self.__sep_string))

    def get_longitude_arc(self):
        return self.__longitude_number / 1296000 * 2 * math.pi

    def set_longitude_string(self, longitude_string):
        self.__longitude_number = longitude_string_to_number(longitude_string,
                                                             sep_string=self.__sep_string,
                                                             direction_flag=self.__direction_flag)
        self.__longitude_string = longitude_string

    def get_longitude_string(self):
        return self.__longitude_string

    def set_longitude_number(self, longitude_number):
        if abs(longitude_number) > 648000:
            raise Exception("Invalid longitude number: %d" % longitude_number)
        self.__longitude_string = number_to_longitude_string(longitude_number,
                                                             sep_string=self.__sep_string,
                                                             direction_flag=self.__direction_flag)
        self.__longitude_number = longitude_number

    def get_longitude_number(self):
        return self.__longitude_number

    def set_sep_string(self, sep_string):
        self.__sep_string = sep_string
        self.__longitude_string = number_to_longitude_string(self.__longitude_number,
                                                             sep_string=self.__sep_string,
                                                             direction_flag=self.__direction_flag)

    def get_sep_string(self):
        return self.__sep_string

    def set_direction_flag(self, direction_flag):
        if len(direction_flag) < 2:
            raise Exception("Invalid direction flag: %s" % str(direction_flag))
        self.__direction_flag = direction_flag
        self.__longitude_string = number_to_longitude_string(self.__longitude_number,
                                                             sep_string=self.__sep_string,
                                                             direction_flag=self.__direction_flag)

    def get_direction_flag(self):
        return self.__direction_flag

    def east_move_second(self, second):
        second %= 1296000
        self.__longitude_number += second
        self.__longitude_number += 648000
        self.__longitude_number %= 1296000
        self.__longitude_number -= 648000
        self.__longitude_string = number_to_longitude_string(self.__longitude_number,
                                                             sep_string=self.__sep_string,
                                                             direction_flag=self.__direction_flag)

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
        else:
            raise Exception("Invalid latitude type: %s" % str(type(latitude)))

    def get_latitude_tuple(self):
        return (int(elem) for elem in self.__latitude_string.split(self.__sep_string))

    def get_latitude_arc(self):
        return self.__latitude_number / 1296000 * 2 * math.pi

    def set_latitude_string(self, latitude_string):
        self.__latitude_number = latitude_string_to_number(latitude_string,
                                                           sep_string=self.__sep_string,
                                                           direction_flag=self.__direction_flag)
        self.__latitude_string = latitude_string

    def get_latitude_string(self):
        return self.__latitude_string

    def set_latitude_number(self, latitude_number):
        if abs(latitude_number) > 324000:
            raise Exception("Invalid latitude number: %d" % latitude_number)
        self.__latitude_string = number_to_latitude_string(latitude_number,
                                                           sep_string=self.__sep_string,
                                                           direction_flag=self.__direction_flag)
        self.__latitude_number = latitude_number

    def get_latitude_number(self):
        return self.__latitude_number

    def set_sep_string(self, sep_string):
        self.__sep_string = sep_string
        self.__latitude_string = number_to_latitude_string(self.__latitude_number,
                                                           sep_string=self.__sep_string,
                                                           direction_flag=self.__direction_flag)

    def get_sep_string(self):
        return self.__sep_string

    def set_direction_flag(self, direction_flag):
        if len(direction_flag) < 2:
            raise Exception("Invalid direction flag: %s" % str(direction_flag))
        self.__direction_flag = direction_flag
        self.__latitude_string = number_to_latitude_string(self.__latitude_number,
                                                           sep_string=self.__sep_string,
                                                           direction_flag=self.__direction_flag)

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
        self.__latitude_string = number_to_latitude_string(self.__latitude_number,
                                                           sep_string=self.__sep_string,
                                                           direction_flag=self.__direction_flag)

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
    def __init__(self, longitude=None, latitude=None, sep_string=".", direction_flag=(("E", "W"), ("N", "S"))):
        self.__sep_string = sep_string
        self.__longitude_direction_flag = direction_flag[0]
        self.__latitude_direction_flag = direction_flag[-1]
        self.__time_zone = None
        self.__local_time = None
        if longitude is not None:
            self.set_longitude(longitude)
        else:
            self.__longitude = None
        if latitude is not None:
            self.set_latitude(latitude)
        else:
            self.__latitude = None

    def get_by_name(self, name):
        name_object = {
            "longitude": self.__longitude,
            "latitude": self.__latitude,
            "time_zone": self.__time_zone,
            "local_time": self.__local_time,
        }
        if name not in name_object:
            return None
        else:
            return name_object[name]

    def set_longitude(self, longitude):
        if isinstance(longitude, str) or isinstance(longitude, int):
            self.__longitude = Longitude(longitude)
        elif isinstance(longitude, Longitude):
            self.__longitude = copy.deepcopy(longitude)
        else:
            raise Exception("Invalid longitude type: %s" % str(type(longitude)))
        mp_logic.mp_logic.change_linkage(self, "longitude")

    def get_longitude(self):
        return self.__longitude

    def set_latitude(self, latitude):
        if isinstance(latitude, str) or isinstance(latitude, int):
            self.__latitude = Latitude(latitude)
        elif isinstance(latitude, Latitude):
            self.__latitude = copy.copy(latitude)
        else:
            raise Exception("Invalid longitude type: %s" % str(type(latitude)))

    def get_latitude(self):
        return self.__latitude

    def _compute_time_zone(self):
        if self.__longitude is None:
            raise Exception("Can not compute time zone: longitude is None")
        return int(self.__longitude.get_longitude_number() / 15)

    def set_time_zone(self, time_zone_second):
        if time_zone_second < -43200 or time_zone_second > 43200:
            raise Exception("Invalid time zone: %d" % time_zone_second)
        self.__time_zone = time_zone_second
        mp_logic.mp_logic.change_linkage(self, "time_zone")

    def set_time_zone_standardized(self, time_zone_standardized):
        self.set_time_zone(time_zone_standardized * 15 * 3600)

    def get_time_zone(self):
        return self.__time_zone

    def set_local_time(self, time):
        if not isinstance(time, "Time"):
            raise Exception("Must input Time instance: %s" % str(type(time)))
        self.__local_time = copy.copy(time)

    def get_local_time(self):
        return self.__local_time

    def compute_time_zone_standardized(self):
        if self.__time_zone is not None:
            return int(self.__time_zone / 3600 / 15)
        else:
            return None

    def compute_greenwich_mean_time(self, time):
        time.backward_second(self.get_time_zone())

    def compute_local_date_time(self, earth):
        date = Date(earth.get_date())
        time = Time(earth.get_time())
        time_number = time.get_time_number()
        time_number += self.__time_zone
        if time_number < 0:
            date.backward_day(1)
            time_number += 86400
        elif time_number > 86400:
            date.forward_day(1)
            time_number -= 86400
        time.set_time_number(time_number)
        return date, time

    def compute_arc_distance(self, target_location):
        return location_arc_distance(self, target_location)

    def compute_distance(self, target_location):
        return location_distance(self, target_location)

    def compute_direction(self, target_location):
        return location_direction(self, target_location)

    def compute_direction_eight_party(self, target_location):
        return location_eight_party(self, target_location)

    def compute_noon_sun_height(self, earth):
        latitude_difference = abs(self.__latitude.get_latitude_number() - earth.get_declination().get_latitude_number())
        return 324000 - latitude_difference

    def compute_day_length(self, earth):
        declination = earth.get_declination()
        theta = math.atan(math.tan(declination.get_latitude_arc()) * math.tan(self.get_latitude().get_latitude_arc()))
        theta += 3.4212671791288e-7 / (math.cos(declination.get_latitude_arc()) ** 2 * math.cos(self.get_latitude().get_latitude_arc()) * math.cos(theta))
        return int((12 + 2 * theta / (2 * math.pi * 24)) * 3600)

    def compute_sunrise_sunset_local_time(self, earth):
        day_length = self.compute_day_length(earth)
        sunrise_time = int(43200 - day_length / 2)
        sunset_time = int(43200 + day_length / 2)
        return Time(sunrise_time), Time(sunset_time)
