# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 15:40:27 2020

@author: XEON
"""

from preprocess import utils

if __name__ == "__main__":
    file = utils.read_file("F:\\OneDrive - THE GOD'S CHILD PROJECT\\骨质疏松症项目\\骨质疏松")

    images = utils.IsDCM(file)  # image列表里都是DCM文件
    MRI_image = utils.IsMRI(file)  # MRI_image列表里都是MRI DCM文件
    Report = utils.IsReport(images)  # Report列表里都是挑选出DCM里面都是诊断书的DCM文件

    MRI_imagePath, Report_imagePath = utils.Label_MRI_images_Func(Report, MRI_image)  # 这里得到有Report的MRI影像路径和有影像的Report路径
    Male_MRI_image = utils.duplication_reduce(utils.select_sex("男性", MRI_imagePath))  # 这里得到男性的MRI影像路径
    Female_MRI_image = utils.duplication_reduce(utils.select_sex("女性", MRI_imagePath))  # 这里得到女性的MRI影像路径

    # 这一步取得变量名
    Male_MRI_image_name = utils.retrieve_name(Male_MRI_image)[0]
    Female_MRI_image_name = utils.retrieve_name(Female_MRI_image)[0]
    Report_image_name = utils.retrieve_name(Report_imagePath)[0]

    # 这一步将变量名作为文件名，并将文件写成.list文件后缀格式
    utils.WriteData(Male_MRI_image, Male_MRI_image_name)
    utils.WriteData(Female_MRI_image, Female_MRI_image_name)
    utils.WriteData(Report_imagePath, Report_image_name)
