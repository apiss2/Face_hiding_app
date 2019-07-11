import cv2
import numpy as np

def draw_bbox(image, bboxes):
    for bbox in bboxes:
        cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 3, 8)
    return image

def mosaic(src, ratio=0.1):
    small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
    return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

def mosaic_area(src, bboxes, ratio=0.08):
    dst = src.copy()
    for bbox in bboxes:
        dst[bbox[1]:bbox[3], bbox[0]:bbox[2]] = mosaic(dst[bbox[1]:bbox[3], bbox[0]:bbox[2]], ratio)
    return dst

def paste_transparent_image(roi, t_img):
    img2gray = cv2.cvtColor(t_img,cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    #bug
    #同じサイズの画像が来ない場合がある
    print(roi.shape, t_img.shape)
    print(mask_inv.shape, mask.shape)

    img1_bg = cv2.bitwise_and(roi,roi, mask=mask_inv)
    img2_fg = cv2.bitwise_and(t_img,t_img, mask=mask)
    return cv2.add(img1_bg,img2_fg)

def put_image(image, bboxes, icon):
    img = image.copy()
    max_size = img.shape[0] if img.shape[0]>img.shape[1] else img.shape[1]
    LM = cv2.imread(icon)
    LM_size = LM.shape[1]
    for bbox in bboxes:
        size = bbox[2]-bbox[0] if (bbox[2]-bbox[0])>(bbox[3]-bbox[1]) else bbox[3]-bbox[1]
        if size>max_size:
            pass
        else:
            ratio = size/LM_size*1.05
            resised_LM = cv2.resize(LM, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
            h, w, _ = resised_LM.shape
            roi = img[bbox[1]:bbox[1]+h, bbox[0]:bbox[0]+w].copy()
            roi = paste_transparent_image(roi, resised_LM)
            img[bbox[1]:bbox[1]+h, bbox[0]:bbox[0]+w] = roi
    return img
