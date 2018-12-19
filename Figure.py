import numpy as np

EPS = 1e-10

class Figure:
    def __init__(self):
        self.polygons = []

    def get_intersection(self, ray):
        # return closest point, distance to it and normal vector
        return 1,1


class Sphere:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def get_intersection(self, ray):
        # return closest point, distance to it and normal vector
        diff = ray.start_point - self.center
        dir = ray.direction / np.linalg.norm(ray.direction)
        rad = self.radius
        discriminant = np.dot(diff, dir) ** 2 - (np.linalg.norm(diff)**2 - rad*rad)
        if abs(discriminant) < EPS:
            t = -np.dot(dir, diff)
        else:
            # find closest t in ray parametric equation
            a = -np.dot(diff, dir)
            t0 = a + np.sqrt(discriminant)
            t1 = a - np.sqrt(discriminant)
            if t1 < 0:
                if t0 > 0:
                    t = t0
                else:
                    return None
            else:
                t = t1

        print(t)
        inters_point = ray.start_point + t * dir
        distance = np.linalg.norm(t * dir)
        normal = inters_point - self.center

        return inters_point, distance, normal

    def __str__(self):
        return str(self.center) + " " + str(self.radius)