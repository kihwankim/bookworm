import cv2
import numpy as np
import pytesseract
from imutils.object_detection import non_max_suppression

from page_dewarp import preprocessing

def load_img(path=''):
    img = cv2.imread(path)
    img = cv2.resize(img, (640, 1280), interpolation=cv2.INTER_AREA)
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
        f = open(path, 'w')
        f.write(string)
        f.close()
    except Exception as e:
        print("Failed to save the string", e)


def edge_detection(img):
    edges = cv2.Canny(img, 50, 150,apertureSize=3)
    lines = cv2.HoughLines(edges,1,np.pi/180,100,minLineLength=80,maxLineGap=5)
    return edges


def cut_half(img):
    height, width = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    # 선을 추출
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100, minLineLength=80, maxLineGap=5)
    tmp_candy = []
    tmp_abs = []

    for i in range(len(lines)):
        for x1,y1,x2,y2 in lines[i]:
            cv2.line(img, (x1,y1),(x2,y2),(0,255,0),2)
            gapY = np.abs(y2-y1)
            gapX = np.abs(x2-x1)
            # 선의 x축의 차이가 5이하 y축의 차이가 10이상이면 세로줄로 판별
            if gapX < 5 and gapY > 50 :
                tmp_candy.append(x1)
                tmp_abs.append(np.abs(x1- width//2))

    left_img = img[0:height,0:tmp_candy[np.argmin(tmp_abs)]]
    right_img = img[0:height,tmp_candy[np.argmin(tmp_abs)]+1:width]
    show_img(left_img)
    show_img(right_img)
    return left_img, right_img

def draw_boxes(img, bbox):
    x1 = min(bbox[:,0]) - 10
    if x1 < 0:
        x1 = 0
    y1 = min(bbox[:, 1]) - 10
    if y1 < 0:
        y1 = 0
    x2 = max(bbox[:, 2]) + 10
    if x2 > img.shape[1]:
        x2 = img.shape[1] - 1
    y2 = max(bbox[:, 3]) + 10
    if y2 > img.shape[0]:
        y2 = img.shape[0] - 1
    # cv2.line(img, (x2, y1), (x2, y1), (255, 255, 255), 3)
    # cv2.line(img, (x1, y2), (x1, y2), (255, 255, 255), 3)
    # cv2.line(img, (x2, y2), (x2, y2), (255, 255, 255), 3)
    # cv2.line(img, (x1, y1), (x1, y1), (255, 255, 255), 3)
    i = 1

    # bbox = sorted(bbox, key=lambda x:x[1])

    # for x1,y1,x2,y2 in bbox:
    #     cv2.rectangle(img, (x1,y1),(x2,y2),(0,i,255),1)
    #     cv2.putText(img,str(i),(x1,y1),cv2.FONT_ITALIC,0.5,(255,255,255),1)
    #     # cv2.line(img,(x1-100,y1),(x2+100,y1),(255,0,0),2)
    #     # cv2.line(img, (0, y2), (img.shape[0] + 100, y2), (0, 255, 0), 1)
    #     i += 1
    return img[y1:y2,x1:x2]
    # return img

def east(img):
    net = cv2.dnn.readNet("/home/eggbread/project/eggbread/bookworm/model/frozen_east_text_detection.pb")
    blob = cv2.dnn.blobFromImage(img, 1.0, (640, 1280), (123.68, 116.78, 103.94), True, False)
    net.setInput(blob)
    outputLayers = []
    outputLayers.append("feature_fusion/Conv_7/Sigmoid")
    outputLayers.append("feature_fusion/concat_3")
    (scores, geometry) = net.forward(outputLayers)
    (rects, confidences) = decode_predictions(scores, geometry)
    boxes = non_max_suppression(np.array(rects), probs=confidences)
    img = draw_boxes(img, boxes)
    #흑백
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #선명도
    # kernel = np.array([[0, -1, 0],
    #                    [-1, 5, -1],
    #                    [0, -1, 0]])
    # img_sharp = cv2.filter2D(imgray, -1, kernel)
    # 대비
    # img_equal = cv2.equalizeHist(imgray)
    # 이진화
    img_binary = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,99,10)
    # show_img(img)
    return img_binary


def decode_predictions(scores, geometry):
    # grab the number of rows and columns from the scores volume, then
    # initialize our set of bounding box rectangles and corresponding
    # confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the
        # geometrical data used to derive potential bounding box
        # coordinates that surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]
        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability,
            # ignore it
            if scoresData[x] < 0.3:
                continue
            # compute the offset factor as our resulting feature
            # maps will be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)
            # extract the rotation angle for the prediction and
            # then compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)
            # use the geometry volume to derive the width and height
            # of the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]
            # compute both the starting and ending (x, y)-coordinates
            # for the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)
            # add the bounding box coordinates and probability score
            # to our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])
    # return a tuple of the bounding boxes and associated confidences
    return (rects, confidences)


def run_tesseract(img):
    detected_text = pytesseract.image_to_string(img, lang='kor')
    return detected_text


if __name__ == '__main__':
    img_path = "test7-kor-left.jpg"
    img_wpath = "*thr-test7-right-kor.jpg"
    str_path = "test7-kor.txt"
    img_dir = "./img/"
    write_dir = "./result/"

    img = load_img(img_dir + img_path)
    # img = cut_half(img)
    img = east(img)
    # img = preprocessing(img)
    show_img(img)
    # img = edge_detection(img)
    string = run_tesseract(img)
    from googletrans import Translator

    translator = Translator()
    translated_string = translator.translate(string, dest='en')
    # write_img(img, write_dir + img_wpath)
    # write_string(string, write_dir+str_path)
    print(translated_string.text)
    print(string)
