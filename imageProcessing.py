import cv2 as cv
import numpy as np
from PIL import Image

carousel = ((204,102,255),(0,255,0), (204,102,51), (255,153,51), (102,255,255), (255, 204, 51))

def processMask(raw_mask):
    x = 0
    mask = []
    for i in range(0,len(raw_mask)):
        if i&1:
            mask.append([x,raw_mask[i]])
        else:
            x = raw_mask[i]
    mask = np.array(mask, np.int32)
    mask = mask.reshape(-1,1,2)
    return mask

def drawTransparentMask(img, raw_masks, color):
    b = 0
    g = 0
    r = 0
    if color == 0:
        b = 255
    elif color == 1:
        g = 255
    else:
        r = 255
    for raw_mask in raw_masks['segmentation']:
        mask = processMask(raw_mask)
        overlay = img.copy()
        output = img.copy()
        cv.polylines(output,[mask],True,(b,g,r))
        #cv.drawContours(overlay,[mask],-1,(b,g,r),-1,cv.LINE_AA)
    #cv.addWeighted(overlay,0.5,output,1-0.5,0,output)
    #Criar uma imagem a partir do output em forma de mosaico
    #Olhar codigo do professor em caso de duvida
    x,y,w,h = [int(x) for x in raw_masks['bbox']]
    return cv.resize(output[y:y+h,x:x+w],(75,75),interpolation=cv.INTER_CUBIC)
    # return res_img+output[y:h, x:w]

def findMinMaxXY(npArrayOfArrays):
    minX = npArrayOfArrays[0][0][0]
    minY = npArrayOfArrays[0][0][1]
    maxX = npArrayOfArrays[0][0][0]
    maxY = npArrayOfArrays[0][0][1]
    i  = 1
    while i < len(npArrayOfArrays):
        data = npArrayOfArrays[i][0]
        if minX > data[0]:
            minX = data[0]
        if minY > data[1]:
            minY = data[1]
        if maxX < data[0]:
            maxX = data[0]
        if maxY < data[1]:
            maxY = data[1]
        i = i + 1
    return minX, minY, maxX, maxY

def drawMask(img, raw_masks, color = carousel[0]):
    orig = img.copy()
    count = 0

    min_x = 100000
    min_y = 100000
    max_x = -1
    max_y = -1
    for raw_mask in raw_masks['segmentation']:
        mask = processMask(raw_mask)
        aux_min_x, aux_min_y, aux_max_x, aux_max_y = findMinMaxXY(mask)
        if min_x > aux_min_x:
            min_x = aux_min_x
        if min_y > aux_min_y:
            min_y = aux_min_y
        if max_x < aux_max_x:
            max_x = aux_max_x
        if max_y < aux_max_y:
            max_y = aux_max_y

        cv.drawContours(img,[mask],-1,color,-1,cv.LINE_AA)
        count = count + 1

    if count > 1:
        cv.rectangle(img, (min_x, max_y), (max_x, min_y), (255, 255, 255), 2)


    # b,g,r = [0,0,0]
    # if status == 0:
    #     g = 1
    # elif status == 1:
    #     r = 1
    # else:
    #     g = 1
    #     r = 1
    #cv.polylines(img, [mask], True, (b*255, g*255, r*255))
    #cv.polylines(img, [mask], True, (0, (not (status&1))*255, bool(status)*255))
    #Desenhar com cv.contour ou algo assim
    cv.addWeighted(orig,0.4,img,0.6,0.0,img)
    return img

def openImage(image_path):
    return cv.imread(image_path, -1)

def originalImage(tmp_img_path, image_path):
    cv.imwrite(tmp_img_path, cv.imread(image_path, -1))

def vconcat_resize(img_list, interpolation=cv.INTER_CUBIC):
    w_min = min(img.shape[1] for img in img_list)
    im_list_resize = [cv.resize(img,(w_min, int(img.shape[0]*w_min/img.shape[1])), interpolation=interpolation) for img in img_list]
    return cv.vconcat(im_list_resize)

def hconcat_resize(img_list, interpolation=cv.INTER_CUBIC):
    h_min = min(img.shape[0] for img in img_list)
    im_list_resize = [cv.resize(img,(int(img.shape[1]*h_min/img.shape[0]),h_min), interpolation=interpolation) for img in img_list]
    return cv.hconcat(im_list_resize)

def drawMosaic(list_2d, interpolation=cv.INTER_CUBIC):
    img_list_v = [hconcat_resize(list_h) for list_h in list_2d]
    return vconcat_resize(img_list_v)

def drawMasks(image_path, tmp_img_path, tmp_img_path2, annotationsRectangle, raw_masks):
    img = openImage(image_path)
    img2 = img.copy()
    res_img = []
    z = 0
    color = 0
    colorMask = 0
    modMask = len(carousel)
    for raw_mask in raw_masks:
        res_img.append(drawTransparentMask(img, raw_mask, color))
        z+=1
        img2 = drawMask(img2, raw_mask, carousel[colorMask])
        color = (color+1)%3
        colorMask = (colorMask + 1)%modMask
    list_2d = []
    z = 0
    num_imgs_per_row = 13
    num_rows = len(res_img)//num_imgs_per_row
    if (len(res_img)%num_imgs_per_row != 0): num_rows+=1
    if num_rows == 0: num_rows=1
    b_im = np.zeros((75,75,3), dtype="uint8")
    for i in range(0,num_rows):
        list_2d.append([])
        for j in range(0,num_imgs_per_row):
            if (z < len(res_img)):
                list_2d[i].append(res_img[z])
                z+=1
            else:
                list_2d[i].append(b_im)
    cv.imwrite(tmp_img_path, drawMosaic(list_2d))#cv.resize(drawMosaic(list_2d),(1280,720),interpolation=cv.INTER_CUBIC))
    #cv.imwrite(tmp_img_path, img)
    x0,y0,w,h = annotationsRectangle
    x1 = x0 + w
    y1 = y0 + h

    cv.line(img2,(x0,y0),(x1,y0),(0,0,0),1);
    cv.line(img2,(x1,y0),(x1,y1),(0,0,0),1);
    cv.line(img2,(x1,y1),(x0,y1),(0,0,0),1);
    cv.line(img2,(x0,y1),(x0,y0),(0,0,0),1);
    cv.imwrite(tmp_img_path2, img2)
