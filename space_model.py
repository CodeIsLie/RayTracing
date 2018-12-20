from ray import *
from scene import *
import numpy as np

LEFT_BOUND = 0
RIGHT_BOUND = 10

BOT_BOUND = 0
TOP_BOUND = 10
HALF_DIST = (LEFT_BOUND + RIGHT_BOUND) / 2

AMBIENT = 230, 230, 230


class SpaceModel:
    def __init__(self, figures, lights, camera):
        self.figures = figures
        self.lights = lights
        self.camera = camera
        self.pixels = None

    def ray_tracing(self, width, height):
        color_mat = []
        for i in range(width):
            color_vec = []
            for j in range(height):
                # pixel coordinates
                y = LEFT_BOUND + (RIGHT_BOUND-LEFT_BOUND) * (i+0.5)/width
                z = TOP_BOUND - (TOP_BOUND - BOT_BOUND) * (j+0.5)/height

                point = np.array([10, y, z])
                ray = point - self.camera
                ray = Ray(point, ray / np.linalg.norm(ray))

                # print("for {0:.3f} and {1:.3f} intersection: ".format(y, z))
                color = self.ray_trace(ray)
                color_vec.append(color)
            color_mat.append(color_vec)

        self.pixels = color_mat

    def find_intersection(self, ray):
        res_intersection = None
        best_distance = 1e+20
        for fig in self.figures:
            intersection = fig.get_intersection(ray)
            if intersection is not None:
                distance = intersection[1]
                if distance < best_distance:
                    best_distance = distance
                    res_intersection = intersection

        return res_intersection

    def ray_trace(self, start_ray):
        #
        # start ray from camera center to pixel (virtual coordinate)
        # for each ray:
        #   find closest intersection with one of the objects
        #   calc distance to object
        #   from intersection start 3 new rays:
        #       for each light source:
        #           shadow ray with some power
        #       reflection ray with some power, if object have reflection property
        #       transparence ray with some power, if object have transparency property
        #   Color of pixel = color(diffuse + specular)
        #

        # TODO: make something except one shadow ray
        intersection = self.find_intersection(start_ray)
        if intersection is None:
            return AMBIENT
        else:
            # print(intersection)
            return intersection[-1]


    # maybe not face but normal vector
    def reflection_ray(self, start_ray, normal):
        # calc new direction, calc power
        new_ray = Ray()

    def transparency_ray(self, start_ray, normal):
        # calc new direction
        # cos (new angle) = sqrt(1 - (n1*n1/(n2*n2)*(1 - dot(N, I) * dot(N,I)) )
        # T = n1/n2*I - (cos (new angle) + n1/n2*dot(N, I)) * N
        #   where
        #       I - start ray, N - normal vector, n1, n2 - refraction coefficients
        #       T - resulting Ray
        #
        ray = Ray()

    def shadow_ray(self, start_ray, face, light_source):
        # just to light source, if face direction is appropriate
        pass

    @staticmethod
    def get_scene():
        return SpaceModel(scene_figures, scene_lights, scene_camera)