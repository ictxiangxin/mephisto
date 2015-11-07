import mp_configure
import mp_date_time
import mp_location
import mp_log


def normalize_date(date_string):
    mp_log.log.record("Normalize Date: \"%s\"" % date_string)
    if "年" not in date_string:
        date_string = "2015年" + date_string
    date_string = date_string.replace("年", mp_configure.date_sep_string)
    date_string = date_string.replace("月", mp_configure.date_sep_string)
    date_string = date_string.replace("日", "")
    date = mp_date_time.Date(date_string)
    return date


def normalize_time(time_string):
    mp_log.log.record("Normalize Time: \"%s\"" % time_string)
    if "时" in time_string or "点" in time_string:
        if "分" not in time_string:
            time_string += "00分"
        if "秒" not in time_string:
            time_string += "00秒"
        time_string = time_string.replace("时", mp_configure.time_sep_string).replace("点", mp_configure.time_sep_string)
        time_string = time_string.replace("分", mp_configure.time_sep_string)
        time_string = time_string.replace("秒", "")
    else:
        if sum([1 if c == ":" else 0 for c in time_string]) == 1:
            time_string += ":00"
        time_string = time_string.replace(":", mp_configure.time_sep_string)
    time = mp_date_time.Time(time_string)
    return time


def normalize_time_lapse(time_string):
    mp_log.log.record("Normalize Time Lapse: \"%s\"" % time_string)
    if "分" not in time_string:
        time_string += "00分"
    if "秒" not in time_string:
        time_string += "00秒"
    time_string = time_string.replace("小时", mp_configure.time_sep_string)
    time_string = time_string.replace("分", mp_configure.time_sep_string)
    time_string = time_string.replace("秒", "")
    h, m, s = [int(elem) for elem in time_string.split(mp_configure.time_sep_string)]
    total_s = h * 3600 + m * 60 + s
    return total_s


def normalize_degree(degree_string):
    mp_log.log.record("Normalize Degree: \"%s\"" % degree_string)
    if "′" not in degree_string:
        degree_string += "00′"
    if "″" not in degree_string:
        degree_string += "00″"
    degree_string = degree_string.replace("°", mp_configure.location_sep_string)
    degree_string = degree_string.replace("′", mp_configure.location_sep_string)
    degree_string = degree_string.replace("″", "")
    degree_string += mp_configure.location_direction_flag[1][0]
    degree = mp_location.Latitude(degree_string)
    return degree


def normalize_longitude(longitude_string):
    mp_log.log.record("Normalize Longitude: \"%s\"" % longitude_string)
    if "东经" in longitude_string:
        longitude_string = longitude_string[2:]
        longitude_string += mp_configure.location_direction_flag[0][0]
    if "西经" in longitude_string:
        longitude_string = longitude_string[2:]
        longitude_string += mp_configure.location_direction_flag[0][1]
    degree_string = longitude_string[:-1]
    direction = longitude_string[-1]
    if "′" not in degree_string:
        degree_string += "00′"
    if "″" not in degree_string:
        degree_string += "00″"
    degree_string = degree_string.replace("°", mp_configure.location_sep_string)
    degree_string = degree_string.replace("′", mp_configure.location_sep_string)
    degree_string = degree_string.replace("″", "")
    degree_string += mp_configure.location_direction_flag[0][0]
    degree = mp_location.Longitude(degree_string).get_longitude_number()
    if direction == "W":
        degree = -degree
    longitude = mp_location.Longitude(degree)
    return longitude


def normalize_latitude(latitude_string):
    mp_log.log.record("Normalize Latitude: \"%s\"" % latitude_string)
    if "北纬" in latitude_string:
        latitude_string = latitude_string[2:]
        latitude_string += mp_configure.location_direction_flag[1][0]
    if "南纬" in latitude_string:
        latitude_string = latitude_string[2:]
        latitude_string += mp_configure.location_direction_flag[1][1]
    degree_string = latitude_string[:-1]
    direction = latitude_string[-1]
    if "′" not in degree_string:
        degree_string += "00′"
    if "″" not in degree_string:
        degree_string += "00″"
    degree_string = degree_string.replace("°", mp_configure.location_sep_string)
    degree_string = degree_string.replace("′", mp_configure.location_sep_string)
    degree_string = degree_string.replace("″", "")
    degree_string += mp_configure.location_direction_flag[1][0]
    degree = mp_location.Latitude(degree_string).get_latitude_number()
    if direction == "S":
        degree = -degree
    latitude = mp_location.Latitude(degree)
    return latitude


def normalize_geo(geo_string):
    geo_name_map = {
        "位于": "direction"
    }
    if geo_string not in geo_name_map:
        return "<Unknown>"
    return geo_name_map[geo_string]


def normalize_metric(metric_string):
    metric_name_map = {
        "距离": "distance"
    }
    if metric_string not in metric_name_map:
        return "<Unknown>"
    return metric_name_map[metric_string]


def normalize_attribute(attribute_string):
    attribute_name_map = {
        "日出": "sunrise_time",
        "日落": "sunset_time",
        "昼长": "day_length",
        "正午太阳高度": "noon_sun_height",
        "经度": "longitude",
        "纬度": "latitude",
        "时区": "time_zone_text",
    }
    if attribute_string not in attribute_name_map:
        return "<Unknown>"
    return attribute_name_map[attribute_string]


def normalize_phenomenon(phenomenon_string):
    phenomenon_name_map = {
        "日影最短": "shortest_shadow_of_sun",
        "正午": "noon_time",
    }
    if phenomenon_string not in phenomenon_name_map:
        return "<Unknown>"
    return phenomenon_name_map[phenomenon_string]
