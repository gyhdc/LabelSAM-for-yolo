# LabelSAM-for-yolo

简易的yolo半自动标注工具，目前只支持单目标。


<p float="left">
 <img src="asserts/road.png?raw=true" width="58%" />
 <img src="asserts/wheats.png?raw=true" width="40%"  />
</p>




## 项目结构：

```
1.LabelSAM:项目源码，请到segment-anything(https://github.com/facebookresearch/segment-anything)
2.segment_anything:segment-anything code
3.images:存放待处理的图片文件，同labelimg的open dir路径。
4.labels:存放生成的标注的标签
5.model:存放SAM的模型文件，去https://github.com/facebookresearch/segment-anything#model-checkpoints下载对应的模型文件。
6.result:存放分割后的图像
7.main.py:项目的示例代码，只需要调整模型的参数达到符合自己任务的需求即可。
```

### Doload models(放在model目录下)：

- **`vit_h`: [ViT-H SAM model.](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth)**
- `vit_l`: [ViT-L SAM model.](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth)
- `vit_b`: [ViT-B SAM model.](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth)

### python环境：

```
python>=3.8, as well as pytorch>=1.7 and torchvision>=0.8,opencv-python>=4.6.0
```


## 注意：SAM的推理对gpu性能要求较高，作者本身是3060，使用vit_l模型推理一张1080p的图像算是快显存极限了。不赶时间的话，gpu又不太好的同学，可以用cpu。


### 基于SAM的yolo半自动标注后端。请配合labelimg使用，或者将生成的标注文件自己移动到其他软件下使用。

用法很简单，源码也加满了注释。直接使用的话可以将待处理图片放入

```
images/train
```


标注文件的默认路径在

```
labels/train
```

然后运行main.py文件

## main.py参数:

save_crop=True $~~~~~~~~~~~~~~~~~~~~~~~$ -- 是否保存检测框内的mask   

resize_img=False $~~~~~~~~~~~~~~~~~~~~~$ -- 是否降低分辨率   


LABEL_NAME="object"    $~~~~~~~~~~~~$       -- 单目标标签名   

imgDir = r'./images/train' $~~~~~~~~~$   -- 待标注的图片路径   

labelDir = r'./labels/train' $~~~~~~~~~~$ --  存放标注txt的路径,同labelimg的save dir   

cropDir = r'./result/main'  $~~~~~~~~~~$  -- 存放检测框中的图像   

resizeDir=r'./images/temp' $~~~~~~~~$   -- 低分辨率图像目录

## 常见问题:

### UDA out of memory(GPU显存不够)

### 解决方法1 

修改main.py中resize_img=False 更改为 resize_img=True, 并设置降低分辨率倍数factor 

### 解决方法2

main.py中device = 'cuda' 更改为 device = 'cpu'

可以的话能给我个小⭐⭐吗....



