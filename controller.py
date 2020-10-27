import os
import sys
import time
from view import view
from preprocessing import *
from translator import translator
from voice import voice


def main():
    event_handler = view()
    trans = translator()
    announcer = voice()
    mode = 'kor'
    while True:
        voc_event = event_handler.voice_flag
        cap_event = event_handler.capture_flag

        if voc_event:
            cap_img = event_handler.handle_voice()
            paragraph_list, is_eng = preprocess_img(cap_img, mode=mode)

            if is_eng:
                paragraph_list = trans.translate(paragraph_list, 'ko')

            ptr_voice = announcer.store_voice(paragraph_list)  # default en

            success = event_handler.print_voice(ptr_voice)

            if not success:
                event_handler.print_error()

        if cap_event:
            event_handler.handle_capture()

        time.sleep(1)


if __name__ == '__main__':
    main()
