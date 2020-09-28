import cv2
import numpy as np
import pytesseract


def load_img(path=''):
    img = cv2.imread(path)
    return img


def show_img(img):
    cv2.namedWindow('test')
    cv2.imshow('test', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def write_img(img=None, path=''):
    try:
        cv2.imwrite(path, img)
    except Exception as e:
        print("Failed to save the img", e)


def write_string(string='', path=''):
    try:
        f = open(path,'w')
        f.write(string)
        f.close()
    except Exception as e:
        print("Failed to save the string", e)

def contour(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 200, 255, 0)
    # image, contours, h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # image = cv2.drawContours(img, contours, -1, (0,255,0),3)
    show_img(thresh)
    return thresh


def run_tesseract(img):
    detected_text = pytesseract.image_to_string(img)
    return detected_text


if __name__ == '__main__':
    img_path = "test3-eng.jpg"
    str_path = "test3-eng.txt"
    img_dir = "./img/"
    write_dir = "./result/"

    img = load_img(img_dir + img_path)
    contour_img = contour(img)
    string = run_tesseract(img)

    write_img(contour_img, write_dir + img_path)
    write_string(string, write_dir+str_path)
    print(string)
