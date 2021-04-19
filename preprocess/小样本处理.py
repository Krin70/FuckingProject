# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 15:38:57 2021

@author: XEON
"""

import utils
import re
import os


DIR = r"J:\label\_json"
fileList=utils.read_file(DIR)
for i in fileList:
    oldFileName = i.split('\\')[-1]
    newFileName = re.sub(r'\D', "", i)+'.png'
    path = i.replace(oldFileName,'')
    if oldFileName=='img.png':
        print(path+oldFileName+'=====>'+path+newFileName)
        os.rename(path+oldFileName,path+newFileName)

fileList=[i for i in utils.read_file(DIR) if i.split('\\')[-1].split('.')[0].isdigit()]
oldDir = [i.replace(i.split('\\')[-1],'') for i in fileList]
file = [i.split('\\')[-1] for i in fileList]
dst_path = r"F:\OneDrive - THE GOD'S CHILD PROJECT\骨质疏松症项目\代码\整理代码\Mask_RCNN-master\img"
for index in range(len(oldDir)):
    src_path = oldDir[index]
    utils.move_file(src_path, dst_path, file[index])
    

os.chdir(r"F:\OneDrive - THE GOD'S CHILD PROJECT\骨质疏松症项目\代码\整理代码\Mask_RCNN-master")
os.getcwd()

import cv2
from mrcnn.visualize import display_instances
from mrcnn.config import Config
from mrcnn import model as modellib


class BalloonConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "balloon"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # Background + balloon

    # Number of training steps per epoch
    #    STEPS_PER_EPOCH = 100

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9


if __name__ == "__main__":
    images = cv2.imread("img\\1.png")
    config = BalloonConfig()
    
    model = modellib.MaskRCNN(mode="inference", config=config, model_dir="logs")
    
    model.load_weights("logs/mask_rcnn_balloon_0009.h5", by_name=True)
    
    result = model.detect([images])
    
    print(result[0])
    
    class_name = ["BG", "bone"]
    
    display_instances(images, result[0]["rois"], result[0]["masks"], result[0]["class_ids"], class_name[1],
                      scores=None, title="bone",
                      figsize=(16, 16), ax=None,
                      show_mask=True, show_bbox=True,
                      colors=None, captions=None)

