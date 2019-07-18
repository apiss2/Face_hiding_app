from __future__ import division
import cv2
import time
from .hiding_tool import put_image, mosaic_area
import os
from os.path import join, dirname, abspath, normpath, exists
from pathlib import Path
from django.conf import settings

def image_converter(input_path, output_path, threshold, convert_mode):
    result={"status": "erorr", "error_message": None}
    mode_dict = {0:("put","face"), 1:("put","no_photo"), 2:("put","default_icon"),
                3:("msc",0.1), 4:("msc",0.05), 5:("msc",0.01)}

    try:
        if not (type(input_path) is str and type(output_path) is str \
                and type(threshold) is int and type(convert_mode) is int): #入力の型チェック
            result["error_message"]="Unexpected inputs"
            return result

        #顔検出
        image = cv2.imread(input_path)
        if image is None:
            result["error_message"]="No such image file or directory"
            return result

        try:
            bboxes = face_detection(image, threshold=((11-threshold)*0.05))
        except:
            result["error_message"] = "DNN error"
            return result

        #処理方法選択
        mode, detail = mode_dict[convert_mode]
        if mode == "put":
            icon_path = settings.BASE_DIR + f"/media/icons/{detail}.png"
            try:
                image = mosaic_area(image, bboxes, ratio=0.08)
                out_image = put_image(image, bboxes, icon_path)
            except:
                result["error_message"] = "Failed to combine images"
                return result
        elif mode == "msc":
            try:
                out_image = mosaic_area(image, bboxes, ratio=detail)
            except:
                result["error_message"] = "Failed to combine images"
                return result
        else:
            result["error_message"] = "Unexpected inputs (convert_mode)"
            return result

        #画像の保存
        try:
            cv2.imwrite(output_path, out_image)
            result["status"] = "success"
            return result
        except:
            result["error_message"] = "Failed to save image"
            return result
    except:
        result["error_message"] = "Unknown error"
        return result

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

def face_detection(img, threshold=0.5):
    now_dir = Path(__file__).parent
    configFile = join(now_dir, "models/SFD.prototxt")
    modelFile = join(now_dir, "models/SFD.caffemodel")
    net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
    bboxes = detecter(net, img, threshold=threshold)
    return bboxes

if __name__ == "__main__" :
    a = image_converter("./image/sample.jpg",
                    threshold=1, convert_mode=3)
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
    """