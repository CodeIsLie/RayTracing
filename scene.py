from Figure import *
from Light import *
from ray import Ray
import numpy as np


walls = []
figures = []


def get_room():
    room = get_cube()
    k_size = 10
    # do scaling
    room.scale(k_size, k_size, k_size)
    room.move(k_size/2, k_size/2, k_size/2)
    del room.polygons[-1]
    room.polygons[0].color = (180, 180, 180)
    room.polygons[1].color = (240, 20, 20)
    room.polygons[2].color = (120, 180, 180)
    room.polygons[3].color = (100, 10, 240)
    room.polygons[4].color = (0, 10, 240)

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
    # p = 2
    return Cube(polygons, [0, 0, 0])

# ASSUMING that field of view is 90 degrees on X and Y
def get_camera():
    return np.array([15, 5, 5])

# cube = get_cube()
# room = get_room()
# print(room)

scene_figures = [get_room()]
scene_lights = []
scene_camera = get_camera()

print(get_room().get_intersection(Ray(np.array([10, 5, 5]), np.array([-1, 0, 0]))) )