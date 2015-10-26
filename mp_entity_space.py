import mp_aster
import mp_location
import mp_phenomenon


class World:
    def __init__(self):
        self.__earth = mp_aster.Earth()
        self.__location = {}
        self.__anonymous_entity = []
        self.__phenomenon = {}

    def import_earth(self, earth):
        if not isinstance(earth, mp_aster.Earth):
            raise Exception("Import object is not Earth, type: %s" % type(earth))
        self.__earth = earth
        for name, location in self.__location.items():
            location.set_bind_earth(self.__earth)

    def get_earth(self):
        return self.__earth

    def add_location(self, name, location):
        if not isinstance(location, mp_location.Location):
            raise Exception("Import object is not Location, type: %s" % type(location))
        self.__location[name] = location
        if self.__earth is not None:
            location.set_bind_earth(self.__earth)

    def get_location(self, name):
        if name not in self.__location:
            return None
        return self.__location[name]

    def get_location_list(self):
        return list(self.__location)

    def add_phenomenon(self, location_name, phenomenon_name):
        if location_name not in self.__location:
            raise Exception("Invalid location name: %s" % location_name)
        if phenomenon_name not in mp_phenomenon.phenomenon_map:
            raise Exception("Invalid phenomenon name: %s" % phenomenon_name)
        if location_name not in self.__phenomenon:
            self.__phenomenon[location_name] = []
        self.__phenomenon[location_name].append(phenomenon_name)

    def get_phenomenon(self, name):
        if name not in self.__phenomenon:
            return None
        return self.__phenomenon[name]
