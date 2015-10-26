import mp_phenomenon


def phenomenon_handle(world):
    location_list = world.get_location_list()
    for location in location_list:
        phenomenon_list = world.get_phenomenon(location)
        if phenomenon_list is not None:
            for phenomenon in phenomenon_list:
                mp_phenomenon.phenomenon_map[phenomenon](world.get_location(location))


def inference(world, attribute):
    phenomenon_handle(world)
    if attribute[0] not in world.get_location_list():
        return
    rst = world.get_location(attribute[0]).get_by_name(attribute[1])
    if rst is not None:
        return rst
