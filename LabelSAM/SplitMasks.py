'''
分割一个幕布上的所有目标.
'''
import json
import os
from os.path import join as pathjoin
import numpy as np
from PIL import Image

def saveForce(img,path):#不重复的存储图片
    respath = path
    for i in range(1000):
        if os.path.exists(respath) == True:
            dir,f=os.path.split(path)
            f='.'.join(f.split('.')[:-1])+str(i)+'.'+f.split('.')[-1]
            respath=pathjoin(dir,f)
            # print(path)
        else:
            break
    img.save(respath)
def splitExp(imagesPath,labelsPath,savePath):
    # labelsPath=r'D:\Desktop\1.WheatCounting\Detect\yolov5-master\yolov5-master\runs\MyOperation\SAM_labels\labels\train'
    # imagePath=r'D:\Desktop\1.WheatCounting\Detect\yolov5-master\yolov5-master\runs\MyOperation\SAM_labels\images\train'
    # savePath='./AfterSpliting'#todo 保存分割后图像的路径
    imgs=[Image.open(pathjoin(imagesPath,img)) for img in os.listdir(imagesPath) if not len(img.split('.')) ==1 ]#所有图片（原图）
    labels=[x for x in os.listdir(labelsPath) if  x.find('classes') == -1]#所有标签
    for i,txt in enumerate(labels):
        try:
            if not txt.find('class') == -1:
                continue
            posPath=pathjoin(labelsPath,txt)
            img=imgs[i]#当前标签对应的图片
            imgSize=img.size

            with open(posPath, "r") as f:
                for s in f.readlines():#每个框的坐标
                    points=list(map(float,s.split()))[1:]#(center.x,center.y,width,height),中心坐标和宽高
                    leftup=(np.array((points[0],points[1]))*np.array([imgSize[0],imgSize[1]])).astype(int)#左上坐标（x,y)
                    wh=((np.array((points[2],points[3]))*np.array([imgSize[0],imgSize[1]])).astype(int))
                    leftup=leftup-(wh/2).astype(int)#左上角
                    zone=[leftup[0],leftup[1],leftup[0]+wh[0],leftup[1]+wh[1]]#裁剪区域
                    # print(zone)
                    detectedBox=img.crop(zone)
                    # print(pathjoin(savePath,'box'))
                    saveDir=pathjoin(savePath,f"{os.path.splitext(txt)[0]}")
                    if os.path.exists(saveDir) ==False:
                        os.mkdir(saveDir)
                    saveForce(detectedBox,pathjoin(saveDir,f'{txt.split(".")[0]}_box.jpg'))#保存检测后的子图到对应labels名称目录里
        except Exception as e:
            print(f"保存{txt}时出错\n{e}")

if __name__ == '__main__':
    # splitExp()
    pass