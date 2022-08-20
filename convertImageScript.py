from pydoc import ispath
import numpy as np
import cv2
import os

def convertImage(filename):
    ## process for cropping the image
    print(filename)
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

    cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnt = sorted(cnts, key=cv2.contourArea)[-1]

    x,y,w,h = cv2.boundingRect(cnt)
    img = img[y:y+h, x:x+w]
    
    ## process for scaling up the image to scale upto 1000*1000
    original_height, original_width, channels = img.shape

    ##frame_width = 1000
    ##rame_height = 1000

    scale_up_factor = 0

    if original_height > original_width:
        scale_up_factor = (725) / original_height
    else:
        scale_up_factor = (725) / original_width

    new_image_height = int(original_height * scale_up_factor)
    new_image_width = int(original_width * scale_up_factor)

    scaled_up_image = cv2.resize(img, None, fx= scale_up_factor, fy= scale_up_factor, interpolation= cv2.INTER_LINEAR)

    ## process for  framing image into 1000*1000 frame
    old_image_height, old_image_width, channels = scaled_up_image.shape
    new_image_width = 1000
    new_image_height = 1000
    color = (255,255,255)
    frame_image = np.full((new_image_height,new_image_width, channels), color, dtype=np.uint8)

    x_center = (new_image_width - old_image_width) // 2
    y_center = (new_image_height - old_image_height) // 2

    frame_image[y_center:y_center+old_image_height, 
           x_center:x_center+old_image_width] = scaled_up_image
    
    if os.path.exists('./convertedImages'):
        filename = 'convertedImages/converted_' + filename.split('/')[2]
    else:
        os.makedirs('./convertedImages')
        filename = 'convertedImages/converted_' + filename.split('/')[2]
    print(filename)
    return cv2.imwrite(filename,frame_image)

if __name__ == '__main__':
    filename = input("Enter the filename with its destination : (eg- ./folder/images.jpeg")
    convertImage(filename)
