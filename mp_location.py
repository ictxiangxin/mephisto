__author__ = 'ict'


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


class Longitude:
    def __init__(self, longitude_string, sep_string=".", direction_flag=("E", "W")):
        self.__longitude_number = 0
        self.__longitude_string = sep_string.join(["0"] * 3) + direction_flag[0]
        self.__sep_string = sep_string
        self.__direction_flag = direction_flag
        self.set_longitude_string(longitude_string)

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
    def __init__(self, latitude_string, sep_string=".", direction_flag=("N", "S")):
        self.__latitude_number = 0
        self.__latitude_string = sep_string.join(["0"] * 3) + direction_flag[0]
        self.__sep_string = sep_string
        self.__direction_flag = direction_flag
        self.set_latitude_string(latitude_string)

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