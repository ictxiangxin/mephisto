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

    def set_earth_attribute(self, attribute_name, data):
        self.__earth.set_by_name(attribute_name, data)

    def add_location(self, name, location):
        if not isinstance(location, mp_location.Location):
            raise Exception("Import object is not Location, type: %s" % type(location))
        self.__location[name] = location
        location.bind_earth(self.__earth)

    def get_location(self, name):
        if name not in self.__location:
            return None
        return self.__location[name]

    def get_location_list(self):
        return list(self.__location)

    def set_location_attribute(self, name, attribute_name, data):
        if name in self.__location:
            self.__location[name].set_by_name(attribute_name, data)


class MephistoEngine:
    def __init__(self):
        self.__world = World()
        self.__variable = {}

    def execute_code(self, code):
        import mp_mephisto_language
        token_list = mp_mephisto_language.mephisto_language_lexical(code)
        code_list = mp_mephisto_language.mephisto_language_grammar(token_list)
