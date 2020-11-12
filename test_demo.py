import cv2
import preprocessing
from gtts import gTTS

cap_img = cv2.imread('./voice/test1.png')
cv2.imshow('demo', cap_img)
cv2.waitKey(0)

result, bool_data = preprocessing.preprocess_img(cap_img, 'eng')
# result = "123\n234"
result = result.split('\n')
for each in result:
    print(each)

#
# result = ['6) Communicating', '~ (C) Answering que', '(D) Arranging mee', '', '47. How does the ertic', '\x0c']
# # result = ['\x0c']
# print(result)
# filename = 0
# # test = gTTS(text='fuck you asswhole')
# # test.save('fuckyou.mp3')
#
# for paragraph in result:
#     data = ''
#     for each_data in paragraph:
#         if each_data == ' ':
#             if data == '':
#                 continue
#             else:
#                 data += each_data
#         elif 'a' <= each_data <= 'z' or 'A' <= each_data <= 'Z' or '0' <= each_data <= '9':
#             data += each_data
#     if data == '':
#         continue
#     filename += 1
#     print(data)
#     tts = gTTS(text=data)
#     tts.save(str(filename) + ".mp3")
#     print("save all")
