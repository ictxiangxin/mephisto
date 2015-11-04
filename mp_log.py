import time
import inspect
import sys


class MephistoLog:
    def __init__(self):
        self.__log_list = []
        self.__log_detail = {}
        self.__log_file_count = {}
        self.__log_caller_count = {}
        self.__log_count = 0

    def record(self, log_object):
        record_time = time.strftime("%Y-%m-%d %H:%M:%S")
        record_frame = inspect.currentframe().f_back
        record_code = record_frame.f_code
        caller = record_code.co_name
        filename = record_code.co_filename.split("/")[-1].split("\\")[-1]
        function_line_number = record_code.co_firstlineno
        code_line_number = record_frame.f_lineno
        log_object_string = str(log_object)
        if "\n" in log_object_string:
            log_object_string = "\n" + log_object_string
            log_object_string = log_object_string.replace("\n", "\n    ")
        log_tuple = (str(record_time), str(filename), str(function_line_number), str(caller), str(code_line_number), log_object_string)
        self.__log_list.append(log_tuple)
        if filename not in self.__log_detail:
            self.__log_detail[filename] = {}
        if caller not in self.__log_detail[filename]:
            self.__log_detail[filename][caller] = 0
        self.__log_detail[filename][caller] += 1
        if filename not in self.__log_file_count:
            self.__log_file_count[filename] = 0
        self.__log_file_count[filename] += 1
        if (filename, caller) not in self.__log_caller_count:
            self.__log_caller_count[(filename, caller)] = 0
        self.__log_caller_count[(filename, caller)] += 1
        self.__log_count += 1

    def output(self, fp=sys.stdout):
        fp.write("================================ Mephisto Logs Record ================================\n")
        for log in self.__log_list:
            log_text = "%s\t%s [%s:%s] <%s>\t%s\n" % (log[0], log[1], log[2], log[3], log[4], log[5])
            fp.write(log_text)

    def statistics(self, fp=sys.stdout):
        file_count_tuple_list = []
        caller_count_tuple_list = []
        for file, count in self.__log_file_count.items():
            file_count_tuple_list.append((count, file))
        for caller, count in self.__log_caller_count.items():
            caller_count_tuple_list.append((count, caller))
        file_count_tuple_list.sort(reverse=True)
        caller_count_tuple_list.sort(reverse=True)
        top_count_file = file_count_tuple_list[0]
        top_count_caller = caller_count_tuple_list[0]
        top10_count_file = file_count_tuple_list[:10]
        top10_count_caller = caller_count_tuple_list[:10]
        average_count_file = sum([file_count[0] for file_count in file_count_tuple_list]) / len(file_count_tuple_list)
        average_count_caller = sum([caller_count[0] for caller_count in caller_count_tuple_list]) / len(caller_count_tuple_list)
        statistics_text = "================================ Mephisto Logs Statistics ================================\n"
        statistics_text += "    Total Logs: %d\n" % self.__log_count
        statistics_text += "    Average record per file: %f\n" % average_count_file
        statistics_text += "    Average record per caller: %f\n" % average_count_caller
        statistics_text += "    Most record file: %s [%d]\n" % (top_count_file[1], top_count_file[0])
        statistics_text += "    Most record caller: %s @ %s [%d]\n" % (top_count_caller[1][1], top_count_caller[1][0], top_count_caller[0])
        statistics_text += "<Top %d record file>\n" % len(top10_count_file)
        for file_count in top10_count_file:
            statistics_text += "    %d\t\t%s\n" % (file_count[0], file_count[1])
        statistics_text += "<Top %d record caller>\n" % len(top10_count_file)
        for caller_count in top10_count_caller:
            statistics_text += "    %d\t\t%s @ %s\n" % (caller_count[0], caller_count[1][1], caller_count[1][0])
        fp.write(statistics_text)


log = MephistoLog()
