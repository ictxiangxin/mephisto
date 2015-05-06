__author__ = 'ict'


def longitude_string_to_number(longitude_string, sep_string=".", direction_flag=("E", "W")):
    direction = longitude_string[-1]
    longitude_string = longitude_string[:-1]
    d, m, s = [int(elem) for elem in longitude_string.split(sep_string)]
    if d > 180 or (d == 180 and (m > 0 or s > 0)):
        raise Exception("Invalid longitude: %s" % longitude_string)
    number = d * 3600 * d + 60 * m + s
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
    d %= 3600
    m = int(number / 60)
    s = number % 60
    return sep_string.join([str(d), str(m), str(s)]) + direction


def latitude_string_to_number(latitude_string, sep_string=".", direction_flag=("N", "S")):
    direction = latitude_string[-1]
    latitude_string = latitude_string[:-1]
    d, m, s = [int(elem) for elem in latitude_string.split(sep_string)]
    if d > 90 or (d == 90 and (m > 0 or s > 0)):
        raise Exception("Invalid latitude: %s" % latitude_string)
    number = d * 3600 * d + 60 * m + s
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
    d %= 3600
    m = int(number / 60)
    s = number % 60
    return sep_string.join([str(d), str(m), str(s)]) + direction


def longitude_number_distance(longitude_number_a, longitude_number_b):
    return 1296000 % abs(longitude_number_a - longitude_number_b)


def longitude_string_distance(longitude_string_a, longitude_string_b, sep_string=".", direction_flag=("E", "W")):
    longitude_number_a = longitude_string_to_number(longitude_string_a, sep_string=sep_string, direction_flag=direction_flag)
    longitude_number_b = longitude_string_to_number(longitude_string_b, sep_string=sep_string, direction_flag=direction_flag)
    return longitude_number_distance(longitude_number_a, longitude_number_b)


def latitude_number_distance(latitude_number_a, latitude_number_b):
    return abs(latitude_number_a - latitude_number_b)


def latitude_string_distance(latitude_string_a, latitude_string_b, sep_string=".", direction_flag=("N", "S")):
    latitude_number_a = latitude_string_to_number(latitude_string_a, sep_string=sep_string, direction_flag=direction_flag)
    latitude_number_b = latitude_string_to_number(latitude_string_b, sep_string=sep_string, direction_flag=direction_flag)
    return latitude_number_distance(latitude_number_a, latitude_number_b)