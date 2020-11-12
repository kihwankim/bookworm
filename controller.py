import os
import sys
import time
from view import view
from preprocessing import *
from translator import translator
from voice import voice
import buttons
import cv2


def button_init(event_handler):
    buttons.gpio_init()
    buttons_thread = buttons.Thread(target=buttons.thread_voice_flag, args=(1, event_handler))
    buttons_thread.start()


def main():
    event_handler = view()
    trans = translator()
    announcer = voice()
    mode = 'eng'
    button_init(event_handler)  # start button thread

    while True:
        voc_event = event_handler.voice_flag
        cap_event = event_handler.capture_flag
        ret_val, cam_img = event_handler.handle_capture()
        event_handler.show_img(cam_img) # show image for testing


        if voc_event:
            # cap_img = event_handler.handle_voice()
            cap_img = cam_img
            # cap_img = cv2.imread('./test/img/test1-eng.jpg')
            # cv2.imshow('gray', cap_img)
            # cv2.waitKey(0)
            paragraph_list, is_eng = preprocess_img(cap_img, mode=mode)

            # if is_eng:
            #     paragraph_list = trans.translate(paragraph_list, 'ko')
            paragraph_list = paragraph_list.split('\n')
            print(paragraph_list)

            ptr_voice = announcer.store_voice(paragraph_list)  # default en

            success = event_handler.print_voice(ptr_voice)

            if not success:
                event_handler.print_error()

            event_handler.set_voice_flag = False

        if cap_event:
            event_handler.handle_capture()

        time.sleep(1)


if __name__ == '__main__':
    main()
