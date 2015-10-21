from mp_date_time import *
from mp_location import Latitude
import copy
import math


def compute_time_zone_by_longitude(location):
    location.set_time_zone(int(location.get_longitude().get_longitude_number() / 15))


def compute_longitude_by_time_zone(location):
    location.set_longitude(location.get_time_zone() * 15)


def compute_declination_by_date(earth):
    y, m, d = earth.__date.get_date_tuple()
    ordinal_number = month_to_number(m) + d
    b = 2 * math.pi * (ordinal_number - 1) / 365
    delta = 0.006918
    delta -= 0.399912 * math.cos(b) + 0.006758 * math.cos(2 * b) + 0.002697 * math.cos(3 * b)
    delta += 0.070257 * math.sin(b) + 0.000907 * math.sin(2 * b) + 0.001480 * math.sin(3 * b)
    earth.set_declination(Latitude(int(648000 / math.pi * delta), sep_string=earth.get_location_sep_string(),
                                   direction_flag=earth.get_direction_flag()[-1]))


def compute_equinox_by_date(earth):
    y, m, d = earth.__date.get_date_tuple()
    yy = y % 100
    d = int(yy * 0.2422 + 20.646) - int(yy / 4)
    m = 3
    sprint_equinox = Date(earth.__date_sep_string.join([str(y), str(m), str(d)]))
    autumnal_equinox = copy.deepcopy(sprint_equinox)
    autumnal_equinox.forward_day(186)
    earth.set_spring_equinox(sprint_equinox)
    earth.set_autumnal_equinox(autumnal_equinox)


function_register = {
    "compute_time_zone_by_longitude": compute_time_zone_by_longitude,
    "compute_longitude_by_time_zone": compute_longitude_by_time_zone,
    "compute_declination_by_date": compute_declination_by_date,
    "compute_equinox_by_date": compute_equinox_by_date,
}
