# -*- coding: utf-8 -*-
#
# utils.py
#
# The module is part of prototype.
#

"""
The prototype utilities module.
"""

__author__ = 'Severin E. R. Langberg'
__email__ = 'Langberg91@gmail.no'
__status__ = 'Operational'


import numpy as np


# Evaluated constraints on blob characteristics.
CONSTRAINTS = {
    'min_area': -np.float('inf'),
    'max_area': np.float('inf'),
    'min_solidity': -np.float('inf'),
    'min_solidity': np.float('inf'),
    'min_eccent': -np.float('inf'),
    'max_eccent': np.float('inf')
}


def _check_image(image):
    # Returns a copy on the image. If not the image is grayscale the average
    # across the channels is returned.

    img_shape = np.shape(image)

    if len(img_shape) == 2:
        _image = image.copy()
    elif len(img_shape) == 3:
        _image = np.mean(image.copy(), axis=2)
    else:
        raise RuntimeError('Image should be 2D not {}D'.format(len(img_shape)))

    return _image


def _check_blob_constraints(constraints):

    for key in constraints.keys():
        if not key in CONSTRAINTS.keys():
            raise ValueError('Invalid key: `{}` not in constraint keys:\n {}'
                             ''.format(key, list(CONSTRAINTS.keys())))

    CONSTRAINTS.update(constraints)

    return CONSTRAINTS

def _check_parameter(parameter, dtype, value):
    # Parameter value type checking.

    if not isinstance(value, dtype):
        raise TypeError('`{param}` must be {dtype}, and not {err_dtype}'
        ''.format(param=parameter, dtype=dtype, err_dtype=type(value)))
