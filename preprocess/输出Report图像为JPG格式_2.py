# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 16:56:13 2020

@author: XEON
"""
import os
from preprocess import utils


if __name__ == "__main__":
    ROOT_DIR = os.getcwd()
    utils.create_dir(ROOT_DIR, [r"./Label/Report"])
    for reportPath in utils.loadData("Report_imagePath.list"):
        os.chdir(reportPath.replace(reportPath.split("\\")[-1], ''))
        utils.OutputReport(reportPath.split("\\")[-1].strip(), r"J:\Medical\preprocess\Label\Report", reportPath)
    print("finished")
