# -*- coding: utf-8 -*-
#
# segmentation.py
#
# The module is part of prototype.
#

"""
Binarizing images by a selected threshold algorithm.
"""

__author__ = 'Severin E. R. Langberg'
__email__ = 'Langberg91@gmail.no'
__status__ = 'Operational'


import numpy as np

from skimage.segmentation import join_segmentations

from scipy.ndimage.morphology import binary_fill_holes

from utils import _check_image


def select_targets(image1, image2):
    """Creates an image containing the overlapping regions from the passed
    images.

    Args:
        image1 (array-like): A binary image serving as reference in comparing
            image regions with another image.

        image2 (array-like): A binary image serving as samples in comparing
            image regions with the reference image.

    Returns:
        targets (array-like): An image containing the common regions in both of
            the passed images.

    """

    _image1, _image2 = _check_image(image1), _check_image(image2)

    masked = join_segmentations(_image1, _image2)
    masks = np.unique(masked)

    targets = np.zeros_like(_image1)
    targets[masked == masks[-1]] = 255

    return targets


def clear_borders(image):
    """Creates an image containing only the inner cluter regions by removing
    the foreground borders of the original image around a center region of the
    image.

    Args:

    Returns:

    """

    _image = _check_image(image)

    center_region = binary_fill_holes(_image)

    center = np.zeros_like(_image)
    center[center_region == True] = 255

    cleared = _image - center

    return -cleared
