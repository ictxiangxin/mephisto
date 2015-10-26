import mp_date_time


def ph_shortest_shadow_of_sun(location):
    location.set_local_time(mp_date_time.Time("12:00:00"))


phenomenon_map = {
    "shortest_shadow_of_sun": ph_shortest_shadow_of_sun,
}
