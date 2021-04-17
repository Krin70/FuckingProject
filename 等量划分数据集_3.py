# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:07:23 2020

@author: XEON
"""

import os
import random

import utils


# def read_file(DIR):
#     file_dir = DIR
#     images = []
#     temp = []  # 文件夹目录
#     for root, sub_folders, files in os.walk(file_dir):
#         for name in files:
#             images.append(os.path.join(root, name))
#         for name in sub_folders:
#             temp.append(os.path.join(root, name))
#     return images

# 获得一个不重复随机数
def getRandomList(List1, num):
    resultList = random.sample(range(0, len(List1)), num)
    return resultList


# 输出格式为(List, Str)
# 输出格式为List   如List[0] = {C:\Users\XEON\temp\test.1.jpg}
def renameFile(oldNameList, label):
    newNameList = []
    n = 0
    fileDirectory = oldNameList[0]
    newName = fileDirectory.split("\\")[-1]
    path = fileDirectory.replace(newName, '')
    for i in oldNameList:
        # 设置旧文件名（就是路径+文件名）
        oldName = i  # os.sep添加系统分隔符

        # 设置新文件名
        newName = path + label + '.' + str(n + 1) + '.jpg'

        os.rename(oldName, newName)  # 用os模块中的rename方法对文件改名
        print(oldName, '======>', newName)

        n += 1
        newNameList.append(newName)
    return newNameList


if __name__ == "__main__":
    ROOT_DIR = os.getcwd()
    createdir = ["Train", "Valid", "Test"]
    utils.create_dir(ROOT_DIR, createdir)
    Path_file = utils.read_file(ROOT_DIR)

    # 得到一个label为0的list
    # [name for name in Path_file if name.split("\\")[-2]==str(0)]

    # 0 = 骨质疏松 = osteoporosis = OP =
    # 1 = 骨量减少 = Osteopenia = OST = low bone mass low bone mass
    # 2 = 骨量正常 = NBM = normal bone mass

    OP = [name for name in Path_file if name.split("\\")[-2] == str(0)]
    OST = [name for name in Path_file if name.split("\\")[-2] == str(1)]
    NBM = [name for name in Path_file if name.split("\\")[-2] == str(2)]

    maxImagesNum = min([len(OP), len(OST), len(NBM)])

    randomList = getRandomList(OP, maxImagesNum)
    OP = [OP[i] for i in randomList]
    randomList = getRandomList(OST, maxImagesNum)
    OST = [OST[i] for i in randomList]
    randomList = getRandomList(NBM, maxImagesNum)
    NBM = [NBM[i] for i in randomList]

    # 测试renameFile函数
    # oldnameList = ["C:\\Users\\XEON\\temp\\91.5.jpg","C:\\Users\\XEON\\temp\\91.4.jpg"]
    #
    # newnameList = renameFile(oldnameList)

    rename_OP = renameFile(OP, "OP")
    rename_OST = renameFile(OST, "OST")
    rename_NBM = renameFile(NBM, "NBM")

    # 移动文件测试
    # for i in oldnameList:
    #    file = i.split("\\")[-1]
    #    src_path = i.replace(file,'')
    #    move_file(src_path,r"./Train",file)
    #

    # for i in [rename_OP,rename_OST,rename_NBM]:
    #    file = i.split("\\")[-1]
    #    src_path = i.replace(file,'')
    #    move_file(src_path,r"./dataset",file)

    for i in rename_OP:
        file = i.split("\\")[-1]
        src_path = i.replace(file, '')
        utils.move_file(src_path, r"./dataset", file)

    for i in rename_OST:
        file = i.split("\\")[-1]
        src_path = i.replace(file, '')
        utils.move_file(src_path, r"./dataset", file)

    for i in rename_NBM:
        file = i.split("\\")[-1]
        src_path = i.replace(file, '')
        utils.move_file(src_path, r"./dataset", file)
