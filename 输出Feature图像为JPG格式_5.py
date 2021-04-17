# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 16:56:13 2020

@author: XEON
"""

import pydicom
import matplotlib.pyplot as plt
import matplotlib
import os
import utils


def convertToJPG(MRI_image, Path):
    for i in MRI_image:
        filename = i.split("\\")[-1]
        os.chdir(i.replace(filename, ''))
        if os.path.exists(filename.split(".")[0] + ".jpg") is False:
            ds = pydicom.dcmread(filename, force=True)
            ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
            img = ds.pixel_array  # 提取图像信息
            matplotlib.use('Agg')
            plt.figure(figsize=(7, 7.5))
            plt.axis('off')
            plt.imshow(img, cmap=plt.cm.gray)
            os.chdir(ROOT_DIR + Path)
            plt.savefig(filename.split(".")[0] + ".jpg", bbox_inches="tight")
            plt.close()


if __name__ == "__main__":
    ROOT_DIR = os.getcwd()

    MalePath = r".\Male_MRI_image.list"
    FemalePath = r".\Female_MRI_image.list"

    createdir = [r"Feature\\Male", r"Feature\\Female"]
    utils.create_dir(ROOT_DIR, createdir)

    Male_MRI_image = utils.loadData(MalePath)
    Male_MRI_image = [i.strip() for i in Male_MRI_image]
    Female_MRI_image = utils.loadData(FemalePath)
    Female_MRI_image = [i.strip() for i in Female_MRI_image]

    convertToJPG(Male_MRI_image, r"\Feature\Male")
    convertToJPG(Female_MRI_image, r"\Feature\Female")
