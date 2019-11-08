import cv2
import glob
import os

srcImgName = glob.glob("./datasets/img_align_celeba/*.jpg")

for i in range(len(srcImgName)):
    
    _srcImg = cv2.imread(srcImgName[i])
    name_srcImg = os.path.basename(srcImgName[i])

    imgYCC = cv2.cvtColor(_srcImg, cv2.COLOR_BGR2YCR_CB)

    y = imgYCC[:,:,0]

    cv2.imwrite("./datasets_2/img_align_celeba/" + name_srcImg, y)

    print(name_srcImg)