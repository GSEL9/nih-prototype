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


import utils

import numpy as np

from skimage import measure


def region_labeling(image, neighbors=8, background=0):
    """Labels blobs of a binary image.

    Args:
        image (array-like): Input image. Is converted to grayscale if RGB.

        neighbors ():

        background ():

    Returns:
        labeled (array-like):

    """

    _image = utils._check_image(image)

    labeled = measure.label(
        _image, neighbors=neighbors, background=background
    )

    return labeled


def region_selection(image, constraints):
    """Retain only the regions from a binary image with an area inside the
    specified range.

    Args:
        image (array-like): Input image. Is converted to grayscale if RGB.

        constraints (dict):

    Returns:
        filtered (array-like):

    """

    _image = utils._check_image(image)
    _constraints = utils._check_blob_constraints(constraints)

    labeled = measure.label(_image, neighbors=8, background=0)

    num_regions = labeled.max()
    wanted_blobs = [True] * num_regions

    regions = measure.regionprops(labeled)

    for num, blob in enumerate(regions):
        wanted_blobs[num] = _is_wanted_blob(blob, _constraints)

    filtered = _select_regions(labeled, wanted_blobs)

    return filtered


def _is_wanted_blob(blob, limits):
    # Evaluates a set of blob characteristics in order to determine the the
    # blob is actually a cluster, or noise.

    wanted = True

    if not limits['min_area'] <= blob.area <= limits['max_area']:
        wanted = False

    # The more bays, nooks, and crannies it has, the lower the solidity.
    if not limits['min_solidity'] <= blob.solidity <= limits['max_solidity']:
        wanted = False

    # Straight line eccentricity = inf. Pefect circle eccentricity = 0.
    if not limits['min_eccent'] <= blob.eccentricity <= limits['max_eccent']:
        wanted = False

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
