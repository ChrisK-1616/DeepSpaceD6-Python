"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       utils.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Utility functions
"""

# Imports
import math


# Consts
# Globals
# Classes


# Functions
def centre_image(image):
    """
    Sets an image's anchor point to its center

    :param: image - image with which to set centre anchor

    :returns: nothing
    """
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


def distance(point_1=(0, 0), point_2=(0, 0)):
    """
    Returns the distance between two points

    :param point_1:
    :param point_2:
    :return:
    """
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)


def direction(x, y):
    if x > 0.001:
        return math.atan(-y / x)

    if x < -0.001:
        return math.atan(-y / x) + math.pi

    if y > 0.001:
        return 3 * math.pi / 2

    if y < -0.001:
        return math.pi / 2

    return 0  # No direction
