'''

Input script for colSizeAnalyzer.py
User-friendly
Written by George Walters-Marrah
Last updated: 6/26/2019

'''
# import the colony analyzer script
import colSizeAnalyzer as ca

'''
Notes

The class will be created like below:
colSizeAnalyzer = analyzer(Folders, imVectors, imStrains, imPlates, imRepNums, imType, firstMask, secondMaskLow, secondMaskHigh, smallSize, largeSize, stdThreshold, control)

Importing the image files:
    The image files must be named like this: vector_strain_plate_repnumber.filetype
    If any of these do not apply to your colony images just put NA.
    Image file datatype must be uint8
    checkFiletype quickly goes through all the image files and ensures they are uint8. If they are not, it throws an error.

    Folders: The folder names where the image files are located. Must be a list.
    imVectors: The vector names of the images. Must be a list.
    imStrains: The strain names of the images. Must be a list.
    imPlates: The resistance used or the plates in the images. Must be a list.
    imRepNums: The replicate numbers of the images. Must be a list.
    imType: the image type used. Must be a string. Ex. '.png'

Cleaning up the image:
    Large pixel intensity numbers have lighter intensities and small pixel intensity numbers have darker intensities. Change numbers as needed.
    firstMask: A number that specifies the pixel intesity that will be masked. Every pixel with an intensity above this number will be removed (light pixels).
    *Filter makes the image uniform*
    secondMaskLow: A number that specifies the pixel intesity that will be masked. Every pixel with an intensity below this number will be removed (dark pixels).
    secondMaskHigh: A number that specifies the pixel intesity that will be masked. Every pixel with an intensity above this number will be removed (light pixels).
        Should be more stringent(lower number) than the first mask.
    smallSize: A number that specifies the size of small objects that will be removed. Every object with less pixels than this number will be removed.
    largeSize: A number that specifies the size of large objects that will be removed. Every object with more pixels than this number will be removed.
    stdThreshold: Number that specifies how symmetrical the colonies must be. The lower the number the more symmetrical the colonies must be.
        Unsymmetrical colonies are disposed of.

Measuring colony size:
    control: the vector, strain, and plate of the control. Used to make the size ratio. Must be a list.
    Ex. control = ['pJHAPAOrn', 'dOrn', 'Gm']

Make and Export the data:
    Method will be used like below:
    makeData(exportNameSum, exportNameRaw, listRawData)

    exportNameSum: the export name of the excel file that will have the summary data
    exportNameRaw: the export name of the excel file that will have the raw data
    listRawData: list of all the raw data. Must be a list.
        if only one dataset in list it will export that one dataset.
        if more than one data set it will combine the datasets then export them.

Suggestions:
        Run the colSizeMeasurer program with the image with your largest colonies and the image with your smallest colonies.
        Run the colSizeMeasurer with results as True and manual as False.
        Change the clean up values until the clean up is up to par.
        Take those optimized numbers and use this program to analyze all your images processively.
'''

# code needed to run program
Folders = ['BruNrnC_Rescue_041819']
Folders2 = ['BruNrnC_Rescue_042419']
imVectors = ['D83A', 'empty', 'H78A', 'H204A', 'K102A', 'L30A', 'L30F', 'WT', 'Y14A', 'Y150A']
imStrains = ['dOrn']
imPlates = ['Gm+Ara']
imRepNums = ['NA']
imType = '.png'
firstMask = 190
secondMaskLow = 50
secondMaskHigh = 185
smallSize = 4
largeSize = 235
stdThreshold = 1.75
control = ['empty', 'dOrn', 'Gm+Ara']

# creates the analyzer
col = ca.analyzer(Folders, imVectors, imStrains, imPlates, imRepNums, imType, firstMask, secondMaskLow, secondMaskHigh, smallSize, largeSize, stdThreshold, control)
col2 = ca.analyzer(Folders2, imVectors, imStrains, imPlates, imRepNums, imType, firstMask, secondMaskLow, secondMaskHigh, smallSize, largeSize, stdThreshold, control)

# checks file type of images
col.checkFiletype()
col2.checkFiletype()

# gets the control datatype
control = col.getControl()
control2 = col2.getControl()

# analyzes the images
data = col.analyze(control)
data2 = col2.analyze(control2)

# creates and exports the data
ca.makeData('BruNrnCRescue_041819_sum', 'BruNrnCRescue_041819_raw', [data])
ca.makeData('BruNrnCRescue_042419_sum', 'BruNrnCRescue_042419_raw', [data2])
