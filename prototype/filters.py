# -*- coding: utf-8 -*-
#
# filters.py
#
# The module is part of prototype.
#

"""
Region labeling, filtering of regions based on region area and extracting the
overlapping regions in two binary images.
"""

__author__ = 'Severin E. R. Langberg'
__email__ = 'Langberg91@gmail.no'
__status__ = 'Operational'


import numpy as np

from skimage import filters

from utils import _check_image


def threshold(image, algorithm='otsu', nbins=256, thresh=None):
    """Creates a binary image from input image by thresholding the image
    according to specified algorithm.

    Args:
        image (array-like): Input image. Is converted to grayscale if RGB.

        algorithm (str, {'otsu', 'li', 'yen'}): Thresholding algorithm to
            determine threshold value. Defaults to 'otsu'.

        nbins (int): The number of bins used to calculate histogram as input to
            thresholding algorithms. Defaults to 256 bins.

        thresh (int): Optional threshold value to use instead of a thresholding
            algorithm. Defaults to None.

    Returns:
        binary (array-like): The binarized versinon of the input image
            according to selected thresholding algorithm.

    """

    _image = _check_image(image)

    binary = np.zeros_like(_image, dtype=np.uint8)

    if thresh is None:

        if algorithm == 'otsu':
            thresh = filters.threshold_otsu(_image, nbins=nbins)

        elif algorithm == 'li':
            thresh = filters.threshold_li(_image)

        elif algorithm == 'yen':
            thresh = filters.threshold_yen(_image, nbins=nbins)

        else:
            raise ValueError('Algorithm {} not available'.format(algorithm))

        binary[_image > thresh] = 255

    else:

        binary[_image > thresh] = 255

    return binary
