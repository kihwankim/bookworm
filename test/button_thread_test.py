import RPi.GPIO as GPIO
import sys
import threading
import time

but_pin = 12
but_pin2 = 16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(but_pin, GPIO.IN)
GPIO.setup(but_pin2, GPIO.IN)
GPIO.add_event_detect(but_pin, GPIO.FALLING)
GPIO.add_event_detect(but_pin2, GPIO.FALLING)

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

def main():
    while True:
        test1 = Thread(target=printer)
        if GPIO.event_detected(but_pin):
            test1.start()
            while True:
                if GPIO.event_detected(but_pin2):
                    test1.stop()
                    print('stopped')
                    test1.join()
                    break


def printer():
    while True:
        print(time.time() % 1)
        time.sleep(0.5)




if __name__ == '__main__':
    main()
