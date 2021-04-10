'''

Measures the square area of colonies in several image files and exports data as an excel sheet.
Written by George Walters-Marrah
Last updated: 6/26/2019

'''

# import needed packages
import colSizeMeasurer as cm
import numpy as np
import pandas as pd
import os.path
from os import path
import imageio

# analyzes several images at processively
class analyzer:
    # initializes the analyzer with all the information it needs
    def __init__(self, imFolders, imVectors, imStrains, imPlates, imRepNums, imType, firstMask, secondMaskLow, secondMaskHigh, smallSize, largeSize, stdThreshold, control):
            self._imFolders = imFolders
            self._imVectors = imVectors
            self._imStrains = imStrains
            self._imPlates = imPlates
            self._imRepNums = imRepNums
            self._imType = imType
            self._control = control
            self._firstMask = firstMask
            self._secondMaskLow = secondMaskLow
            self._secondMaskHigh = secondMaskHigh
            self._smallSize = smallSize
            self._largeSize = largeSize
            self._stdThreshold = stdThreshold
            self._control = control

    def checkFiletype(self):
        fileList = []

        for folder in range(len(self._imFolders)):
            imFolder = self._imFolders[folder]
            for vector in range(len(self._imVectors)):
                imVector = self._imVectors[vector]
                for strain in range(len(self._imStrains)):
                    imStrain = self._imStrains[strain]
                    for plate in range(len(self._imPlates)):
                        imPlate = self._imPlates[plate]
                        for repNum in range(len(self._imRepNums)):
                            imRepNum = self._imRepNums[repNum]

                            # Check if the PATH exists
                            filePath = imFolder + '/' + imVector + '_' + imStrain + '_' + imPlate + '_' + imRepNum + self._imType
                            if path.exists(filePath):
                                imCheck = imageio.imread(filePath)
                                dtypeCheck = imCheck.dtype
                                if dtypeCheck != 'uint8':
                                    fileList.append(filePath)

        if len(fileList) == 0:
            print('Files in folder(s) ' + str(self._imFolders) + ' checked.')
        else:
            raise ValueError(str(fileList) + ' must be uint8. Change image file(s) to uint8 then try again.')

    # defines and gets the size of the control where it will be
    def getControl(self):
        data = []
        for Folder in range(len(self._imFolders)):
            imFolder = self._imFolders[Folder]
            for repNum in range(len(self._imRepNums)):
                imRepNum = self._imRepNums[repNum]

                # Check if the PATH exists
                controlPath = imFolder + '/' + self._control[0] + '_' + self._control[1] + '_' + self._control[2] + '_' + imRepNum + self._imType
                if path.exists(controlPath):
                    # Analyze data if the PATH exists
                    controlData = cm.measure(imFolder, self._control[0], self._control[1], self._control[2], imRepNum, self._imType, self._firstMask, self._secondMaskLow, self._secondMaskHigh, self._smallSize, self._largeSize, self._stdThreshold, False, True)
                    data.append(controlData[1])
                # Decide what to do if PATH does not exist
                else:
                    check = input('The PATH "' + controlPath + '" does not exist. Do you want to continue? If yes, type Y. If no, type N:')
                    if check == 'Y' or check == 'y':
                        print('PATH ignored.')
                    elif check == 'N' or check == 'n':
                        raise ValueError('Program stopped. Change PATH and try again.')
                    else:
                        doubleCheck = input('Did you mean to put N?:')
                        if doubleCheck == 'Y' or doubleCheck == 'y':
                            raise ValueError('Program stopped. Change PATH and try again.')
                        else:
                            print('PATH ignored.')
        np_data = np.array(data)
        print('')
        print('||| Control created using', self._control[0] + '_' + self._control[1] + '_' + self._control[2], '|||')
        return np.around(np.mean(np_data),2)

    # analyzes the data images in a processive manner
    def analyze(self, control):
        fin_data = []

        colName = []
        colMean = []
        colMedian = []
        colStd = []
        colFolder = []
        colVector = []
        colStrain = []
        colPlate = []
        colRepNum = []
        colData = []
        colRatio = []

        for folder in range(len(self._imFolders)):
            imFolder = self._imFolders[folder]
            for vector in range(len(self._imVectors)):
                imVector = self._imVectors[vector]
                for strain in range(len(self._imStrains)):
                    imStrain = self._imStrains[strain]
                    for plate in range(len(self._imPlates)):
                        imPlate = self._imPlates[plate]
                        for repNum in range(len(self._imRepNums)):
                            imRepNum = self._imRepNums[repNum]

                            # Check if the PATH exists
                            dataPath = imFolder + '/' + imVector + '_' + imStrain + '_' + imPlate + '_' + imRepNum + self._imType
                            if path.exists(dataPath):
                                # Analyze data if the PATH exists
                                initial_data = cm.measure(imFolder, imVector, imStrain, imPlate, imRepNum, self._imType, self._firstMask, self._secondMaskLow, self._secondMaskHigh, self._smallSize, self._largeSize, self._stdThreshold, False, True)
                                ratio = np.around(initial_data[1]/control,3)
                                initial_data.append(ratio)
                                fin_data.append(initial_data)
                            # Decide what to do if PATH does not exist
                            else:
                                check = input('The PATH "' + dataPath + '" does not exist. Do you want to continue? If yes, type Y. If no, type N:')
                                if check == 'Y' or check == 'y':
                                    print('PATH ignored.')
                                elif check == 'N' or check == 'n':
                                    raise ValueError('Program stopped. Change PATH and try again.')
                                else:
                                    doubleCheck = input('Did you mean to put N?:')
                                    if doubleCheck == 'Y' or doubleCheck == 'y':
                                        raise ValueError('Program stopped. Change PATH and try again.')
                                    else:
                                        print('PATH ignored.')

        for l in fin_data:
            colName.append(l[0])
            colMean.append(l[1])
            colMedian.append(l[2])
            colStd.append(l[3])
            colFolder.append(l[4])
            colVector.append(l[5])
            colStrain.append(l[6])
            colPlate.append(l[7])
            colRepNum.append(l[8])
            colData.append(l[9])
            colRatio.append(l[10])
        all_data = [colName, colMean, colMedian, colStd, colFolder, colVector, colStrain, colPlate, colRepNum, colData, colRatio]
        return all_data

