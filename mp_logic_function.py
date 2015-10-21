def compute_time_zone_by_longitude(location):
    location.set_time_zone(int(location.get_longitude().get_longitude_number() / 15))


def compute_longitude_by_time_zone(location):
    location.set_longitude(location.get_time_zone() * 15)


function_register = {
    "compute_time_zone_by_longitude": compute_time_zone_by_longitude,
    "compute_longitude_by_time_zone": compute_longitude_by_time_zone,
}
