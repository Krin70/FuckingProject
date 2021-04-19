import inspect
import os
import shutil
import traceback
from collections import Counter


def read_file(path):
    """Takes a list of file from the path.
        path: String of image path 'path'.

        Returns 1 String list:
        filePathList: [filePath1, filePath2, filePath3...].
    """
    filePathList = []  # 文件目录列表
    directoryList = []  # 文件夹目录列表
    for root, sub_folders, files in os.walk(path):
        for name in files:
            filePathList.append(os.path.join(root, name))
        for name in sub_folders:
            directoryList.append(os.path.join(root, name))
    return filePathList


def create_dir(path, createDirectoryList):
    """create directories in the path.
        path: String of image path 'path'.
        createDirectoryList: List of String of directory ['directory1','directory2'....].
    """
    try:
        for directory in createDirectoryList:
            if not os.path.exists(os.path.join(path, directory)):
                os.makedirs(os.path.join(path, directory))
                print("%s 文件夹创建成功" % directory)
            else:
                print("%s 文件夹已经存在" % directory)
    except Exception as e:
        print(e)


def move_file(src_path, dst_path, file):
    """move file from directory of scr_path to directory of dst_path.
        src_path: String of the src_path to file 'src_path'.
        dst_path: String of the dst_path 'dst_path'.
        file: String of the file 'file'
    """
    print('from : ', src_path)
    print('to : ', dst_path)
    try:
        # cmd = 'chmod -R +x ' + src_path
        # os.popen(cmd)
        f_src = os.path.join(src_path, file)
        if not os.path.exists(dst_path):
            os.mkdir(dst_path)
        f_dst = os.path.join(dst_path, file)
        shutil.move(f_src, f_dst)
    except Exception as e:
        print('move_file ERROR: ', e)
        traceback.print_exc()


# 清洗images中非DCM文件
def IsDCM(path):
    """Takes a list of DCM image path from the path.
        path: String of image path 'path'.

        Returns 1 String list:
        returnDCMList: [imgPath1, imgPath2, imgPath3...].
    """
    returnDCMList = []
    for IsDcm in path:
        Suffix = IsDcm.split(".")[-1]
        if Suffix == 'DCM':
            returnDCMList.append(IsDcm)
    return returnDCMList


# 选出MRI图像
def IsMRI(path):
    """Takes a list of MRI DCM image path from the path.
        path: String of DCM image path 'path'.

        Returns 1 String list:
        returnMRIList: [imgPath1, imgPath2, imgPath3...].
    """
    returnMRIList = []  # DCM文件里在MRI文件夹下面的文件
    for Is_MRI in path:
        rex = Is_MRI.split("\\")
        for temp in rex:
            if temp == 'MRI':
                returnMRIList.append(Is_MRI)
    return returnMRIList


def IsReport(images):
    """Takes a list of MRI DCM image path from the path.
        images: List of String of DCM image path ['images1','images2'..].

        Returns 1 String list:
        report: [imgPath1, imgPath2, imgPath3...].
    """
    report = []
    for isReport in images:
        Suffix = isReport.split(".")[0][-12:]
        if Suffix == 'W65280L32640':
            report.append(isReport)
    return report


def Label_MRI_images_Func(ReportList, MRI_Images_List):
    Report_Number = [j for i in ReportList for j in i.split("\\") if j.isnumeric()]  # 报告文件中的病历号

    b = dict(Counter(Report_Number))
    # print([key for key, value in b.items() if value > 1])  # 只展示重复元素
    Report_Number = [key for key, value in b.items() if value == 1]  # 原先540个样本，这一步放弃掉了56个有重复的病历号样本

    MRI_image_Number = [j for i in MRI_Images_List for j in i.split("\\") if j.isnumeric()]  # MRI中的病历号
    # 筛选在MRI中且在Report中的病例号
    MRI_image_in_Report = [j for i in MRI_image_Number for j in Report_Number if i == j]  # 在报告中的病历号列表

    # 这一步相当于内连接
    # 把有标签的MRI图像保存下来
    HasReport_MRI_images = [i for i in MRI_Images_List for j in i.split("\\") if j.isnumeric() for k in
                            MRI_image_in_Report if k == j]
    # for i in MRI_Images_List:
    #     for j in i.split("\\"):
    #         if j.isnumeric():
    #             for k in MRI_image_in_Report:
    #                 if k == j:
    #                     HasReport_MRI_images.append(i)
    return HasReport_MRI_images


def loadData(infile):
    f = open(infile, 'r', encoding='utf-8')
    sourceInLine = f.readlines()
    return sourceInLine


def WriteData(list1, name):
    file = open(name + ".list", "w", encoding='utf-8')
    file.write('\n'.join(list1))
    file.close()


def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]
