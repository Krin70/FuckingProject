# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 15:40:27 2020

@author: XEON
"""

import jieba
from preprocess import utils


def Label_MRI_images_Func(ReportList, MRI_Images_List):
    MRI_image_in_Report = []  # 在报告中的病历号列表
    Report_Number = []  # 报告文件中的病历号
    HasReport_MRI_images = []

    for i in ReportList:
        for j in i.split("\\"):  #
            if j.isnumeric():  # 病历号
                Report_Number.append(j)  #
    Report_Number = list(set(Report_Number))  # 这一步为什么与Report数量差了这么多

    MRI_image_Number = []  # MRI中的病历号
    for i in MRI_Images_List:
        for j in i.split("\\"):
            if j.isnumeric():
                MRI_image_Number.append(j)
    MRI_image_Number = list(set(MRI_image_Number))

    # 筛选在MRI中且在Report中的病例号
    for i in MRI_image_Number:
        for j in Report_Number:
            if i == j:
                MRI_image_in_Report.append(j)

    # 这一步相当于内连接
    # 把有标签的MRI图像保存下来
    for i in MRI_Images_List:
        for j in i.split("\\"):
            if j.isnumeric():
                for k in MRI_image_in_Report:
                    if k == j:
                        HasReport_MRI_images.append(i)
    return HasReport_MRI_images


# from collections import Counter #引入Counter
# a = [1, 2, 3, 3, 4, 4]
# b = dict(Counter(a))
# print(b)
# print ([key for key,value in b.items() if value > 1]) #只展示重复元素
# print ({key:value for key,value in b.items() if value > 1}) #展现重复元素和重复次数

def select_sex(Str1, img):
    sex_MRI_image = []
    for Is_Male_MRI in img:
        rex = Is_Male_MRI.split("\\")
        for temp in rex:
            temp = list(jieba.cut(temp))
            break_flag = False  # 跳出循环标志
            for t in temp:
                if t == Str1:
                    break_flag = True
                    sex_MRI_image.append(Is_Male_MRI)
                    break
        if break_flag == True:
            break
    return sex_MRI_image


def duplication_reduce(list1):
    set2 = set(list1)
    list1 = list(set2)
    return list1


if __name__ == "__main__":
    file = utils.read_file("F:\\OneDrive - THE GOD'S CHILD PROJECT\\骨质疏松症项目\\骨质疏松")

    images = utils.IsDCM(file)  # image列表里都是DCM文件
    MRI_image = utils.IsMRI(file)  # MRI_image列表里都是MRI DCM文件
    Report = utils.IsReport(images)  # Report列表里都是挑选出DCM里面都是诊断书的DCM文件

    Label_MRI_images = utils.Label_MRI_images_Func(Report, MRI_image)
    Male_MRI_image = duplication_reduce(select_sex("男性", Label_MRI_images))
    Female_MRI_image = duplication_reduce(select_sex("女性", Label_MRI_images))

    Male_MRI_image_name = utils.retrieve_name(Male_MRI_image)[0]
    Female_MRI_image_name = utils.retrieve_name(Female_MRI_image)[0]
    Report_image_name = utils.retrieve_name(Report)[0]

    utils.WriteData(Male_MRI_image, Male_MRI_image_name)
    utils.WriteData(Female_MRI_image, Female_MRI_image_name)
    utils.WriteData(Report, Report_image_name)
