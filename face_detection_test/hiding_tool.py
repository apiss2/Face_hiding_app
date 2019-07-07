import cv2

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

    img1_bg = cv2.bitwise_and(roi,roi, mask=mask_inv)
    img2_fg = cv2.bitwise_and(t_img,t_img, mask=mask)

    dst = cv2.add(img1_bg,img2_fg)
    return dst

def put_laugh_man(image, bboxes):
    img = image.copy()
    LM = cv2.imread("./image/face.png")
    LM_size = LM.shape[1]
    for bbox in bboxes:
        size = bbox[2]-bbox[0] if (bbox[2]-bbox[0])>(bbox[3]-bbox[1]) else bbox[3]-bbox[1]
        ratio = size/LM_size
        resised_LM = cv2.resize(LM, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
        h, w, _ = resised_LM.shape
        roi = img[bbox[1]:bbox[1]+h, bbox[0]:bbox[0]+w].copy()
        roi = paste_transparent_image(roi, resised_LM)
        img[bbox[1]:bbox[1]+h, bbox[0]:bbox[0]+w] = roi
    return img
