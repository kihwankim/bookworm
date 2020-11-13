import cv2
from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract

MARGIN = 10


def detect_text_area(img):
    net = cv2.dnn.readNet("./frozen_east_text_detection.pb")
    blob = cv2.dnn.blobFromImage(img, 1.0, (640, 1280), (123.68, 116.78, 103.94), True, False)
    net.setInput(blob)
    outputLayers = []
    outputLayers.append("feature_fusion/Conv_7/Sigmoid")
    outputLayers.append("feature_fusion/concat_3")
    (scores, geometry) = net.forward(outputLayers)
    (rects, confidences) = decode_predictions(scores, geometry)
    boxes = non_max_suppression(np.array(rects), probs=confidences)
    return crop(img, boxes)


def img_makeup(img):
    # grayscale
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 선명도
    # kernel = np.array([[0, -1, 0],
    #                    [-1, 5, -1],
    #                    [0, -1, 0]])
    # img_sharp = cv2.filter2D(imgray, -1, kernel)
    # 대비
    # img_equal = cv2.equalizeHist(imgray)
    # 이진화
    img_binary = cv2.adaptiveThreshold(imgray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 99, 10)
    return img_binary


def crop(img, bbox):
    x1 = min(bbox[:, 0]) - MARGIN
    if x1 < 0:
        x1 = 0
    y1 = min(bbox[:, 1]) - MARGIN
    if y1 < 0:
        y1 = 0
    x2 = max(bbox[:, 2]) + MARGIN
    if x2 > img.shape[1]:
        x2 = img.shape[1] - 1
    y2 = max(bbox[:, 3]) + MARGIN
    if y2 > img.shape[0]:
        y2 = img.shape[0] - 1

    return img[y1:y2, x1:x2]


def run_tesseract(img, mode='kor'):
    detected_text = pytesseract.image_to_string(img, lang=mode)
    return detected_text


def decode_predictions(scores, geometry):
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    for y in range(0, numRows):
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]
        for x in range(0, numCols):
            if scoresData[x] < 0.3:
                continue
            (offsetX, offsetY) = (x * 4.0, y * 4.0)
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])
    return rects, confidences


def check_language(extracted_text):
    k_cnt = 0
    e_cnt = 0
    for s in extracted_text:
        if ord('가') <= ord(s) <= ord('힣'):
            k_cnt += 1
        elif ord('a') <= ord(s.lower()) <= ord('z'):
            e_cnt += 1

    if (k_cnt + e_cnt) == 0:
        return 0
    return k_cnt / (k_cnt + e_cnt), e_cnt / (k_cnt + e_cnt)


def preprocess_img(img, mode):
    detected_img = detect_text_area(img)
    makeup_img = img_makeup(detected_img)
    cv2.imwrite('./test.jpg', makeup_img)
    extracted_text = run_tesseract(makeup_img, mode)
    prob_k, prob_e = check_language(extracted_text)
    if prob_k > prob_e:
        return extracted_text, False
    else:
        return extracted_text, True
