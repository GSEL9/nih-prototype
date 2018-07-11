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

    # TODO: Change function to something like:
    # num_regions = labeled.max()
    # wanted_blobs = [True] * num_regions
    # regions = regionprops(labeled)
    # for num, blob in enumerate(regions):
    #     wanted_blobs[num] = _is_wanted_blob(blob)
    # filtered = _select_regions(labeled, wanted_blobs)

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

    # TODO:
    filtered = _select_regions(labeled, wanted_blobs)

    return filtered


# TODO: Compute skimage.regionprops for labeled image in region_selection().
# for each blob, check if blob is wanted based on blob props.
def _is_wanted_blob(blob, min_area, max_area, min_solidity):
    # Evaluates a set of blob characteristics in order to determine the the
    # blob is actually a cluster, or noise.

    wanted = True

    if not min_area <= blob.area <= max_area:
        wanted = False

    if not min_solidity <= blobl.solidity <= max_solidity:
        wanted = False

    """Solidity is area fraction of the region as compared to its convex hull.
    The convex hull is what you'd get if you wrapped a rubber band around your
    region. So solidity is what fraction of the actual area your region is. For
    any convex object it's 1. An asterisk might have a solidity of around 0.5,
    while a thin "L" shape (or T or E, etc.)would have a very low solidity.
    The more bays, nooks, and crannies it has, the lower the solidity.
    """

    if not min_eccentricity <= blobl.eccentricity <= max_eccentricity:
        wanted = False

    # Straight line has eccentricity = inf. A pefect circle has eccentricity = 0.

    return wanted


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
