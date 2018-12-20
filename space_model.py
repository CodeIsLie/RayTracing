from ray import *
from scene import *
import numpy as np

LEFT_BOUND = 0
RIGHT_BOUND = 10

BOT_BOUND = 0
TOP_BOUND = 10
HALF_DIST = (LEFT_BOUND + RIGHT_BOUND) / 2

AMBIENT = 230, 230, 230

AIR_TRANSPARENCY = 1

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
        #   from intersection start 3 new rays:
        #       for each light source:
        #           shadow ray with some power
        #       reflection ray with some power, if object have reflection property
        #       transparence ray with some power, if object have transparency property
        #   Color of pixel = color(diffuse + specular)
        #


        # find closest intersection with one of the objects
        intersection = self.find_intersection(start_ray)
        if intersection is None:
            return AMBIENT
        else:
            obj = intersection[-1]
            shadow_rays = []
            for light in self.lights:
                shadow_rays.append(self.shadow_ray(start_ray, intersection, light))

            if obj.reflection > 0:
                self.reflection_ray(start_ray, intersection)
            if obj.transparency > 0:
                self.transparency_ray(start_ray, intersection)
            # print(intersection)
            return intersection[-1].color


    # maybe not face but normal vector
    def reflection_ray(self, start_ray, intersection):
        # calc new direction, calc power
        normal = intersection[2]
        start_dir = start_ray.direction
        direction = start_dir - 2*normal*np.dot(normal, start_dir)
        new_ray = Ray(intersection[0], direction)
        return new_ray

    def transparency_ray(self, start_ray, intersection):
        # calc new direction
        # cos (new angle) = sqrt(1 - (n1*n1/(n2*n2)*(1 - dot(N, I) * dot(N,I)) )
        # T = n1/n2*I - (cos (new angle) + n1/n2*dot(N, I)) * N
        #   where
        #       I - start ray, N - normal vector, n1, n2 - refraction coefficients
        #       T - resulting Ray
        #
        ray = Ray()

    def shadow_ray(self, start_ray, intersection, light):
        """
        create a ray from intersection point to light source, if it possible

        """
        goal = light.source
        normal = intersection[2]
        direction = goal - intersection[0]
        if np.dot(direction, normal) < 0:
            return None
        # start_ray.add_child()
        return Ray(intersection[0], direction)

    @staticmethod
    def get_scene():
        return SpaceModel(scene_figures, scene_lights, scene_camera)