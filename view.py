import os


class view(object):
    def __init__(self):
        self.__capture_flag = False
        self.__voice_flag = False

    def handle_capture(self):
        pass

    def handle_voice(self):
        pass

    def print_voice(self, voice_filename):
        base = './voice/'
        for filename in range(1, voice_filename + 1):
            os.system("mpg123 " + base + str(filename) + ".mp3")

    def print_error(self):
        pass

    @property
    def capture_flag(self):
        return self.__capture_flag

    @property
    def voice_flag(self):
        return self.__voice_flag
