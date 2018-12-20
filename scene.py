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

    for i in range(len(room.polygons)):
        room.polygons[i].normal *= -1

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


sphere_1 = Sphere(np.array([5,2,2]), 2, (200, 100, 150))
sphere_2 = Sphere(np.array([6, 7, 1]), 1, (30, 200, 100))

cube_1 = get_cube()
k_cube_1 = 3
cube_1.scale(k_cube_1, k_cube_1, k_cube_1)
cube_1.move(2+k_cube_1/2, k_cube_1/2 + 6, k_cube_1/2)
cube_1.set_color((80, 40, 200))
# cube_1.polygons[5].transparency = -1

scene_figures = [get_room(), sphere_1, cube_1]

light1 = LightSource(np.array([5, 2, 9.95]), 0.5)
light2 = LightSource(np.array([6, 7, 9.95]), 0.5)
scene_lights = [light1, light2]
scene_camera = get_camera()

print(get_room().get_intersection(Ray(np.array([10, 5, 5]), np.array([-1, 0, 0]))) )