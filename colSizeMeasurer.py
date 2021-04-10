'''

Measures the square area of colonies in an image file.
Written by George Walters-Marrah
Last updated: 6/26/2019

'''

# import needed packages
import imageio
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
from skimage import morphology as morph
import os.path
from os import path

def remove_large_objects(ar, max_size=64, connectivity=1, in_place=False):
    """Remove objects larger than the specified size.
    Expects ar to be an array with labeled objects, and removes objects
    larger than max_size. If `ar` is bool, the image is first labeled.
    This leads to potentially different behavior for bool and 0-and-1
    arrays.
    Parameters
    ----------
    ar : ndarray (arbitrary shape, int or bool type)
        The array containing the objects of interest. If the array type is
        int, the ints must be non-negative.
    max_size : int, optional (default: 64)
        The largest allowable object size.
    connectivity : int, {1, 2, ..., ar.ndim}, optional (default: 1)
        The connectivity defining the neighborhood of a pixel. Used during
        labelling if `ar` is bool.
    in_place : bool, optional (default: False)
        If ``True``, remove the objects in the input array itself.
        Otherwise, make a copy.
    Raises
    ------
    TypeError
        If the input array is of an invalid type, such as float or string.
    ValueError
        If the input array contains negative values.
    Returns
    -------
    out : ndarray, same shape and type as input `ar`
        The input array with small connected components removed.
    Examples
    --------
    >>> from skimage import morphology
    >>> a = np.array([[0, 0, 0, 1, 0],
    ...               [1, 1, 1, 0, 0],
    ...               [1, 1, 1, 0, 1]], bool)
    >>> b = morphology.remove_small_objects(a, 6)
    >>> b
    array([[False, False, False, False, False],
           [ True,  True,  True, False, False],
           [ True,  True,  True, False, False]], dtype=bool)
    >>> c = morphology.remove_small_objects(a, 7, connectivity=2)
    >>> c
    array([[False, False, False,  True, False],
           [ True,  True,  True, False, False],
           [ True,  True,  True, False, False]], dtype=bool)
    >>> d = morphology.remove_small_objects(a, 6, in_place=True)
    >>> d is a
    True
    """

    if in_place:
        out = ar
    else:
        out = ar.copy()

    if max_size == 0:  # shortcut for efficiency
        return out

    if out.dtype == bool:
        selem = ndi.generate_binary_structure(ar.ndim, connectivity)
        ccs = np.zeros_like(ar, dtype=np.int32)
        ndi.label(ar, selem, output=ccs)
    else:
        ccs = out

    try:
        component_sizes = np.bincount(ccs.ravel())
    except ValueError:
        raise ValueError("Negative value labels are not supported. Try "
                         "relabeling the input with `scipy.ndimage.label` or "
                         "`skimage.morphology.label`.")

    too_big = component_sizes > max_size
    too_big_mask = too_big[ccs]
    out[too_big_mask] = 0

    return out

