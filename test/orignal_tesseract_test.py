import os

try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract

# 영어 인식
dir_list = os.listdir('out_original')

true_count = 0
false_count = 0
with open("before_result_original.txt", 'w') as result_file:
    for file_name in dir_list:
        if file_name.find('\'') != -1:
            continue
        img = Image.open('out_original/' + file_name)
        tesseract_result = pytesseract.image_to_string(img).split("\n")[0]
        print(tesseract_result)
        if tesseract_result == file_name.split("_")[0]:
            result_file.write(file_name + "|True\n")
            true_count += 1
        else:
            false_count += 1
            result_file.write(file_name + "|False\n")

print(true_count, ", ", false_count)

# 한글
# print(pytesseract.image_to_string(Image.open('hangul.png'), lang='Hangul'))
