class Log:
    def __init__(self, file_log=False, file_log_name="log", file_log_path=""):
        self.file_log = file_log
        self.file_log_name = file_log_name
        self.file_log_path = file_log_path

    def _log_in_file(self, type_log, message):
        if self.file_log:
            with open(self.file_log_path + self.file_log_name + '.log', 'a') as log_file:
                log_file.write(f"{type_log} > {message}\n")

    def warn(self, message):
        print(f"\033[33m WRN > \033[37m{message}")
        self._log_in_file("WARNING", message)

    def error(self, message):
        print(f"\033[31m ERR > \033[37m{message}")
        self._log_in_file("ERROR", message)

    def info(self, message):
        print(f"\033[35m INF > \033[37m{message}")
        self._log_in_file("INFO", message)

    def success(self, message):
        print(f"\033[36m SUC > \033[37m{message}")
        self._log_in_file("SUCCESS", message)