def measure(imFolder, imVector, imStrain, imPlate, imRepNum, imType , firstMask, secondMaskLow, secondMaskHigh, smallSize, largeSize, stdThreshold, results = True, manual = False, stdManual = 1):
    # make an object with the filepath to the image you want to analysis
    imName =  imVector + '_' + imStrain + '_' + imPlate + '_' + imRepNum
    imGenericName = imVector + '_' + imStrain + '_' + imPlate
    imPath = imFolder + '/' + imName + imType

    # check if the path exists
    if path.exists(imPath):
        pass
    else:
        raise ValueError('The PATH specified does not exist. Change PATH and try again.')

    # read in plate picture as an uint8 *only works with uint8 dtypes*
    im = imageio.imread(imPath)

    # prints the dtype and min/max. Values should be: dtype = uint8, min = ~0, max = ~255
    dtype = im.dtype

    if results:
        print('Data type:', dtype)
        print('Min. value:', im.min())
        print('Max value:', im.max())
        print('')

    # raises error of image type isn't uint8
    if dtype != 'uint8':
        raise ValueError(imPath + ' must be uint8. Change image file to uint8 then try again.')

    # Gets rid pure white regions of the image
    mask = im < firstMask
    im_mask = np.where(mask, im, 0)

    # show images
    if results:
        fig, axes = plt.subplots(1,2)
        axes[0].imshow(im, cmap = 'gray')
        plt.axis('off')
        axes[1].imshow(im_mask, cmap = 'gray')
        plt.axis('off')
        plt.show()

    # Uniforms the photo to make the edges clearer and easier to detect
    im_filt = ndi.uniform_filter(im_mask, size=3)

    # searches for the gray areas (where colonies are).
    col_mask1 = im_filt > secondMaskLow
    col_mask2 = im_filt < secondMaskHigh
    col_mask = col_mask1 & col_mask2
    im_colonies = np.where(col_mask, im, 0)

    # Creates label objects
    labels, nlabels = ndi.label(col_mask)

    # Get initial amount of objects found by mask
    bboxinitial = ndi.find_objects(labels)
    if results:
        print('Objects found in initial mask for ' + imPath + ': ', len(bboxinitial))
        print('')

    # show images
    if results:
        fig, axes = plt.subplots(1,2)
        axes[0].imshow(im_filt, cmap = 'gray')
        plt.axis('off')
        axes[1].imshow(im_colonies, cmap = 'gray')
        plt.axis('off')
        plt.show()

    # Removes abnormally small or large objects
    cols_cleaned1 = morph.remove_small_objects(labels, smallSize)
    cols_cleaned2 = remove_large_objects(cols_cleaned1, largeSize)
    bboxes = ndi.find_objects(cols_cleaned2)

    # shows images
    if results:
        fig, axes = plt.subplots(1,2)
        axes[0].imshow(im_colonies, cmap = 'gray')
        plt.axis('off')
        axes[1].imshow(cols_cleaned2, cmap = 'rainbow')
        plt.axis('off')
        plt.show()

    # Calculates the colony size
    col_size_init = []
    for index in range(len(bboxes)):
        # excludes colonies with abnormal morphology
        npixel = 0
        dpixel = 6.45*6.45
        colony = cols_cleaned2[bboxes[index]]
        std = np.std(colony.shape[:2])
        if (std <= stdThreshold):
            for image in colony:
                for pixel in image:
                    if pixel > 0:
                        npixel += 1
            meas = npixel*dpixel
            measFin = np.around(meas, 2)
            col_size_init.append(measFin)
        else: pass

    # allows you to manually discard bad data points.
    if manual:
        np_col_size_init = np.array(col_size_init)
        col_size = []
        for index in range(len(bboxes)):
            # excludes colonies with abnormal morphology and perfect squares
            size_std = np.std(np_col_size_init)
            size_median = np.median(np_col_size_init)
            npixel = 0
            dpixel = 6.45*6.45
            colony = cols_cleaned2[bboxes[index]]
            std = np.std(colony.shape[:2])
            if (std <= stdThreshold):
                for image in colony:
                    for pixel in image:
                        if pixel > 0:
                            npixel += 1
                meas = npixel*dpixel
                measFin = np.around(meas, 2)
            else:
                measFin = False

            # allows to manually sift through outliers
            if measFin == False:
                pass
            elif measFin < size_median - stdManual * size_std or measFin > size_median + stdManual * size_std:
                    plt.imshow(im_colonies[bboxes[index]], cmap = 'gray')
                    plt.axis('off')
                    plt.show()
                    ques = input('Do you want to analyze that colony from ' + imName + '(' + imFolder + ')' + '? If yes, type Y. If no, type N:')
                    if ques == 'Y' or ques == 'y':
                        col_size.append(measFin)
                        print('Colony analyzed.')
                    elif ques == 'N' or ques == 'n':
                        print('Colony skipped.')
                    else:
                        doubleCheck = input('Did you mean to put N?:')
                        if doubleCheck == 'N' or doubleCheck == 'n':
                            col_size.append(measFin)
                            print('Colony analyzed.')
                        else:
                            print('Colony skipped.')
            else:
                col_size.append(measFin)
        np_col_size = np.array(col_size)
    else:
        np_col_size = np.array(col_size_init)

    # contains all the calculated diameter values and summarized data
    colMean = np.around(np.mean(np_col_size),2)
    colMedian = np.around(np.median(np_col_size),2)
    colStd = np.around(np.std(np_col_size),2)
    data = [imGenericName, colMean, colMedian, colStd, imFolder, imVector, imStrain, imPlate, imRepNum, np_col_size]

    # prints out a summary of the results
    if results:
        print('Data for', imName, '(' + imFolder + ')')
        print('Final amount of colonies measured:', len(np_col_size))
        print('Mean of data: ', colMean)
        print('Median of data: ', colMedian)
        print('Standard deviation of data: ', colStd)
        print('')

    print(imName, 'area calculated.')
    print('')

    return data

def main():
    measure('', '', '', '', '', '', firstMask = 190, secondMaskLow = 50, secondMaskHigh = 185, smallSize = 2, largeSize = 235, stdThreshold = 1)


if __name__ == '__main__': main()
