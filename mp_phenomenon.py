from mp_date_time import Time


def ph_shortest_shadow_of_sun(location):
    location.set_local_time(Time("12:00:00"))


phenomenon_map = {
    "shortest_shadow_of_sun": ph_shortest_shadow_of_sun,
}
