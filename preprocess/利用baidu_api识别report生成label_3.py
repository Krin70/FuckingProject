# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 15:48:52 2020

@author: XEON
"""

import glob
from os import path
import os
from aip import AipOcr
from PIL import Image
import time
import numpy as np
from preprocess import utils


# 裁剪图片与压缩图片
def convertImg(PicFile, outputDirectory, need_Crop=True):
    """调整图片大小，对于过大的图片进行压缩
    PicFile:    图片路径
    outputDirectory：    图片输出路径
    """
    img = Image.open(PicFile)
    if need_Crop:
        img = img.crop((36, 804, 514, 899))
    width, height = img.size
    while width * height > 4000000:  # 该数值压缩后的图片大约 两百多k
        width = width // 2
        height = height // 2
    new_img = img.resize((width, height), Image.BILINEAR)
    new_img.save(path.join(outputDirectory, os.path.basename(PicFile)))


# 扫描识别图片
def baiduOCR(picfile):
    """利用百度api识别文本，并保存提取的文字
    picfile:    图片文件名
    """
    fileName = path.basename(picfile)
    APP_ID = '20280389'  # 刚才获取的 ID，下同
    API_KEY = 'V1MgPatLTbbaXCPX7QWN6t8e'
    SECRET_KEY = 'mLBv4t0B1cgw5Ep8djK6uXEOi7qsHcuL'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    i = open(picfile, 'rb')
    img = i.read()
    print("正在识别图片：\t" + fileName)
    message = client.basicGeneral(img)  # 通用文字识别，每天 50 000 次免费
    # message = client.basicAccurate(img)   # 通用文字高精度识别，每天 800 次免费
    print("识别成功！")
    i.close();
    diagnose = ''
    if message.get('words_result_num') != 0:
        for text in message.get('words_result'):
            diagnose = text.get('words')
    else:
        blank_output.append(fileName)
        diagnose = ''
    return blank_output, fileName, diagnose


if __name__ == "__main__":
    ROOT_DIR = os.getcwd()
    outDirectory = './Label/ReportResult'
    if not path.exists(outDirectory):
        os.mkdir(outDirectory)
    print("压缩过大的图片...")
    # 首先对过大的图片进行压缩，以提高识别速度，将压缩的图片保存与临时文件夹中
    for JPG_File in glob.glob(r".\\Label\\Report\\" + "*.jpg"):
        convertImg(JPG_File, outDirectory)
    print("图片识别...")
    blank_output = []
    fileNameList = []
    LabelsList = []
    num = 0  # 计数器
    for JPG_File in glob.glob("./Label/ReportResult/*.jpg"):
        print(num)
        num += 1
        time.sleep(1)
        blank_output, filename, label1 = baiduOCR(JPG_File)
        fileNameList.append(filename)
        LabelsList.append(label1)
        os.remove(JPG_File)
    print('图片文本提取结束！')

    for file in blank_output:
        utils.move_file("./Label/Report/", "./Label/ReportResult/temp", file)

    for JPG_File in glob.glob(r"./Label/ReportResult/temp/" + "*.jpg"):
        convertImg(JPG_File, "./Label/ReportResult/temp/tmp", False)

    fileNameList1 = []
    LabelsList1 = []
    num = 0
    for name in glob.glob("./Label/ReportResult/temp/tmp/" + "*.jpg"):
        filename = path.basename(name)
        APP_ID = '20280389'  # 刚才获取的 ID，下同
        API_KEY = 'V1MgPatLTbbaXCPX7QWN6t8e'
        SECRET_KEY = 'mLBv4t0B1cgw5Ep8djK6uXEOi7qsHcuL'
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

        i = open(name, 'rb')
        img = i.read()
        num += 1
        print(num)
        print("正在识别难以识别的图片：\t" + filename)
        message = client.basicGeneral(img)  # 通用文字识别，每天 50 000 次免费
        # message = client.basicAccurate(img)   # 通用文字高精度识别，每天 800 次免费
        print("识别成功！")
        i.close();
        # if message.get('words_result_num') != 0:
        text = message.get('words_result')
        for i, w in enumerate(text):
            if "意见" in w.get("words"):
                LabelsList1.append(w.get("words") + text[i].get("words") + text[i + 1].get("words"))
                fileNameList1.append(filename)

    Dic = {}
    Dic.update(dict(zip(fileNameList, LabelsList)))
    Dic.update(dict(zip(fileNameList1, LabelsList1)))
    Useful_Report_Filename = []  # 已经识别出来的DCM文件名
    Useful_Report_Result = []  # 已经识别出来的对应标签

    for key, value in Dic.items():
        if '意见' in value or "临床" in value \
                or "异常" in value or "正常" in value \
                or "在同龄人范围内" in value or "临床" in value:
            Useful_Report_Filename.append(key)
            Useful_Report_Result.append(value)
    #     else:
    #         Need_Processed_Filename.append(key)
    #         print(key)
    #         print(value)
    # Need_Processed_Filename = Need_Processed_Filename + blank_output
    # for file in Need_Processed_Filename:
    #     utils.move_file("./Label/ReportResult/", "./Label/ReportResult/temp", file)

    # 数值化标签
    for key, value in enumerate(Useful_Report_Result):
        if '减少' in value or "低于" in value:
            Useful_Report_Result[key] = 1
        elif "正常" in value or "在同龄人范围内" in value \
                or "骨密度在同龄范围内" in value \
                or "未见明显异常" in value:
            Useful_Report_Result[key] = 0
        elif "疏松" in value:
            Useful_Report_Result[key] = 2
        else:
            Useful_Report_Result[key] = value

    Patient_number = []  # 识别出来的DCM文件名中的病历号 
    # 这里出现了一个问题  就是病例号重叠
    # 但是同一个病历号经过观察诊断表发现 结果都一致 所以看作是同一个结果
    for i in Useful_Report_Filename:
        Patient_number.append(i.split("_")[0])

    ContrastDictionary = dict(zip(Patient_number, Useful_Report_Result))  # 已识别图片和对应的标签
    operateDictionary = ContrastDictionary.copy()
    for key in ContrastDictionary:
        if not isinstance(ContrastDictionary[key], int):
            operateDictionary.pop(key)

    # Save
    np.save('./Label/ReportLabel', operateDictionary)
    # Load
    read_dictionary = np.load('./Label/ReportLabel.npy', allow_pickle=True).item()
