import RPi.GPIO as GPIO
import sys
import threading
import time

but_pin2 = 16


class StopThread(StopIteration):
    pass


threading.SystemExit = SystemExit, StopThread


class Thread(threading.Thread):
    def _bootstrap(self, stop_thread=False):
        def stop():
            nonlocal stop_thread
            stop_thread = True

        self.stop = stop

        def tracer(*_):
            if stop_thread:
                raise StopThread()
            return tracer

        sys.settrace(tracer)
        super()._bootstrap()


def gpio_init():
    GPIO.setmode(GPIO.BOARD)
    # GPIO.setup(but_pin2, GPIO.IN)
    # GPIO.add_event_detect(but_pin2, GPIO.FALLING)


def thread_voice_flag(id, view):
    but_pin = 12
    try:
        GPIO.setup(but_pin, GPIO.IN)
        GPIO.add_event_detect(but_pin, GPIO.FALLING)

        while True:
            if GPIO.event_detected(but_pin):
                view.set_voice_flag = True
    except:
        pass
    finally:
        GPIO.cleanup(but_pin)
