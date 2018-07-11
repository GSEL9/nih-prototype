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


def _check_parameter(parameter, dtype, value):
    # Parameter value type checking.

    if not isinstance(value, dtype):
        raise TypeError('`{param}` must be {dtype}, and not {err_dtype}'
        ''.format(param=parameter, dtype=dtype, err_dtype=type(value)))
