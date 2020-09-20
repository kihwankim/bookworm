class view(object):
    def __init__(self):
        self.__capture_flag = False
        self.__voice_flag = False

    def handle_capture(self):
        pass

    def handle_voice(self):
        pass

    def print_voice(self, voice):
        pass

    def print_error(self):
        pass

    @property
    def capture_flag(self):
        return self.__capture_flag

    @property
    def voice_flag(self):
        return self.__voice_flag
