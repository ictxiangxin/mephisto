import mp_date_time


def ph_shortest_shadow_of_sun(location):
    location.set_local_time(mp_date_time.Time("12:00:00"))


phenomenon_map = {
    "shortest_shadow_of_sun": ph_shortest_shadow_of_sun,
}


def phenomenon_implementation(phenomenon_name):
    if phenomenon_name not in phenomenon_map:
        return None
    return phenomenon_map[phenomenon_name]
