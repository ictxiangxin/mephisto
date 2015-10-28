import copy
import mp_configure
import mp_aster
import mp_location
import mp_phenomenon


class World:
    def __init__(self):
        self.__earth = mp_aster.Earth()
        self.__location = {}
        self.__anonymous_entity = []
        self.__phenomenon = {}

    def clear(self):
        self.__init__()

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

    def clear(self):
        self.__init__()

    def get_world(self):
        return self.__world

    def set_variable(self, name, data):
        self.__variable[name] = copy.deepcopy(data)

    def get_variable(self, name):
        if name not in self.__variable:
            return None
        return self.__variable[name]

    def execute_code(self, code):
        import mp_mephisto_language
        token_list = mp_mephisto_language.mephisto_language_lexical(code)
        code_list = mp_mephisto_language.mephisto_language_grammar(token_list)
        for each_code in code_list:
            opcode = each_code[0]
            operand = each_code[1]
            if opcode == "location":
                location_name = operand[0]
                temp_location = mp_location.Location()
                self.__world.add_location(location_name, temp_location)
            elif opcode == "set":
                location_name = operand[0]
                attribute_name = operand[1]
                data_type = operand[2]
                data = operand[3]
                if data_type == "const":
                    pass
                elif data_type == "var":
                    variable_name = data
                    data = self.get_variable(variable_name)
                else:
                    raise Exception("Invalid data type: %s" % data_type)
                if location_name == mp_configure.earth_name:
                    self.__world.set_earth_attribute(attribute_name, data)
                else:
                    self.__world.set_location_attribute(location_name, attribute_name, data)
            elif opcode == "let":
                variable_name = operand[0]
                data_type = operand[1]
                if data_type == "attr":
                    location_name = operand[2]
                    attribute_name = operand[3]
                    data = self.__world.get_location(location_name).get_by_name(attribute_name)
                    self.set_variable(variable_name, data)
                else:
                    raise Exception("Invalid data type: %s" % data_type)
            elif opcode == "event":
                location_name = operand[0]
                event_name = operand[1]
                event_function = mp_phenomenon.phenomenon_implementation(event_name)
                if event_function is None:
                    raise Exception("Phenomenon [%s] is not exist." % event_name)
                if location_name == mp_configure.earth_name:
                    event_function(self.__world.get_earth())
                else:
                    event_function(self.__world.get_location(location_name))
            elif opcode == "output":
                data_type = operand[0]
                if data_type == "attr":
                    location_name = operand[1]
                    attribute_name = operand[2]
                    if location_name == mp_configure.earth_name:
                        data = self.__world.get_earth().get_by_name(attribute_name)
                    else:
                        data = self.__world.get_location(location_name).get_by_name(attribute_name)
                    return str(data)
                elif data_type == "var":
                    variable_name = operand[0]
                    data = self.get_variable(variable_name)
                    return str(data)
                else:
                    raise Exception("Invalid data type: %s" % data_type)
            else:
                raise Exception("Invalid opcode: %s" % opcode)
