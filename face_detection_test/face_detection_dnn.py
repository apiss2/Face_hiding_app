from __future__ import division
import cv2
import time
import sys
from hiding_tool import put_laugh_man, mosaic_area

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
    return frameOpencvDnn, bboxes

def face_detection(image, model="TF", threshold=0.5,file_dir="./models/"):
    image = cv2.imread(image) if isinstance(image, str) else image
    DNN = "CAFFE"
    if DNN == "CAFFE":
        modelFile = "res10_300x300_ssd_iter_140000_fp16.caffemodel"
        configFile = "models/deploy.prototxt"
        net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
    else:
        modelFile = "models/opencv_face_detector_uint8.pb"
        configFile = "models/opencv_face_detector.pbtxt"
        net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

    outOpencvDnn, bboxes = detecter(net,image, threshold=threshold)

    return image

if __name__ == "__main__" :

    t = time.time()
    image = cv2.imread("./image/190707_0003.jpg")
    DNN = "CAFFE"
    if DNN == "CAFFE":
        modelFile = "models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
        configFile = "models/deploy.prototxt"
        net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
    else:
        modelFile = "models/opencv_face_detector_uint8.pb"
        configFile = "models/opencv_face_detector.pbtxt"
        net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

    outOpencvDnn, bboxes = detecter(net,image, threshold=0.5)
    #outOpencvDnn = put_laugh_man(outOpencvDnn, bboxes)
    outOpencvDnn = mosaic_area(outOpencvDnn, bboxes)
    cv2.imshow("Face Detection Comparison", outOpencvDnn)
    print(time.time() - t)
    cv2.waitKey(0)
    cv2.destroyAllWindows()