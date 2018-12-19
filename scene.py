from Figure import *
from Light import *
from space_model import SpaceModel

import numpy as np



figures = []


# cube1 = Figure(polygons, np.array([2, 2, 0.5]))




def get_cube():
    p1 = np.array([-0.5, -0.5, -0.5])
    p2 = np.array([0.5, -0.5, -0.5])
    p3 = np.array([-0.5, 0.5, -0.5])
    p4 = np.array([-0.5, 0.5, 0.5])
    p5 = np.array([0.5, 0.5, -0.5])
    p6 = np.array([0.5, -0.5, 0.5])
    p7 = np.array([-0.5, 0.5, 0.5])
    p8 = np.array([0.5, 0.5, 0.5])

    edge_points = [
        [p1, p2, p5, p3],
        [p1, p2, p6, p4],
        [p1, p3, p7, p4],
        [p8, p7, p4, p6],
        [p8, p7, p3, p5],
        [p8, p6, p2, p5]
    ]
    polygons = [Polygon(points) for points in edge_points]

    return Figure(polygons)