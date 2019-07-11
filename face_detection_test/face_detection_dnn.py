from __future__ import division
import cv2
import time
from hiding_tool import put_image, mosaic_area
from os.path import join, dirname, abspath, normpath

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

def face_detection(image, threshold=0.5):
    img = cv2.imread(image) if isinstance(image, str) else image.copy()
    configFile = normpath(join(dirname(abspath(__name__)),"models/SFD_.prototxt"))
    modelFile = normpath(join(dirname(abspath(__name__)),"models/SFD.caffemodel"))
    net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
    bboxes = detecter(net, img, threshold=threshold)
    return bboxes

if __name__ == "__main__" :
    t = time.time()
    image = cv2.imread("./image/sample.jpg")
    bboxes = face_detection(image, threshold=0.5)
    out_image = put_image(image, bboxes)
    #out_image = mosaic_area(image, bboxes)
    cv2.imshow("Face Detection Comparison", out_image)
    print(time.time() - t)
    cv2.waitKey(0)
    cv2.destroyAllWindows()