# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:07:23 2020

@author: XEON
"""

import os


from preprocess import utils


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

    randomList = utils.getRandomList(OP, maxImagesNum)
    OP = [OP[i] for i in randomList]
    randomList = utils.getRandomList(OST, maxImagesNum)
    OST = [OST[i] for i in randomList]
    randomList = utils.getRandomList(NBM, maxImagesNum)
    NBM = [NBM[i] for i in randomList]

    rename_OP = utils.renameFile(OP, "OP")
    rename_OST = utils.renameFile(OST, "OST")
    rename_NBM = utils.renameFile(NBM, "NBM")

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
