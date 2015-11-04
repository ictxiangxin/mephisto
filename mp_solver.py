import mp_tokenize
import mp_question_parser
import mp_engine
import mp_date_time
import mp_location
import mp_data
import mp_log


def normal_solver(question_text):
    try:
        engine = mp_engine.MephistoEngine()
        token_list = mp_tokenize.tokenize(question_text)
        mp_log.log.record("Token List: %s" % str(token_list))
        city_set = set()
        location_set = set()
        atom_semantic_action = []
        nearest_location = None
        temp_variable_number = 0
        phrase = []
        for token in token_list:
            if token[0] in ["separator", "$"]:
                phrase.append(("$", ""))
                try:
                    mp_log.log.record("Phrase Token List: %s" % str(phrase))
                    grammar = mp_question_parser.mephisto_question_grammar(phrase)
                    mp_log.log.record("Grammar: %s" % str(grammar))
                except:
                    phrase = []
                    continue
                for operation in grammar:
                    opcode = operation[0]
                    operand = operation[1:]
                    mp_log.log.record("Operation: %s->%s" % (str(opcode), str(operand)))
                    if opcode == "set":
                        data_type = operand[0]
                        location = operand[1]
                        data = operand[2]
                        nearest_location = location
                        location_set.add(location[1])
                        if location[0] == "city":
                            city_set.add(location[1])
                        if data_type == "datetime":
                            if isinstance(data, tuple):
                                date = data[0]
                                time = data[1]
                            elif isinstance(data, mp_date_time.Date):
                                date = data
                                time = None
                            elif isinstance(data, mp_date_time.Time):
                                date = None
                                time = data
                            else:
                                date = None
                                time = None
                            if time is not None:
                                action = "(set, \"%s\", \"local_time\", \"const\", \"%s\")" % (location[1], str(time))
                                atom_semantic_action.append(action)
                            if date is not None:
                                action = "(set, \"%s\", \"local_date\", \"const\", \"%s\")" % (location[1], str(date))
                                atom_semantic_action.append(action)
                        elif data_type == "position":
                            if location[0] == "anonymous":
                                if isinstance(data, tuple):
                                    longitude = data[0]
                                    latitude = data[1]
                                elif isinstance(data, mp_location.Longitude):
                                    longitude = data
                                    latitude = None
                                elif isinstance(data, mp_location.Latitude):
                                    longitude = None
                                    latitude = data
                                else:
                                    longitude = None
                                    latitude = None
                                if longitude is not None:
                                    action = "(set, \"%s\", \"longitude\", \"const\", \"%s\")" % (location[1], str(longitude))
                                    atom_semantic_action.append(action)
                                if latitude is not None:
                                    action = "(set, \"%s\", \"latitude\", \"const\", \"%s\")" % (location[1], str(latitude))
                                    atom_semantic_action.append(action)
                        else:
                            action = "(set, \"%s\", \"%s\", \"const\", \"%s\")" % (location[1], data_type, str(data))
                            atom_semantic_action.append(action)
                    elif opcode == "indirect_set":
                        location = operand[0]
                        attribute = operand[1]
                        city = "_" + operand[2]
                        time = operand[3]
                        nearest_location = location
                        location_set.add(location[1])
                        location_set.add(city[1])
                        if location[0] == "city":
                            city_set.add(location[1])
                        city_set.add(city[1])
                        action = "(set, \"%s\", \"local_time\", \"const\", \"%s\")" % (city[1], str(time))
                        atom_semantic_action.append(action)
                        temp_number = temp_variable_number
                        temp_variable_number += 1
                        action = "(let, \"tmp%d\", \"attr\", \"%s\", \"local_time\")" % (temp_number, location[1])
                        atom_semantic_action.append(action)
                        action = "(set, \"%s\", \"%s\", \"var\", \"tmp%d\")" % (location[1], attribute, temp_number)
                        atom_semantic_action.append(action)
                    elif opcode == "get":
                        location = operand[0]
                        attribute = operand[1]
                        if location[0] == "!":
                            location = nearest_location
                        if location is None:
                            raise Exception("Can not solve this question")
                        location_set.add(location[1])
                        if location[0] == "city":
                            city_set.add(location[1])
                        action = "(output, \"attr\", \"%s\", \"%s\")" % (location[1], attribute)
                        atom_semantic_action.append(action)
                    elif opcode == "indirect_get":
                        location = operand[0]
                        attribute = operand[1]
                        city = "_" + operand[2]
                        location_set.add(location[1])
                        location_set.add(city[1])
                        if location[0] == "city":
                            city_set.add(location[1])
                        city_set.add(city[1])
                        temp_number = temp_variable_number
                        temp_variable_number += 1
                        action = "(let, \"tmp%d\", \"attr\", \"%s\", \"%s\")" % (temp_number, location[1], attribute)
                        atom_semantic_action.append(action)
                        action = "(set, \"%s\", \"local_time\", \"var\", \"tmp%d\")" % (location[1], temp_number)
                        atom_semantic_action.append(action)
                        action = "(output, \"attr\", \"%s\", \"local_time\")" % city[1]
                        atom_semantic_action.append(action)
                    elif opcode == "event":
                        location = operand[0]
                        phenomenon = operand[1]
                        if location[0] == "!":
                            location = nearest_location
                        if location is None:
                            raise Exception("Can not solve this question")
                        location_set.add(location[1])
                        if location[0] == "city":
                            city_set.add(location[1])
                        action = "(event, \"%s\", \"%s\")" % (location[1], phenomenon)
                        atom_semantic_action.append(action)
                    elif opcode == "lapse":
                        time = operand[0]
                        location = nearest_location
                        if location is None:
                            raise Exception("Can not solve this question")
                        location_set.add(location[1])
                        if location[0] == "city":
                            city_set.add(location[1])
                        action = "(action, \"%s\", \"time_forward\", \"const\", \"%s\")" % (location[1], time)
                        atom_semantic_action.append(action)
                    elif opcode == "move":
                        data = operand[0]
                        location = nearest_location
                        if location is None:
                            raise Exception("Can not solve this question")
                        location_set.add(location[1])
                        if location[0] == "city":
                            city_set.add(location[1])
                        if isinstance(data, tuple):
                            longitude = data[0]
                            latitude = data[1]
                        elif isinstance(data, mp_location.Longitude):
                            longitude = data
                            latitude = None
                        elif isinstance(data, mp_location.Latitude):
                            longitude = None
                            latitude = data
                        else:
                            longitude = None
                            latitude = None
                        if longitude is not None:
                            action = "(set, \"%s\", \"longitude\", \"const\", \"%s\")" % (location[1], str(longitude))
                            atom_semantic_action.append(action)
                        if latitude is not None:
                            action = "(set, \"%s\", \"latitude\", \"const\", \"%s\")" % (location[1], str(latitude))
                            atom_semantic_action.append(action)
                    elif opcode == "geo":
                        geo_type = operand[0]
                        slave_location = operand[1]
                        main_location = operand[2]
                        slave_number = temp_variable_number
                        temp_variable_number += 1
                        main_number = temp_variable_number
                        temp_variable_number += 1
                        location_set.add(slave_location[1])
                        location_set.add(main_location[1])
                        if slave_location[0] == "city":
                            city_set.add(slave_location[1])
                        if main_location[0] == "city":
                            city_set.add(main_location[1])
                        action = "(let, \"tmp%d\", \"entity\", \"%s\")" % (main_number, main_location[1])
                        atom_semantic_action.append(action)
                        action = "(let, \"tmp%d\", \"entity\", \"%s\")" % (slave_number, slave_location[1])
                        atom_semantic_action.append(action)
                        output_number = temp_variable_number
                        temp_variable_number += 1
                        if geo_type == "direction":
                            action = "(let, \"tmp%d\", \"func\", \"direction\", \"tmp%d\", \"tmp%d\")" % (output_number, main_number, slave_number)
                            atom_semantic_action.append(action)
                            action = "(output, \"var\", \"tmp%d\")" % output_number
                            atom_semantic_action.append(action)
                        else:
                            raise Exception("Invalid geography type: %s" % geo_type)
                    elif opcode == "metric":
                        metric_type = operand[0]
                        slave_location = operand[1]
                        main_location = operand[2]
                        slave_number = temp_variable_number
                        temp_variable_number += 1
                        main_number = temp_variable_number
                        temp_variable_number += 1
                        location_set.add(slave_location[1])
                        location_set.add(main_location[1])
                        if slave_location[0] == "city":
                            city_set.add(slave_location[1])
                        if main_location[0] == "city":
                            city_set.add(main_location[1])
                        action = "(let, \"tmp%d\", \"entity\", \"%s\")" % (main_number, main_location[1])
                        atom_semantic_action.append(action)
                        action = "(let, \"tmp%d\", \"entity\", \"%s\")" % (slave_number, slave_location[1])
                        atom_semantic_action.append(action)
                        output_number = temp_variable_number
                        temp_variable_number += 1
                        if metric_type == "distance":
                            action = "(let, \"tmp%d\", \"func\", \"distance\", \"tmp%d\", \"tmp%d\")" % (output_number, main_number, slave_number)
                            atom_semantic_action.append(action)
                            action = "(output, \"var\", \"tmp%d\")" % output_number
                            atom_semantic_action.append(action)
                        else:
                            raise Exception("Invalid metric type: %s" % metric_type)
                    else:
                        raise Exception("Invalid opcode: %s" % opcode)
                phrase = []
            else:
                phrase.append(token)
        for city in city_set:
            location_info = mp_data.city_coordinate(city)
            longitude = location_info[0]
            latitude = location_info[1]
            action = "(init, \"%s\", \"latitude\", \"const\", \"%s\")" % (city, latitude)
            atom_semantic_action.insert(0, action)
            action = "(init, \"%s\", \"longitude\", \"const\", \"%s\")" % (city, longitude)
            atom_semantic_action.insert(0, action)
        for location in location_set:
            action = "(location, \"%s\")" % location
            atom_semantic_action.insert(0, action)
        final_atom_semantic_action = "\n".join(atom_semantic_action)
        mp_log.log.record(final_atom_semantic_action)
        result = engine.execute_code(final_atom_semantic_action)
        if result == "":
            return None
        return result
    except Exception:
        return None
