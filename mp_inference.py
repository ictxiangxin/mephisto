from mp_phenomenon import phenomenon_map


def phenomenon_handle(world):
    location_list = world.get_location_list()
    for location in location_list:
        phenomenon_list = world.get_phenomenon(location)
        if phenomenon_list is not None:
            for phenomenon in phenomenon_list:
                phenomenon_map[phenomenon](world.get_location(location))


def inference(world, attribute):
    phenomenon_handle(world)
    name = attribute[0]
    elem = attribute[1]
    if name not in world.get_location_list():
        return
    rst = world.get_location(name).get_by_name(elem)
    if rst is not None:
        return rst
