'''
自动生成labels文件
'''
import os
import torch
import cv2
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor



#todo 单目标检测的目标名
# LABEL_NAME='wheat'

def getstdFloat(f, num=6):
    return "{:.6f}".format(f)
def loadModel(model_type,model_path,device='cuda',params=-1,generator=-1):

    #todo 根据自己的配置选择模型,填写模型路径
    h_sam="sam_vit_h_4b8939.pth"
    b_sam="sam_vit_b_01ec64.pth"
    l_sam="sam_vit_l_0b3195.pth"

    modelPath = model_path  # 模型的路径
    sam_checkpoint = modelPath
    model_type = model_type
    device = device


    if params==-1 and generator ==-1:#直接默认模型
        sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        sam.to(device=device)
        params={}
        params['model'] = sam
        mask_generator = SamAutomaticMaskGenerator(
            model=sam
        )
    else:
        #todo 修改检测自己目标的合适参数
        if not generator ==-1:
            mask_generator=generator
        else:
            sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
            sam.to(device=device)
            params['model']=sam
            # print(params)
            mask_generator = SamAutomaticMaskGenerator(
                **params
            )
    print("模型加载完毕。")
    return mask_generator

# #todo 存放标签的目录，自己修改，同labelimg的open dir
# targetDir=r'D:\Desktop\1.WheatCounting\Detect\yolov5-master\yolov5-master\runs\MyOperation\SAM_labels\labels\train'
# #todo 需要标记的图片存放的目录，同labelimg的save dir
# sourceDir=r'D:\Desktop\1.WheatCounting\Detect\yolov5-master\yolov5-master\runs\MyOperation\SAM_labels\images\train'

###

def getCoord(img,mask_generator):#获取一张图的所有坐标
    masks = mask_generator.generate(img)
    ans=[]
    for mask in masks:#存入检测框坐标信息到标签内
        ori_coords=list(mask['bbox'])#[x,y,w,h]获取检测框
        # print((ori_coords))
        imgSize=[img.shape[1],img.shape[0]]
        leftup=[getstdFloat((x + ori_coords[i + 2] / 2) / imgSize[i]) for i, x in enumerate(ori_coords[:2])]
        wh=[getstdFloat(x / imgSize[i]) for i, x in enumerate(ori_coords[2:])]
        coord=[leftup[0],leftup[1],wh[0],wh[1]]#最终坐标
        area=int(ori_coords[2])*int(ori_coords[3])
        res="0 "+' '.join(list(coord))
        ans.append(res)
    return ans


def autoAddLabels(labelsPAth, imagePath,generator,LABEL_NAME='UNK'):#生成检测框标注txt
    '''
    :param labelsPAth: todo 存放标签的目录，自己修改，同labelimg的open dir
    :param imagePath: todo 需要标记的图片存放的目录，同labelimg的save dir
    :return: None
    '''
    # generator=loadModel()
    if not os.path.exists(os.path.join(labelsPAth, 'classes.txt')):#创建分类文件
        with open(os.path.join(labelsPAth, 'classes.txt'), mode='w') as f:
            f.write(LABEL_NAME)
    sourceList = os.listdir(imagePath)
    for i,img in enumerate(sourceList):
        try:
            for _ in range(5):#清空显存
                torch.cuda.empty_cache()
            txt=img.split('.')[0]+".txt"
            print(f'{i}. 正在自动标注 {img}')
            realImgPath=os.path.join(imagePath, img)
            realTXTPath=os.path.join(labelsPAth, txt)
            image_=cv2.imread(realImgPath)
            data=getCoord(image_,generator)
            with open(realTXTPath,mode='w') as f:
                f.write('\n'.join(data))
        except Exception as e:
            print(f"标注{i}.{img}时出错\n{e}")

if __name__ == '__main__':
    pass
    # todo 存放标签的目录，自己修改，同labelimg的open dir
    # targetDir = r'D:\Desktop\1.WheatCounting\Detect\yolov5-master\yolov5-master\runs\MyOperation\SAM_labels\labels\train'
    # # todo 需要标记的图片存放的目录，同labelimg的save dir
    # sourceDir = r'D:\Desktop\1.WheatCounting\Detect\yolov5-master\yolov5-master\runs\MyOperation\SAM_labels\images\train'
    # autoAddLabels(targetDir,sourceDir)
