from ray import *
import numpy as np


class SpaceModel:
    def __init__(self, figures, lights, camera):
        self.figures = figures
        self.lights = lights
        self.camera = camera

    def ray_tracing(self, width, height):
        # for each pixel:
        #   start ray from camera center to pixel (virtual coordinate)
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


        pass

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