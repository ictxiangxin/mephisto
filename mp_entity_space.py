from mp_aster import Earth
from mp_location import Location


class World:
    def __init__(self):
        self.__earth = Earth()
        self.__location = {}
        self.__anonymous_entity = []
        self.__phenomenon_list = []

    def import_earth(self, earth):
        if not isinstance(earth, Earth):
            raise Exception("Import object is not Earth, type: %s" % type(earth))
        self.__earth = earth

    def add_location(self, name, location):
        if not isinstance(location, Location):
            raise Exception("Import object is not Location, type: %s" % type(location))
        self.__location[name] = location
