import os
import subprocess

# file_list = os.listdir("out_original")
#
# count_true = 0
# count_false = 0
# with open("result.txt", 'w') as write_file:
#     for filename in file_list:
#         # os.system('cat out_original/test.jpg')
#         # result = subprocess.check_output(['cat out_original/test.jpg'])
#         # print(result)
#         if filename.find('\'') != -1:
#             continue
#         instruction = 'tesseract ./out_original/\'' + filename + '\'' + ' stdout -l eng+special --oem 1 --psm 3 --tessdata-dir ~/tesstutorial/engoutput'
#         result = subprocess.check_output(instruction, shell=True).decode('utf-8')
#         result = result.split("\n")[0]
#         # result = os.system((
#         #     'tesseract ./out_original/test.jpg stdout -l eng --oem 1 --psm 3 --tessdata-dir ~/tesstutorial/engoutput'))
#         # meseraic procrastinatively anatomicopathologic vetusty sparrow's
#         data = filename.split("_")[0]
#         write_file.write(data)
#         if data == result:
#             write_file.write("|True\n")
#             count_true += 1
#         else:
#             write_file.write("|False\n")
#             count_false += 1
#
# print('count true :', count_true, 'count false :', count_false)
#
#

# file_list = os.listdir("out_skewed")
#
# count_true = 0
# count_false = 0
#
# with open("result_skewed.txt", 'w') as write_file:
#     for filename in file_list:
#         # os.system('cat out_original/test.jpg')
#         # result = subprocess.check_output(['cat out_original/test.jpg'])
#         # print(result)
#         if filename.find('\'') != -1:
#             continue
#         instruction = 'tesseract ./out_skewed/\'' + filename + '\'' + ' stdout -l eng+special --oem 1 --psm 3 --tessdata-dir ~/tesstutorial/engoutput'
#         result = subprocess.check_output(instruction, shell=True).decode('utf-8')
#         result = result.split("\n")[0]
#         # result = os.system((
#         #     'tesseract ./out_original/test.jpg stdout -l eng --oem 1 --psm 3 --tessdata-dir ~/tesstutorial/engoutput'))
#         # meseraic procrastinatively anatomicopathologic vetusty sparrow's
#         data = filename.split("_")[0]
#         write_file.write(data)
#         if data == result:
#             write_file.write("|True\n")
#             count_true += 1
#         else:
#             write_file.write("|False\n")
#             count_false += 1
#
# print('count true :', count_true, 'count false :', count_false)



file_list = os.listdir("out_blub")

count_true = 0
count_false = 0

with open("result_blub.txt", 'w') as write_file:
    for filename in file_list:
        # os.system('cat out_original/test.jpg')
        # result = subprocess.check_output(['cat out_original/test.jpg'])
        # print(result)
        if filename.find('\'') != -1:
            continue
        instruction = 'tesseract ./out_blub/\'' + filename + '\'' + ' stdout -l eng+special --oem 1 --psm 3 --tessdata-dir ~/tesstutorial/engoutput'
        result = subprocess.check_output(instruction, shell=True).decode('utf-8')
        result = result.split("\n")[0]
        # result = os.system((
        #     'tesseract ./out_original/test.jpg stdout -l eng --oem 1 --psm 3 --tessdata-dir ~/tesstutorial/engoutput'))
        # meseraic procrastinatively anatomicopathologic vetusty sparrow's
        data = filename.split("_")[0]
        write_file.write(data)
        if data == result:
            write_file.write("|True\n")
            count_true += 1
        else:
            write_file.write("|False\n")
            count_false += 1

print('count true :', count_true, 'count false :', count_false)
