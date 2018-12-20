from ray import *
from scene import *
import numpy as np

LEFT_BOUND = 0
RIGHT_BOUND = 10

BOT_BOUND = 0
TOP_BOUND = 10
HALF_DIST = (LEFT_BOUND + RIGHT_BOUND) / 2

AMBIENT_COLOR = 10, 10, 10
AMBIENT_K = 0.15

INTENSITY_THRESHOLD = 0.001

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
                if i == 64 and j == 64:
                    k = 2
                    pass
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
        # find closest intersection with one of the objects
        intersection = self.find_intersection(start_ray)
        self.run_ray(start_ray)

        # if start_ray.power < INTENSITY_THRESHOLD:
        #     return AMBIENT_COLOR
        color_k = max(start_ray.power, AMBIENT_K)
        # print(intersection)
        return tuple(np.around([comp * color_k for comp in intersection[-1].color]).astype(int))

    def run_ray(self, ray):
        if ray.power < INTENSITY_THRESHOLD:
            return

        intersection = self.find_intersection(ray)
        if intersection is None:
            if ray.distance_to_light is None:
                ray.power = 0.0
        else:
            # case of shadow ray
            if ray.distance_to_light is not None:
                if ray.distance_to_light >= intersection[1]:
                    ray.power = 0.0
                return
            obj = intersection[-1]
            shadow_rays = []
            for light in self.lights:
                shadow_rays.append(self.shadow_ray(ray, intersection, light))

            if obj.reflection > 0:
                self.reflection_ray(ray, intersection)
            if obj.transparency > 0:
                self.transparency_ray(ray, intersection)
            for r in ray.children:
                self.run_ray(r)
            ray.calc_power()

    # maybe not face but normal vector
    def reflection_ray(self, start_ray, intersection):
        # calc new direction, calc power
        normal = intersection[2]
        start_dir = start_ray.direction
        direction = start_dir - 2*normal*np.dot(normal, start_dir)
        new_ray = Ray(intersection[0], direction, start_ray.power)
        return new_ray

    def transparency_ray(self, start_ray, intersection):
        # calc new direction
        # cos (new angle) = sqrt(1 - (n1*n1/(n2*n2)*(1 - dot(N, I) * dot(N,I)) )
        # T = n1/n2*I - (cos (new angle) + n1/n2*dot(N, I)) * N
        #   where
        #       I - start ray, N - normal vector, n1, n2 - refraction coefficients
        #       T - resulting Ray
        #
        # TODO: calc direction by formula above
        direction = None
        ray = Ray(intersection[0], direction, start_ray.power)
        return ray

    def shadow_ray(self, start_ray, intersection, light):
        """
        create a ray from intersection point to light source, if it possible

        """
        goal = light.source
        normal = intersection[2]
        start = intersection[0] # + normal * 0.0001
        direction = goal - start
        if np.dot(direction, normal) < 0:
            return None
        ray = Ray(start, direction, start_ray.power * light.intensity, np.linalg.norm(direction))
        start_ray.add_child(ray)
        return ray

    @staticmethod
    def get_scene():
        return SpaceModel(scene_figures, scene_lights, scene_camera)