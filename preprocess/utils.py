import inspect
import os
import shutil
import traceback
import pydicom
import cv2 as cv
import numpy as np
from collections import Counter
from random import random
from PIL import Image
from aip import AipOcr
from os import path


def read_file(fpath):
    """Takes a list of file from the path.
        path: String of image path 'path'.

        Returns 1 String list:
        filePathList: [filePath1, filePath2, filePath3...].
    """
    filePathList = []  # 文件目录列表
    directoryList = []  # 文件夹目录列表
    for root, sub_folders, files in os.walk(fpath):
        for name in files:
            filePathList.append(os.path.join(root, name))
        for name in sub_folders:
            directoryList.append(os.path.join(root, name))
    return filePathList


def create_dir(fpath, createDirectoryList):
    """create directories in the path.
        path: String of image path 'path'.
        createDirectoryList: List of String of directory ['directory1','directory2'....].
    """
    try:
        for directory in createDirectoryList:
            if not os.path.exists(os.path.join(fpath, directory)):
                os.makedirs(os.path.join(fpath, directory))
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
def IsDCM(fpath):
    """Takes a list of DCM image path from the path.
        path: String of image path 'path'.

        Returns 1 String list:
        returnDCMList: [imgPath1, imgPath2, imgPath3...].
    """
    returnDCMList = []
    for IsDcm in fpath:
        Suffix = IsDcm.split(".")[-1]
        if Suffix == 'DCM':
            returnDCMList.append(IsDcm)
    return returnDCMList


# 选出MRI图像
def IsMRI(fpath):
    """Takes a list of MRI DCM image path from the path.
        path: String of DCM image path 'path'.

        Returns 1 String list:
        returnMRIList: [imgPath1, imgPath2, imgPath3...].
    """
    returnMRIList = []  # DCM文件里在MRI文件夹下面的文件
    for Is_MRI in fpath:
        for temp in Is_MRI.split("\\"):
            if temp == 'MRI':
                returnMRIList.append(Is_MRI)
    return returnMRIList


