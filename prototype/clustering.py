# -*- coding: utf-8 -*-
#
# measure.py
#
# The module is part of prototype.
#

"""
Clustering of target region centroids according to shortest euclidean distance
to cluster regions.
"""

__author__ = 'Severin E. R. Langberg'
__email__ = 'Langberg91@gmail.no'
__status__ = 'Operational'


import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

from utils import _check_parameter


def _nearest_region(target, regions, distance_thresh):
    # Determines the coordinate pair among the contours of the regions that
    # are closest to the coordinate part of the target centroid according to the
    # specified distance metric. Returns the region identification number
    # corresponding to the closest region.

    closest_region_id = 0
    min_dist = np.float('inf')

    _target = np.array([target])

    for region_id, region in regions.items():

        dist = euclidean_distances(region, _target)
        candidate_dist = np.absolute(np.min(dist))

        if candidate_dist < min_dist:
            min_dist = candidate_dist
            closest_region_id = region_id

    if min_dist > distance_thresh:
        return None
    else:
        return closest_region_id


def nearest_region_clustering(targets, regions, distance_thresh=10.0):
    """Assigns target centroids to the closest region.

    Args:
        targets (dict): The coordinate pairs of each target centroid as
            key-value pairs.

        regions (dict: The coordinate paris for each contour defining each
            image region object as key-value pairs.

        distance_thresh (float): The maximum accepted distance between a target
            and the closest region.

    Returns:
        clusters (dict): The target coordiantes assigned to each cluster as
            key-value pairs.

    """

    _check_parameter('targets', dict, targets)
    _check_parameter('regions', dict, regions)
    _check_parameter('distance_thresh', (int, float), distance_thresh)

    clusters = {region_id: [] for region_id in regions.keys()}

    for target_id, centroid in targets.items():

        region_id = _nearest_region(centroid, regions, distance_thresh)

        if region_id is None:
            continue
        else:
            clusters[region_id].append(centroid)

    return clusters
