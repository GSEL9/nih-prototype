# -*- coding: utf-8 -*-
#
# measure.py
#
# The module is part of prototype.
#

"""
"""

__author__ = 'Severin E. R. Langberg'
__email__ = 'Langberg91@gmail.no'
__status__ = 'Operational'


import numpy as np

from skimage import measure

from utils import _check_image


def region_labeling(image, neighbors=8, background=0):
    """Labels blobs of a binary image.

    Args:
        image (array-like): Input image. Is converted to grayscale if RGB.

        neighbors ():

        background ():

    Returns:
        labeled (array-like):

    """

    _image = _check_image(image)

    labeled = measure.label(
        _image, neighbors=neighbors, background=background
    )

    return labeled


def region_selection(image, nbins=None, min_area=None, max_area=None):
    """Retain only the regions from a binary image with an area inside the
    specified range.

    Args:
        image (array-like): Input image. Is converted to grayscale if RGB.

        nbins (int): The number of bins used to calculate histogram as input to
            thresholding algorithms. Defaults to 256 bins.

        min_area (int): Smallest included blob size.

        max_area (int): Largest included blob size.

    Returns:
        filtered (array-like):

    """

    _image = _check_image(image)

    labeled = measure.label(_image, neighbors=8, background=0)

    min_area = -np.float('inf') if min_area is None else min_area
    max_area = np.float('inf') if max_area is None else max_area

    nbins = np.unique(labeled).size + 1 if nbins is None else nbins

    _areas, _ = np.histogram(labeled, bins=range(nbins))
    areas = np.trim_zeros(_areas[1:], 'b')

    num_regions = labeled.max()
    wanted_blobs = [True] * num_regions
    for num in range(num_regions):
        if not min_area <= areas[num] <= max_area:
            wanted_blobs[num] = False

    filtered = _select_regions(labeled, wanted_blobs)

    return filtered


def _select_regions(image, wanted_blobs, foreground=255, background=0):
    # Removes unwanted blobs and relabels wanted blobs. Returns relabeled image.

    filtered = np.zeros_like(image, dtype=np.uint8)

    num_blobs = len(wanted_blobs)
    unwanted = np.arange(1, num_blobs + 1)[np.logical_not(wanted_blobs)]
    wanted = np.arange(1, num_blobs + 1)[wanted_blobs]

    # Remove unwanted blobs:
    for unwanted_blob in unwanted:
        filtered[image == unwanted_blob] = background

    # Relabel wanted blobs:
    for new_label, wanted_blob in enumerate(wanted):
        filtered[image == wanted_blob] = foreground

    return filtered
