'''
可以将过大的图片放到temp里，然后使用该类进行resize
'''
import cv2
import os
# 读入图片
def resizeImage(dirPath,size=-1,factor=-1):
    '''
    :param dirPath: 需要杯处理的图片路径
    :param size: 固定图像的分辨率如（640，640）
    :param factor: 缩小的倍数
    :return:
    '''
    if not factor ==-1 and not size == -1:
        raise "resize，只可以指定size或者factor其中一个。"
    if size == -1:
        for imgP in os.listdir(dirPath):
            imgP=os.path.join(dirPath,imgP)
            img = cv2.imread(imgP)
            # 获取图片大小
            height, width = img.shape[:2]
            # 缩小图片
            smaller_img = cv2.resize(img, (int(width/factor), int(height/factor)), interpolation=cv2.INTER_AREA)
            cv2.imwrite(imgP,smaller_img)
    else:
        # size=map(int,size)
        for imgP in os.listdir(dirPath):
            imgP=os.path.join(dirPath,imgP)
            img = cv2.imread(imgP)
            # 获取图片大小
            height, width = img.shape[:2]
            # 缩小图片
            smaller_img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
            cv2.imwrite(imgP,smaller_img)
