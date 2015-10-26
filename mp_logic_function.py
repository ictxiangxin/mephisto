import mp_date_time
import mp_location
import copy
import math


def compute_time_zone_by_longitude(location):
    longitude = location.get_longitude().get_longitude_number()
    time_zone = int(longitude / 15)
    location.only_set_time_zone(time_zone)


def compute_longitude_by_time_zone(location):
    time_zone = location.get_time_zone()
    longitude = time_zone * 15
    location.only_set_longitude(longitude)


def compute_local_datetime_by_bind_earth(location):
    earth = location.get_bind_earth()
    earth_date = earth.get_date()
    earth_time = earth.get_time()
    if earth_date is not None:
        earth_date = mp_date_time.Date(earth_date)
    if earth_time is not None:
        earth_time = mp_date_time.Time(earth_time)
        time_number = earth_time.get_time_number()
        time_number += location.get_time_zone()
        if time_number < 0:
            time_number += 86400
            if earth_date is not None:
                earth_date.backward_day(1)
                location.only_set_local_date(earth_date)
        elif time_number > 86400:
            time_number -= 86400
            if earth_date is not None:
                earth_date.forward_day(1)
                location.only_set_local_date(earth_date)
        else:
            if earth_date is not None:
                location.only_set_local_date(earth_date)
        earth_time.set_time_number(time_number)
        location.only_set_local_time(earth_time)


def compute_sunrise_time_by_day_length(location):
    day_length = location.get_day_length()
    day_length_number = day_length.get_time_number()
    sunrise_time = int(43200 - day_length_number / 2)
    location.only_set_sunrise_time(mp_date_time.Time(sunrise_time))


def compute_day_length_by_sunrise_time(location):
    sunrise_time = location.get_sunrise_time()
    sunrise_time_number = sunrise_time.get_time_string()
    day_length = 86400 - 2 * sunrise_time_number
    location.set_day_length(mp_date_time.Time(day_length))


def compute_sunset_time_by_day_length(location):
    day_length = location.get_day_length()
    day_length_number = day_length.get_time_number()
    sunset_time = int(43200 + day_length_number / 2)
    location.only_set_sunrise_time(sunset_time)


def compute_day_length_by_sunset_time(location):
    sunset_time = location.get_sunset_time()
    sunset_time_number = sunset_time.get_time_number()
    day_length = 2 * sunset_time_number - 86400
    location.set_day_length(mp_date_time.Time(day_length))


def compute_earth_datetime_by_local_datetime(location, earth):
    local_date = location.get_local_date()
    local_time = location.get_local_time()
    if local_date is not None:
        local_date = mp_date_time.Date(local_date)
    if local_time is not None:
        local_time = mp_date_time.Time(local_time)
        time_number = local_time.get_time_number()
        time_number -= location.get_time_zone()
        if time_number < 0:
            time_number += 86400
            if local_date is not None:
                local_date.backward_day(1)
                earth.set_date(local_date)
        elif time_number > 86400:
            time_number -= 86400
            if local_date is not None:
                local_date.forward_day(1)
                earth.set_date(local_date)
        else:
            if local_date is not None:
                earth.set_date(local_date)
        local_time.set_time_number(time_number)
        earth.set_time(local_time)


def compute_declination_by_date(earth):
    y, m, d = earth.get_date().get_date_tuple()
    ordinal_number = mp_date_time.month_to_number(m) + d
    b = 2 * math.pi * (ordinal_number - 1) / 365
    delta = 0.006918
    delta -= 0.399912 * math.cos(b) + 0.006758 * math.cos(2 * b) + 0.002697 * math.cos(3 * b)
    delta += 0.070257 * math.sin(b) + 0.000907 * math.sin(2 * b) + 0.001480 * math.sin(3 * b)
    earth.set_declination(mp_location.Latitude(int(648000 / math.pi * delta), sep_string=earth.get_location_sep_string(), direction_flag=earth.get_direction_flag()[-1]))


def compute_equinox_by_date(earth):
    y, m, d = earth.get_date().get_date_tuple()
    yy = y % 100
    d = int(yy * 0.2422 + 20.646) - int(yy / 4)
    m = 3
    sprint_equinox = mp_date_time.Date(earth.get_date_sep_string().join([str(y), str(m), str(d)]))
    autumnal_equinox = copy.deepcopy(sprint_equinox)
    autumnal_equinox.forward_day(186)
    earth.set_spring_equinox(sprint_equinox)
    earth.set_autumnal_equinox(autumnal_equinox)


def compute_local_datetime_by_earth(earth, location):
    earth_date = earth.get_date()
    earth_time = earth.get_time()
    if earth_date is not None:
        earth_date = mp_date_time.Date(earth_date)
    if earth_time is not None:
        earth_time = mp_date_time.Time(earth_time)
        time_number = earth_time.get_time_number()
        time_number += location.get_time_zone()
        if time_number < 0:
            time_number += 86400
            if earth_date is not None:
                earth_date.backward_day(1)
                location.only_set_local_date(earth_date)
        elif time_number > 86400:
            time_number -= 86400
            if earth_date is not None:
                earth_date.forward_day(1)
                location.only_set_local_date(earth_date)
        else:
            if earth_date is not None:
                location.only_set_local_date(earth_date)
        earth_time.set_time_number(time_number)
        location.only_set_local_time(earth_time)


def compute_noon_sun_height(location, earth):
    latitude_difference = abs(location.get_latitude().get_latitude_number() - earth.get_declination().get_latitude_number())
    noon_sun_height = 324000 - latitude_difference
    location.only_set_noon_sun_height(noon_sun_height)


def compute_day_length(location, earth):
    declination = earth.get_declination()
    theta = math.atan(math.tan(declination.get_latitude_arc()) * math.tan(location.get_latitude().get_latitude_arc()))
    theta += 3.4212671791288e-7 / (math.cos(declination.get_latitude_arc()) ** 2 * math.cos(location.get_latitude().get_latitude_arc()) * math.cos(theta))
    day_length = int((12 + 2 * theta / (2 * math.pi * 24)) * 3600)
    location.only_set_day_length(day_length)


function_register = {
    "compute_time_zone_by_longitude": compute_time_zone_by_longitude,
    "compute_longitude_by_time_zone": compute_longitude_by_time_zone,
    "compute_local_datetime_by_bind_earth": compute_local_datetime_by_bind_earth,
    "compute_sunrise_time_by_day_length": compute_sunrise_time_by_day_length,
    "compute_day_length_by_sunrise_time": compute_day_length_by_sunrise_time,
    "compute_sunset_time_by_day_length": compute_sunset_time_by_day_length,
    "compute_day_length_by_sunset_time": compute_day_length_by_sunset_time,
    "compute_earth_datetime_by_local_datetime": compute_earth_datetime_by_local_datetime,
    "compute_declination_by_date": compute_declination_by_date,
    "compute_equinox_by_date": compute_equinox_by_date,
    "compute_local_datetime_by_earth": compute_local_datetime_by_earth,
    "compute_noon_sun_height": compute_noon_sun_height,
    "compute_day_length": compute_day_length,
}
