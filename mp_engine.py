import copy
import mp_configure
import mp_aster
import mp_location
import mp_handle
import mp_log


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
        mp_log.log.record("Set Earth Attribute: \"%s\" = %s" % (attribute_name, str(data)))
        self.__earth.set_by_name(attribute_name, data)

    def set_earth_static_attribute(self, attribute_name):
        mp_log.log.record("Set Earth Attribute Static: \"%s\"" % attribute_name)
        self.__earth.set_static_attribute(attribute_name)

    def add_location(self, name, location):
        mp_log.log.record("Add Location Entity: \"%s\"@%s" % (name, id(location)))
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
        mp_log.log.record("Set Location Attribute: (\"%s\", \"%s\") = %s" % (name, attribute_name, str(data)))
        if name in self.__location:
            self.__location[name].set_by_name(attribute_name, data)

    def set_location_static_attribute(self, name, attribute_name):
        mp_log.log.record("Set Location Attribute Static: (\"%s\", \"%s\")" % (name, attribute_name))
        if name in self.__location:
            self.__location[name].set_static_attribute(attribute_name)


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

    def opcode_location(self, operand):
        location_name = operand[0]
        temp_location = mp_location.Location()
        self.__world.add_location(location_name, temp_location)

    def opcode_init(self, operand):
        location_name = operand[0]
        attribute_name = operand[1]
        if location_name == mp_configure.earth_name:
            self.__world.set_earth_static_attribute(attribute_name)
        else:
            self.__world.set_location_static_attribute(location_name, attribute_name)
        self.opcode_set(operand)

    def opcode_set(self, operand):
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

    def opcode_let(self, operand):
        variable_name = operand[0]
        data_type = operand[1]
        if data_type == "attr":
            location_name = operand[2]
            attribute_name = operand[3]
            data = self.__world.get_location(location_name).get_by_name(attribute_name)
            self.set_variable(variable_name, data)
        elif data_type == "entity":
            entity_name = operand[2]
            data = self.__world.get_location(entity_name)
            self.set_variable(variable_name, data)
        elif data_type == "func":
            function_name = operand[2]
            argument_list = [self.get_variable(tmp_name) for tmp_name in operand[3:]]
            function_function = mp_handle.function_implementation(function_name)
            if function_function is None:
                raise Exception("Function [%s] is not exist." % function_name)
            data = function_function(*argument_list)
            self.set_variable(variable_name, data)
        else:
            raise Exception("Invalid data type: %s" % data_type)

    def opcode_event(self, operand):
        location_name = operand[0]
        event_name = operand[1]
        event_function = mp_handle.phenomenon_implementation(event_name)
        if event_function is None:
            raise Exception("Phenomenon [%s] is not exist." % event_name)
        if location_name == mp_configure.earth_name:
            event_function(self.__world.get_earth())
        else:
            event_function(self.__world.get_location(location_name))

    def opcode_action(self, operand):
        location_name = operand[0]
        action_name = operand[1]
        data_type = operand[2]
        if data_type == "const":
            data = operand[3]
        elif data_type == "attr":
            tmp_location_name = operand[3]
            tmp_attribute_name = operand[4]
            data = self.__world.get_location(tmp_location_name).get_by_name(tmp_attribute_name)
        elif data_type == "var":
            variable_name = operand[3]
            data = self.get_variable(variable_name)
        else:
            raise Exception("Invalid data type: %s" % data_type)
        action_function = mp_handle.action_implementation(action_name)
        if action_function is None:
            raise Exception("Action [%s] is not exist." % action_name)
        if location_name == mp_configure.earth_name:
            action_function(self.__world.get_earth(), data)
        else:
            action_function(self.__world.get_location(location_name), data)

    def opcode_output(self, operand):
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
            variable_name = operand[1]
            data = self.get_variable(variable_name)
            return str(data)
        else:
            raise Exception("Invalid data type: %s" % data_type)

    def execute_code(self, code):
        output_string = ""
        import mp_mephisto_language
        token_list = mp_mephisto_language.mephisto_language_lexical(code)
        mp_log.log.record("Token List: %s" % str(token_list))
        code_list = mp_mephisto_language.mephisto_language_grammar(token_list)
        mp_log.log.record("Code List: %s" % str(code_list))
        for each_code in code_list:
            opcode = each_code[0]
            operand = each_code[1]
            mp_log.log.record("Operation: %s->%s" % (str(opcode), str(operand)))
            if opcode == "location":
                self.opcode_location(operand)
            elif opcode == "init":
                self.opcode_init(operand)
            elif opcode == "set":
                self.opcode_set(operand)
            elif opcode == "let":
                self.opcode_let(operand)
            elif opcode == "event":
                self.opcode_event(operand)
            elif opcode == "action":
                self.opcode_action(operand)
            elif opcode == "output":
                output_string += self.opcode_output(operand) + " "
            else:
                raise Exception("Invalid opcode: %s" % opcode)
        return output_string
