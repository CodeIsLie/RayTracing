from Figure import *
from Light import *
from space_model import SpaceModel

import numpy as np


walls = []
figures = []


def get_room():
    room = get_cube()
    k_size = 10
    # do scaling
    room.scale(k_size, k_size, k_size)
    room.move(k_size/2, k_size/2, k_size/2)
    del room.polygons[-2]

    return room


def get_cube():
    p1 = np.array([-0.5, -0.5, -0.5])
    p2 = np.array([0.5, -0.5, -0.5])
    p3 = np.array([-0.5, 0.5, -0.5])
    p4 = np.array([-0.5, -0.5, 0.5])
    p5 = np.array([0.5, 0.5, -0.5])
    p6 = np.array([0.5, -0.5, 0.5])
    p7 = np.array([-0.5, 0.5, 0.5])
    p8 = np.array([0.5, 0.5, 0.5])

    edge_points = np.array([
        [p1, p2, p5, p3],
        [p1, p2, p6, p4],
        [p1, p3, p7, p4],
        [p8, p7, p4, p6],
        [p8, p7, p3, p5],
        [p8, p6, p2, p5]
    ])
    polygons = [Polygon(points) for points in edge_points]
    p = 2
    return Figure(polygons, [0, 0, 0])

# ASSUMING that field of view is 90 degrees on X and Y
def get_camera():
    return np.array([5, 15, 5])

cube = get_cube()
room = get_room()
print(room)
pass