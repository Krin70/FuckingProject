# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 16:56:13 2020

@author: XEON
"""

import pydicom
import os
import cv2 as cv
import numpy as np
import utils


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
    FileName = FileName.split(".")
    newFileName = FileName[0] + ".jpg"
    dcm = pydicom.read_file(DirAndFile.strip())
    temp = get_pixel_data_with_lut_applied(dcm)
    os.chdir(JPGpath)
    cv.imwrite(newFileName, temp)


if __name__ == "__main__":
    ROOT_DIR = os.getcwd()
    createdir = [r"./Label/Report"]
    utils.create_dir(ROOT_DIR, createdir)

    # os.path.join(ROOT_DIR, createdir[0])

    file = r"Report.list"
    Report = utils.loadData(file)

    for i in Report:
        filename = i.split("\\")[-1]
        os.chdir(i.replace(filename, ''))
        OutputReport(filename.strip(), r"F:\OneDrive - THE GOD'S CHILD PROJECT\骨质疏松症项目\代码\整理代码\Label\report", i)
    print("finished")
