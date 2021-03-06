import mp_date_time
import mp_location
import mp_log


def ph_shortest_shadow_of_sun(location):
    mp_log.log.record("Location: %d" % id(location))
    location.set_local_time(mp_date_time.Time("12:00:00"))


def ph_noon_time(location):
    mp_log.log.record("Location: %d" % id(location))
    location.set_local_time(mp_date_time.Time("12:00:00"))


phenomenon_map = {
    "shortest_shadow_of_sun": ph_shortest_shadow_of_sun,
    "noon_time": ph_noon_time,
}


def phenomenon_implementation(phenomenon_name):
    if phenomenon_name not in phenomenon_map:
        return None
    return phenomenon_map[phenomenon_name]


def ac_time_forward(location, time):
    mp_log.log.record("Location: %s, Time: %s" % (id(location), str(time)))
    local_time = location.get_local_time()
    if local_time is not None:
        local_time.forward_second(int(time))
        location.set_local_time(local_time)


action_map = {
    "time_forward": ac_time_forward,
}


def action_implementation(action_name):
    if action_name not in action_map:
        return None
    return action_map[action_name]


def fc_distance(location_a, location_b):
    mp_log.log.record("Location A: %s, Location B: %s" % (id(location_a), id(location_b)))
    distance = mp_location.location_distance(location_a, location_b)
    return distance


def fc_direction(location_a, location_b):
    mp_log.log.record("Location A: %s, Location B: %s" % (id(location_a), id(location_b)))
    direction = mp_location.location_eight_party_by_direction_tuple(mp_location.location_direction(location_a, location_b))
    return direction


function_map = {
    "distance": fc_distance,
    "direction": fc_direction,
}


def function_implementation(function_name):
    if function_name not in function_map:
        return None
    return function_map[function_name]
