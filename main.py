'''
使用例，详细代码请看LabelSAM
'''
import os
from LabelSAM import AutoAddLabel,ImageResize,SplitMasks
from segment_anything import SamAutomaticMaskGenerator

def Main():
    save_crop=True#是否保存检测框内的mask
    resize_img=False#是否降低分辨率

    LABEL_NAME="wheat"#单目标标签名
    imgDir = r'./images/train'  # 待标注的图片路径
    labelDir = r'./labels/train'  # 存放标注txt的路径,同labelimg的save dir
    cropDir = r'./result/main'  # 存放裁剪完图片的目录
    resizeDir=r'./images/temp' #图片太大需要降低分辨率的目录


    if resize_img:#注意不需要resize的时候请改为false，不然每次运行都会执行resize
        ImageResize.resizeImage(dirPath=resizeDir,factor=2)#目录里的所有图片分辨率降低2倍（长宽/2）
    #模型列表
    h_sam = "sam_vit_h_4b8939.pth"
    b_sam = "sam_vit_b_01ec64.pth"
    l_sam = "sam_vit_l_0b3195.pth"

    model_type='vit_l'#模型类型，与模型类型同步
    model_path=rf'./model/{l_sam}'#模型路径

    #1.加载一个默认参数的模型
    # generator = AutoAddLabel.loadModel(model_type=model_type,model_path=model_path,device='cuda')

    #2.修改检测自己目标的合适参数（重点，因为sam非常通用，想要尽可能多得到自己目标的检测，就要修改参数
    generator2 = AutoAddLabel.loadModel(
        model_path=model_path,
        model_type=model_type,
        device='cuda',#默认使用gpu，配置不够可以改成cpu，但是推理时间会长很多
        params=dict(
            # points_per_side=32,
            pred_iou_thresh=0.3,
            stability_score_thresh=0.9,#得分，越高符合要求的越少
            # crop_n_layers=1,
            # crop_n_points_downscale_factor=2,
            # min_mask_region_area=500,  # Requires open-cv to run post-processing
            # points_per_batch=2
        )#模型参数
    )

    #调用自动标注函数
    # AutoAddLabel.autoAddLabels(labelsPAth=labelDir, imagePath=imgDir,generator=generator)
    AutoAddLabel.autoAddLabels(
        labelsPAth=labelDir, 
        imagePath=imgDir,
        generator=generator2
    )

    #自动标注，将imgDir的标注内容存入labelDir
    if save_crop:
        SplitMasks.splitExp(
            imagesPath=imgDir,
            labelsPath=labelDir,
            savePath=cropDir
        )

if __name__ == '__main__':
    Main()