def IsReport(images):
    """Takes a list of Report MRI DCM image path from the path.
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
    """Takes a list of MRI DCM image path from the path.
        ReportList: List of String of DCM image path ['ReportImages1','ReportImages2'..].
        MRI_Images_List: List of String of feature DCM image path ['featureImages1','featureImages2'..].

        Returns 1 String list:
        FeaturesPath: [FeatureImgPath1, FeatureImgPath2, FeatureImgPath3...].
        ReportsPath: [ReportImgPath1, ReportImgPath2, ReportImgPath3...].
    """
    # 对报告单中非重复的病历号进行操作
    Report_Number = [j for i in ReportList for j in i.split("\\") if j.isnumeric()]  # 报告文件中的病历号
    dictOfNumber_Times = dict(Counter(Report_Number))  # Map word and times to dictionary
    # print([key for key, value in dictOfNumber_Times.items() if value > 1])  # 只展示重复元素
    Report_Number = [key for key, value in dictOfNumber_Times.items() if value == 1]  # 原先540个样本，这一步放弃掉了56个有重复的病历号样本

    MRI_image_Number = list(set([j for i in MRI_Images_List for j in i.split("\\") if j.isnumeric()]))  # 取得MRI中的病历号

    MRI_image_in_Report = list(set([j for i in MRI_image_Number for j in Report_Number if
                                    i == j]))  # 筛选在MRI中且在Report中的病例号  返回在报告中的病历号列表

    Report_in_MRI_image = list(set([j for i in MRI_image_Number for j in Report_Number if
                                    i == j]))  # 筛选在Report中的病例号且在MRI中 返回在有MRI影像特征的病历号列表

    # 把有标签的MRI影像特征路径返回成列表
    FeaturesPath = [i for i in MRI_Images_List for j in i.split("\\") if j.isnumeric() for k in
                    MRI_image_in_Report if k == j]
    # 把有标签的MRI影像Report路径返回成列表
    ReportsPath = [i for i in ReportList for j in i.split("\\") if j.isnumeric() for k in
                   Report_in_MRI_image if k == j]

    return FeaturesPath, ReportsPath


def duplication_reduce(filePathList):
    """drop duplicational file path.
        ReportList: List of String of DCM image path ['ReportImages1','ReportImages2'..].
        MRI_Images_List: List of String of feature DCM image path ['featureImages1','featureImages2'..].

        Returns 1 String list:
        HasReport_MRI_images: [imgPath1, imgPath2, imgPath3...].
    """
    filePathList = list(set(filePathList))
    return filePathList


def select_sex(sex, DCM_Path_List):
    """Takes a list of gender MRI DCM path from the DCM_Path.
        sex: String of gender by Chinese.
        DCM_Path_List: List of String of feature DCM image path ['featureImages1','featureImages2'..].

        Returns 1 String list:
        gender_MRI_path_List: [imgPath1, imgPath2, imgPath3...].
    """
    gender_MRI_path_List = [gender_MRI for gender_MRI in DCM_Path_List if sex in gender_MRI]
    return gender_MRI_path_List


def retrieve_name(var):
    """recall the variable name.
        name: String of full of file name.
        list1: List of String context

        Returns 1 String list:
        [String1, String2, ...]
    """
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]


def WriteData(list1, name):
    """Write List of String content to the  file   separator by '\n' with name end by '.list'.
        name: String of full of file name.
        list1: List of String context
    """
    file = open(name + ".list", "w", encoding='utf-8')
    file.write('\n'.join(list1))
    file.close()


def loadData(fileName):
    """Takes context from the file by utf-8 encode.
        fileName: String of full of file name.

        Returns 1 String list:
        List: [imgPath1, imgPath2, imgPath3...] imgPath : String.
    """
    f = open(fileName, 'r', encoding='utf-8')
    sourceInLine = f.readlines()
    return sourceInLine


def get_pixel_data_with_lut_applied(dcm):
    # For Supplemental, numbers below LUT are greyscale, else clipped
    # Don't have a file to test, or know where this flag is stored in pydicom
    SUPPLEMENTAL_LUT = False

    if dcm.PhotometricInterpretation != 'PALETTE COLOR':
        raise Exception

    if (dcm.RedPaletteColorLookupTableDescriptor[0] != dcm.BluePaletteColorLookupTableDescriptor[0] !=
            dcm.GreenPaletteColorLookupTableDescriptor[0]):
        raise Exception

    if (dcm.RedPaletteColorLookupTableDescriptor[1] != dcm.BluePaletteColorLookupTableDescriptor[1] !=
            dcm.GreenPaletteColorLookupTableDescriptor[1]):
        raise Exception

    if (dcm.RedPaletteColorLookupTableDescriptor[2] != dcm.BluePaletteColorLookupTableDescriptor[2] !=
            dcm.GreenPaletteColorLookupTableDescriptor[2]):
        raise Exception

    if (len(dcm.RedPaletteColorLookupTableData) != len(dcm.BluePaletteColorLookupTableData) != len(
            dcm.GreenPaletteColorLookupTableData)):
        raise Exception

    lut_num_values = dcm.RedPaletteColorLookupTableDescriptor[0]
    lut_first_value = dcm.RedPaletteColorLookupTableDescriptor[1]
    lut_bits_per_pixel = dcm.RedPaletteColorLookupTableDescriptor[2]  # warning that they lie though
    lut_data_len = len(dcm.RedPaletteColorLookupTableData)

    if lut_num_values == 0:
        lut_num_values = 2 ** 16

    if not (lut_bits_per_pixel == 8 or lut_bits_per_pixel == 16):
        raise Exception

    if lut_data_len != lut_num_values * lut_bits_per_pixel // 8:
        # perhaps claims 16 bits but only store 8 (apparently even the spec says implementaions lie)
        if lut_bits_per_pixel == 16:
            if lut_data_len == lut_num_values * 8 / 8:
                lut_bits_per_pixel = 8
            else:
                raise Exception
        else:
            raise Exception

    lut_dtype = None

    if lut_bits_per_pixel == 8:
        lut_dtype = np.uint8

    if lut_bits_per_pixel == 16:
        lut_dtype = np.uint16

    red_palette_data = np.frombuffer(dcm.RedPaletteColorLookupTableData, dtype=lut_dtype)
    green_palette_data = np.frombuffer(dcm.GreenPaletteColorLookupTableData, dtype=lut_dtype)
    blue_palette_data = np.frombuffer(dcm.BluePaletteColorLookupTableData, dtype=lut_dtype)

    if lut_first_value != 0:
        if SUPPLEMENTAL_LUT:
            red_palette_start = np.arange(lut_first_value, dtype=lut_dtype)
            green_palette_start = np.arange(lut_first_value, dtype=lut_dtype)
            blue_palette_start = np.arange(lut_first_value, dtype=lut_dtype)
        else:
            red_palette_start = np.ones(lut_first_value, dtype=lut_dtype) * red_palette_data[0]
            green_palette_start = np.ones(lut_first_value, dtype=lut_dtype) * green_palette_data[0]
            blue_palette_start = np.ones(lut_first_value, dtype=lut_dtype) * blue_palette_data[0]

        red_palette = np.concatenate((red_palette_start, red_palette_data))
        green_palette = np.concatenate((green_palette_start, red_palette_data))
        blue_palette = np.concatenate((blue_palette_start, red_palette_data))
    else:
        red_palette = red_palette_data
        green_palette = green_palette_data
        blue_palette = blue_palette_data

    red = red_palette[dcm.pixel_array]
    green = green_palette[dcm.pixel_array]
    blue = blue_palette[dcm.pixel_array]

    out = np.stack((red, green, blue), axis=-1)

    if lut_bits_per_pixel == 16:
        out = (out // 256).astype(np.uint8)

    return out


def OutputReport(FileName, JPGpath, DirAndFile):
    newFileName = FileName.split(".")[0] + ".jpg"
    dcm = pydicom.read_file(DirAndFile.strip())
    temp = get_pixel_data_with_lut_applied(dcm)
    os.chdir(JPGpath)
    cv.imwrite(newFileName, temp)


# 获得一个不重复随机数
def getRandomList(List1, num):
    resultList = random.sample(range(0, len(List1)), num)
    return resultList


def renameFile(oldNameList, label):
    """Takes context from the file by utf-8 encode.
        fileName: String of full of file name.

        Returns 1 String list:
        List: [imgPath1, imgPath2, imgPath3...] imgPath : String.
    """
    from os import path
    newNameList = []
    n = 0
    fileDirectory = oldNameList[0]
    newName = path.basename(fileDirectory)
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


# 裁剪图片与压缩图片
def cropImg(PicFile, outputDirectory, need_Crop=True):
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
    from os import path
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
    blank_output = []
    if message.get('words_result_num') != 0:
        for text in message.get('words_result'):
            diagnose = text.get('words')
    else:
        blank_output.append(fileName)
        diagnose = ''
    return blank_output, fileName, diagnose
