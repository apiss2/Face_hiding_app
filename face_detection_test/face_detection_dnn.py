from __future__ import division
import cv2
import time
from hiding_tool import put_image, mosaic_area
import os
from os.path import join, dirname, abspath, normpath, exists
import datetime
from pathlib import Path

mode_dict = {0:("put","face"), 1:("put","no_photo"), 2:("put","default_icon"),
            3:("msc",0.1), 4:("msc",0.05), 5:("msc",0.2)}

def image_converter(image_path, threshold, convert_mode):
    if type(image_path) is str and type(convert_mode) is int: #入力の型チェック
        #path関係
        now_dir = Path(__file__).parent
        image_dir = join(now_dir,"image")
        save_dir = join(now_dir,"output_image")
        os.makedirs(save_dir, exist_ok=True)

        #顔検出
        image = cv2.imread(image_path)
        try:
            bboxes = face_detection(image_path, threshold=threshold)
        except:
            return [1, "DNN erroer."]

        #処理方法選択
        mode, detail = mode_dict[convert_mode]
        if mode == "put":
            icon = join(image_dir, detail+".png")
            out_image = put_image(image, bboxes, icon)
        elif mode == "msc":
            out_image = mosaic_area(image, bboxes, ratio=detail)
        else:
            print("error")
            return [0, "Unexpected hiding mode."]

        #画像の保存
        now = datetime.datetime.now()
        filename = 'img_{0:%M%S%f}.jpg'.format(now)
        saved_image_path = join(save_dir,filename)
        cv2.imwrite(saved_image_path, out_image)
        return saved_image_path
    else:
        return [0, "Unexpected input."]

def detecter(net, frame, threshold):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], False, False)

    net.setInput(blob)
    detections = net.forward()
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
    return bboxes

def face_detection(path, threshold=0.5):
    img = cv2.imread(path)
    now_dir = Path(__file__).parent
    configFile = join(now_dir, "models/SFD.prototxt")
    modelFile = join(now_dir, "models/SFD.caffemodel")
    net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
    bboxes = detecter(net, img, threshold=threshold)
    return bboxes

if __name__ == "__main__" :
    """
    a = image_converter("C:/Users/RIKI/Documents/PythonScripts/Face_hiding_app/face_detection_test/image/sample.jpg",
                    threshold=0.5, convert_mode=1)
    print(a)
    """
    t = time.time()
    image = cv2.imread("./image/sample.jpg")
    bboxes = face_detection(image, threshold=0.5)
    out_image = put_image(image, bboxes)
    #out_image = mosaic_area(image, bboxes)
    cv2.imshow("Face Detection Comparison", out_image)
    print(time.time() - t)
    cv2.waitKey(0)
    cv2.destroyAllWindows()