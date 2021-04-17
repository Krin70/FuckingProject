# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 15:40:27 2020

@author: XEON
"""

import jieba
import utils


# 清洗images中非DCM文件
def IsDCM(path_file):
    images_temp = []
    for IsDcm in path_file:
        Suffix = IsDcm.split(".")[-1]
        if Suffix == 'DCM':
            images_temp.append(IsDcm)
    return images_temp


# 选出MRI图像
def IsMRI(path_file):
    MRI_image = []  # DCM文件里在MRI文件夹下面的文件
    for Is_MRI in path_file:
        rex = Is_MRI.split("\\")
        for temp in rex:
            if temp == 'MRI':
                MRI_image.append(Is_MRI)
    return MRI_image


def IsReport(path_file):
    report = []
    for isReport in images:
        Suffix = isReport.split(".")[0][-12:]
        if Suffix == 'W65280L32640':
            report.append(isReport)
    return report


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
    Path_file = utils.read_file("F:\\OneDrive - THE GOD'S CHILD PROJECT\\骨质疏松症项目\\骨质疏松")

    images = IsDCM(Path_file)  # image列表里都是DCM文件
    MRI_image = IsMRI(Path_file)  # MRI_image列表里都是MRI DCM文件
    Report = IsReport(Path_file)

    Label_MRI_images = Label_MRI_images_Func(Report, MRI_image)
    Male_MRI_image = duplication_reduce(select_sex("男性", Label_MRI_images))
    Female_MRI_image = duplication_reduce(select_sex("女性", Label_MRI_images))

    Male_MRI_image_name = utils.retrieve_name(Male_MRI_image)[0]
    Female_MRI_image_name = utils.retrieve_name(Female_MRI_image)[0]
    Report_image_name = utils.retrieve_name(Report)[0]

    utils.WriteData(Male_MRI_image, Male_MRI_image_name)
    utils.WriteData(Female_MRI_image, Female_MRI_image_name)
    utils.WriteData(Report, Report_image_name)
