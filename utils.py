import inspect
import os
import shutil
import traceback


def read_file(file_dir):
    DCM_Images = []
    temp = []  # 文件夹目录
    for root, sub_folders, files in os.walk(file_dir):
        for name in files:
            DCM_Images.append(os.path.join(root, name))
        for name in sub_folders:
            temp.append(os.path.join(root, name))
    return DCM_Images


def create_dir(work_dir, createDirectory):
    try:
        for directory in createDirectory:
            if not os.path.exists(os.path.join(work_dir, directory)):
                os.makedirs(os.path.join(work_dir, directory))
                print("%s 文件夹创建成功" % directory)
            else:
                print("%s 文件夹已经存在" % directory)
    except Exception as e:
        print(e)


def move_file(src_path, dst_path, file):
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


def IsDCM(Path_file):
    fileNameList = []
    for pathString in Path_file:
        fileName = pathString.split("\\")[1]
        fileNameList.append(fileName)
    return fileNameList


def loadData(infile):
    f = open(infile, 'r')
    sourceInLine = f.readlines()
    return sourceInLine


def WriteData(list1, name):
    file = open(name + ".list", "w")
    file.write('\n'.join(list1))
    file.close()


def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]