# makes and returns the data as an excel sheet. Can also combine data if you choose
def makeData(exportNameSum, exportNameRaw, listRawData):
# combines data if there is more than one dataset
    if len(listRawData) > 1:
        rawData = [[],[],[],[],[],[],[],[],[],[],[]]
        for data in  listRawData:
            for index in range(len(rawData)):
                rawData[index] = rawData[index] + data[index]
    else:
        rawData = listRawData[0]

# Make the dataframe of summary data
    dicSum = {'imName': rawData[0],
    'ratio': rawData[10],
    'mean': rawData[1],
    'median': rawData[2],
    'standardDeviation': rawData[3],
    'folder': rawData[4],
    'vector': rawData[5],
    'strain': rawData[6],
    'plate': rawData[7],
    'repetitionNumber': rawData[8],
    'rawData': rawData[9]}
    finalDataSum = pd.DataFrame(dicSum)
    colsSum = ['imName', 'ratio', 'mean', 'median', 'standardDeviation', 'folder', 'vector', 'strain', 'plate', 'repetitionNumber', 'rawData']
    finalDataSum = finalDataSum[colsSum]
    print('Summary Data')
    print(finalDataSum.iloc[:, 0:5])

# folders where raw data(size of every individual colony) will be stored
    imNameRaw = []
    measRaw = []
    amountRaw = []
    folderRaw = []

# creates the raw data
    for data in range(len(rawData[9])):
        for value in rawData[9][data]:
            imNameRaw.append(rawData[0][data])
            measRaw.append(value)
            amountRaw.append(len(rawData[9][data]))
            folderRaw.append(rawData[4][data])

    dicRaw = {'imName': imNameRaw,
    'area': measRaw,
    'dataPointNum': amountRaw,
    'folder': folderRaw}
    finalDataRaw = pd.DataFrame(dicRaw)
    colsRaw = ['imName', 'area', 'dataPointNum', 'folder']
    finalDataRaw = finalDataRaw[colsRaw]

# Write the data to the excel sheet
    excelFileSum = exportNameSum + '.xlsx'
    excelFileRaw = exportNameRaw + '.xlsx'
    finalDataSum.to_excel(excelFileSum)
    finalDataRaw.to_excel(excelFileRaw)

    print('')
    print('Check folder to see new ' + exportNameSum + ' and ' + exportNameRaw + ' file.')

def main():
    Folders = ['NrnC_Rescue_041319']
    imVectors = ['NA']
    imStrains = ['WT']
    imPlates = ['LB']
    imRepNums = ['1']
    imType = '.png'
    control = ['NA', 'dOrn', 'LB']

    col = analyzer(Folders, imVectors, imStrains, imPlates, imRepNums, imType, 190, 50, 185, 2, 235, 1.5, control)
    control_size = col.getControl()
    data = col.analyze(control_size)

    makeData('WTvdOrn_041319_sum', 'WTvdOrn_041319_raw', [data])

if __name__ == '__main__': main()
