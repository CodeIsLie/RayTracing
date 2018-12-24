from ray import *
from scene import *
import numpy as np

LEFT_BOUND = 0
RIGHT_BOUND = 10
BOT_BOUND = 0
TOP_BOUND = 10

HALF_DIST = (LEFT_BOUND + RIGHT_BOUND) / 2

AMBIENT_COLOR = 10, 10, 10
AMBIENT_K = 0.16
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

                point = np.array([9.99, y, z])
                ray = point - self.camera
                ray = Ray(point, ray / np.linalg.norm(ray))

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

        distance_lightning = 0
        point = intersection[0]

        for l in scene_lights:
            distance = np.linalg.norm(point - l.source)
            distance_lightning += 2/(1+distance)
        light_minimum = max(AMBIENT_K, distance_lightning)

        # фоновое освещение
        ambient_lightning = np.array([comp * light_minimum for comp in intersection[-1].color])
        # прямое освещение
        diffuse_lightning = np.array(start_ray.color)

        combine_lightning = np.array([min(255, color) for color in (ambient_lightning + diffuse_lightning)])
        # делаем преобразование из float в int, так как цвет должен быть целым
        return tuple(combine_lightning.astype(int))

    def run_ray(self, ray):
        if ray.power < INTENSITY_THRESHOLD:
            return

        intersection = self.find_intersection(ray)
        if intersection is None:
            # если это не теневой луч, то он не будет учитывается
            if ray.distance_to_light is None:
                ray.power = 0.0
        else:
            # case of shadow ray
            if ray.distance_to_light is not None:
                if ray.distance_to_light >= intersection[1]:
                    ray.power = 0.0
                return

            # sphere or polygon
            figure = intersection[-1]
            if ray.rayType == TranceRayType.IN:
                intersection = self.move_intersection_point(ray, intersection)
            for light in self.lights:
                self.shadow_ray(ray, intersection, light)

            if figure.reflection > 0:
                self.reflection_ray(ray, intersection)
            if figure.transparency > 0:
                if ray.rayType == TranceRayType.OUT:
                    intersection = self.move_intersection_point(ray, intersection)
                self.transparency_ray(ray, intersection)
            for r in ray.children:
                self.run_ray(r)
            ray.calc_power()

    # return new intersection with replaced point
    def move_intersection_point(self, ray, intersection):
        original = intersection[0]
        dir = ray.direction
        new_start = original + 15*EPS*dir
        return new_start, intersection[1], intersection[2], intersection[-1]

    def reflection_ray(self, start_ray, intersection):
        # calc new direction, calc power
        normal = intersection[2]
        start_dir = start_ray.direction
        direction = start_dir - 2*normal*np.dot(normal, start_dir)
        new_ray = Ray(intersection[0], direction, start_ray.power * intersection[-1].reflection)
        start_ray.add_child(new_ray)

    def calc_refraction_ray(self, start_ray, intersection):
        normal = intersection[2] if start_ray.rayType == TranceRayType.OUT else (-1) * intersection[2]
        start_dir = start_ray.direction
        obj_transparency = intersection[-1].transparency
        obj_refraction = intersection[-1].refraction
        k = obj_refraction / AIR_TRANSPARENCY if start_ray.rayType == TranceRayType.IN \
            else AIR_TRANSPARENCY / obj_refraction
        scalar_p = np.dot(normal, start_dir)
        cos = np.sqrt(max(0, 1 - k * k * (1 - scalar_p ** 2)))
        direction = k * start_dir - (cos + k * scalar_p) * normal

        # move through object by some value
        start = intersection[0]
        ray_type = TranceRayType.OUT if start_ray.rayType == TranceRayType.IN else TranceRayType.IN
        return Ray(start, direction, start_ray.power * obj_transparency, rayType=ray_type)

    def transparency_ray(self, start_ray, intersection):
        ray = self.calc_refraction_ray(start_ray, intersection)
        start_ray.add_child(ray)

    def refraction_shadow_ray(self, start_ray, intersection, light):
        goal = light.source
        normal = intersection[2]
        start = intersection[0]
        direction = goal - start
        if np.dot(direction, normal) < 0:
            return None
        forward_ray_k = 1 - intersection[-1].transparency - intersection[-1].reflection
        power = start_ray.power * forward_ray_k * light.intensity
        color = tuple([c * power for c in intersection[-1].color])
        ray = Ray(start, direction, power, np.linalg.norm(direction), color)

        ray_intersection = self.find_intersection(ray)
        if ray_intersection[1] < ray.distance_to_light:
            if ray_intersection[-1].transparency > 0:

                self.refraction_shadow_ray(ray, ray_intersection)
                pass

    def shadow_ray(self, start_ray, intersection, light):
        """
        create a ray from intersection point to light source, if it possible

        """
        goal = light.source
        normal = intersection[2]
        start = intersection[0]
        direction = goal - start
        if np.dot(direction, normal) < 0:
            return None
        forward_ray_k = 1 - intersection[-1].transparency - intersection[-1].reflection
        power = start_ray.power * forward_ray_k * light.intensity
        color = tuple([c * power for c in intersection[-1].color])
        ray = Ray(start, direction, power, np.linalg.norm(direction), color, light=light)
        start_ray.add_child(ray)

    @staticmethod
    def get_scene():
        return SpaceModel(scene_figures, scene_lights, scene_camera)