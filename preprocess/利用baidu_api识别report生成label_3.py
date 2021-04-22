# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 15:48:52 2020

@author: XEON
"""

import glob
from os import path
import os
import time
import numpy as np
from preprocess import utils

if __name__ == "__main__":
    ROOT_DIR = os.getcwd()
    outDirectory = '.\\preprocess\\Label\\ReportResult'
    if not path.exists(outDirectory):
        os.mkdir(outDirectory)
    print("压缩过大的图片...")
    # 首先对过大的图片进行压缩，以提高识别速度，将压缩的图片保存与临时文件夹中
    for JPG_File in glob.glob(".\\preprocess\\Label\\Report\\*.jpg"):
        utils.cropImg(JPG_File, outDirectory)
    print("图片识别...")
    fileNameList = []
    LabelsList = []
    num = 0  # 计数器
    for JPG_File in glob.glob(".\\preprocess\\Label\\ReportResult\\*.jpg"):
        print(num)
        num += 1
        time.sleep(1)
        _, filename, label1 = utils.baiduOCR(JPG_File)
        fileNameList.append(filename)
        LabelsList.append(label1)
        os.remove(JPG_File)
    print('图片文本提取结束！')

    # for file in blank_output:
    #     utils.move_file(".\\preprocess\\Label\\Report\\", ".\\preprocess\\Label\\ReportResult\\temp", file)

    # for JPG_File in glob.glob(".\\preprocess\\Label\\ReportResult\\temp\\" + "*.jpg"):
    #     utils.cropImg(JPG_File, ".\\preprocess\\Label\\ReportResult\\temp\\tmp", False)

    fileNameList1 = []
    LabelsList1 = []
    num = 0
    for name in glob.glob(".\\preprocess\\Label\\ReportResult\\temp\\tmp\\" + "*.jpg"):
        filename = path.basename(name)
        APP_ID = '20280389'  # 刚才获取的 ID，下同
        API_KEY = 'V1MgPatLTbbaXCPX7QWN6t8e'
        SECRET_KEY = 'mLBv4t0B1cgw5Ep8djK6uXEOi7qsHcuL'
        client = utils.AipOcr(APP_ID, API_KEY, SECRET_KEY)

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
    np.save('.\\preprocess\\Label\\ReportLabel', operateDictionary)
    # Load
    read_dictionary = np.load('.\\preprocess\\Label\\ReportLabel.npy', allow_pickle=True).item()
