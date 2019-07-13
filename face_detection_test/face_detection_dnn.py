from __future__ import division
import cv2
import time
from hiding_tool import put_image, mosaic_area
import os
from os.path import join, dirname, abspath, normpath, exists
import datetime
from pathlib import Path

def image_converter(image_path, threshold, convert_mode):
    result={"status": "erorr", "path": None, "error_message": None}
    mode_dict = {0:("put","face"), 1:("put","no_photo"), 2:("put","default_icon"),
                3:("msc",0.1), 4:("msc",0.05), 5:("msc",0.01)}

    try:
        if not (type(image_path) is str and type(threshold) is int and type(convert_mode) is int): #入力の型チェック
            result["error_message"]="Unexpected inputs"
            return result

        #path関係
        now_dir = Path(__file__).parent
        image_dir = join(now_dir,"image")
        save_dir = join(now_dir,"output_image")
        os.makedirs(save_dir, exist_ok=True)

        #顔検出
        image = cv2.imread(image_path)
        if image is None:
            result["error_message"]="No such file or directory"
            return result

        try:
            bboxes = face_detection(image_path, threshold=(((10-threshold)+1)*0.05))
        except:
            result["error_message"] = "DNN error"
            return result

        #処理方法選択
        mode, detail = mode_dict[convert_mode]
        if mode == "put":
            icon = join(image_dir, detail+".png")
            try:
                image = mosaic_area(image, bboxes, ratio=0.08)
                out_image = put_image(image, bboxes, icon)
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

        #画像名作成
        filename = 'img_{0:%M%S%f}.jpg'.format(datetime.datetime.now())
        saved_image_path = join(save_dir,filename)
        #画像の保存
        try:
            cv2.imwrite(saved_image_path, out_image)
            result["status"] = "success"
            result["path"] = abspath(saved_image_path)
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

def face_detection(path, threshold=0.5):
    img = cv2.imread(path)
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