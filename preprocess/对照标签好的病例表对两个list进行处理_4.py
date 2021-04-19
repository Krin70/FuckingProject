import numpy as np

import utils


def compareFeatureAndLabeledPatientNum(MRI_image):
    New_MRI_image_List = []
    for file in MRI_image:
        PatientNum = file.split("\\")[-1].split("_")[0]
        if PatientNum in read_dictionary:
            New_MRI_image_List.append(file)
    return New_MRI_image_List


if __name__ == "__main__":
    read_dictionary = np.load('./Label/ReportLabel.npy', allow_pickle=True).item()

    MalePath = r".\Male_MRI_image.list"
    FemalePath = r".\Female_MRI_image.list"

    Male_MRI_image = utils.loadData(MalePath)
    Male_MRI_image = [i.strip() for i in Male_MRI_image]
    Male_MRI_image = compareFeatureAndLabeledPatientNum(Male_MRI_image)
    Female_MRI_image = utils.loadData(FemalePath)
    Female_MRI_image = [i.strip() for i in Female_MRI_image]
    Female_MRI_image = compareFeatureAndLabeledPatientNum(Female_MRI_image)

    Male_MRI_image_name = utils.retrieve_name(Male_MRI_image)[0]
    Female_MRI_image_name = utils.retrieve_name(Female_MRI_image)[0]

    utils.WriteData(Male_MRI_image, Male_MRI_image_name)
    utils.WriteData(Female_MRI_image, Female_MRI_image_name)
