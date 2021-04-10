'''

Input script for colSizeMeasurer.py
User-friendly
Written by George Walters-Marrah
Last updated: 6/26/2019

'''
# import the colony measurer script
import colSizeMeasurer as cm

'''
Notes

The function to measure colony size will be called like below:
cm.measure(imFolder, imVector, imStrain, imPlate, imRepNum, imType, firstMask, secondMaskLow, secondMaskHigh, smallSize, largeSize, stdThreshold, results = True, manual = False, stdManual = .65)
Last three values are not necessarily needed because they have default values

Importing the image File:
    The image file must be named like this: vector_strain_plate_repnumber.filetype
    If any of these do not apply to your colony image just put NA.
    Image file datatype must be uint8

    imFolder: The folder name where the image file is located. Must be a string.
    imVector: The vector name of the image. Must be a string.
    imStrain: The strain name of the image. Must be a string.
    imPlate: The resistance or the plate in the image. Must be a string.
    imRepNum: The replicate number of the image. Must be a string.
    imType: the image type used. Must be a string. Ex. '.png'

Cleaning up the image:
    Large pixel intensity numbers have lighter intensities and small pixel intensity numbers have darker intensities. Change numbers as needed.
    firstMask: A number that specifies the pixel intesity that will be masked. Every pixel with an intensity above this number will be removed (light pixels).
    *Filter makes the image uniform
    secondMaskLow: A number that specifies the pixel intesity that will be masked. Every pixel with an intensity below this number will be removed (dark pixels).
    secondMaskHigh: A number that specifies the pixel intesity that will be masked. Every pixel with an intensity above this number will be removed (light pixels).
        Should be more stringent(lower number) than the first mask.
    smallSize: A number that specifies the size of small objects that will be removed. Every object with less pixels than this number will be removed.
    largeSize: A number that specifies the size of large objects that will be removed. Every object with more pixels than this number will be removed.
    stdThreshold: Number that specifies how symmetrical the colonies must be. The lower the number the more symmetrical the colonies must be.
        Unsymmetrical colonies are disposed of.

Measuring colony size:
    results: Shows the images and analyzing step by step if True. If False, skips showing these things.
        default is True. Change as needed.
    manual: allows you to manually analyze/skip outliers if True. Analyzes every colony that survives "clean up" if False.
        default is False. Change as needed.
    stdManual: a number that specifies what an outlier is in the dataset. The number of standard deviations away from the median.
        Everything outside of that will be considered an outlier and will prompt you to decide whether or not to analyze it.
        A good number is 1 standard deviations which is the default. Change if you feel the need to.

Suggestions:
        Run this program with the image with your largest colonies and the image with your smallest colonies.
        Run with results as True and manual as False.
        Change the clean up values until the clean up is up to par.
        Take those optimized numbers and use the colSizeAnalyzer to analyze all your images processively with manual set to True.
'''

# code needed to run program
cm.measure(imFolder = 'BruNrnC_Rescue_042419', imVector = 'empty', imStrain = 'dOrn', imPlate = 'Gm+Ara', imRepNum = 'NA', imType = '.png', firstMask = 190, secondMaskLow = 50, secondMaskHigh = 185, smallSize = 2, largeSize = 235, stdThreshold = 1.5, results = True, manual = False, stdManual = 1)
