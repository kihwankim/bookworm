import os
import cv2


class view(object):
    def __init__(self):
        self.__capture_flag = False
        self.__voice_flag = False
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 1280)  # CV_CAP_PROP_FRAME_WIDTH
        self.cam.set(4, 720)  # CV_CAP_PROP_FRAME_HEIGHT

    def handle_capture(self):
        return self.cam.read()

    def show_img(self, img):
        cv2.imshow('frame', img)
        cv2.waitKey(1)

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

    @voice_flag.setter
    def set_voice_flag(self, voice):
        self.__voice_flag = voice
