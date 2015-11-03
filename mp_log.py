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

    def add_log(self, log_object):
        record_time = time.strftime("%Y-%m-%d %H:%M:%S")
        record_frame = inspect.currentframe().f_back
        record_code = record_frame.f_code
        caller = record_code.co_name
        filename = record_code.co_filename.split("/")[-1]
        line_number = record_code.co_firstlineno
        log_tuple = (str(record_time), str(filename), str(line_number), str(caller), str(log_object))
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
        for log in self.__log_list:
            log_text = "%s\t%s [%s:%s]\t%s\n" % (log[0], log[1], log[2], log[3], log[4])
            fp.write(log_text)

    def statistics(self, fp=sys.stdout):
        file_count_tuple_list = []
        caller_count_tuple_list = []
        for file, count in self.__log_file_count.items():
            file_count_tuple_list.append((count, file))
        for caller, count in self.__log_caller_count.items():
            caller_count_tuple_list.append((count, caller))
        file_count_tuple_list.sort()
        caller_count_tuple_list.sort()
        top_count_file = file_count_tuple_list[-1]
        top_count_caller = caller_count_tuple_list[-1]
        statistics_text = "Mephisto Logs Statistics\n"
        statistics_text += "Total Logs: %d\n" % self.__log_count
        statistics_text += "Most record file: %s [%d]\n" % (top_count_file[1], top_count_file[0])
        statistics_text += "Most record caller: %s @ %s [%d]\n" % (top_count_caller[1][1], top_count_caller[1][0], top_count_caller[0])
        fp.write(statistics_text)
