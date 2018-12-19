import numpy as np

EPS = 1e-10


class PlaneEq:
    def __init__(self, p1, p2, p3):
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0


class Polygon:
    def __init__(self, points=None):
        self.points = [] if points is None else points
        self.eq = PlaneEq(points[0], points[1], points[2])

    def transform(self, matrix):
        tensors = [np.array([x, y, z, 1]) for x,y,z in self.points]
        self.points = [np.dot(tensor, matrix)[:3] for tensor in tensors]

    def polygon_intersection(self, ray):
        A = self.eq.A
        B = self.eq.B
        C = self.eq.C
        D = self.eq.D
        p0 = ray.start_point
        v = ray.direction
        denominator = A * v[0] + B * v[1] + C * v[2]
        if abs(denominator) < EPS:
            return None

        t = - (A * p0[0] + B * p0[1] + C * p0[2] + D) / denominator
        p = p0 + t * v
        # check if point in polygon or not
        return p


class Figure:
    def __init__(self, polygons, center=np.array([0, 0, 0])):
        self.polygons = polygons
        self.center = center

    def transform(self, matrix):
        x, y, z = self.center
        self.center = np.dot(np.array([x, y, z, 1]), matrix)
        for plane in self.polygons:
            plane.transform(matrix)

    def move(self, dx, dy, dz):
        self.transform(
            np.array([
                [1,  0,  0,  0],
                [0,  1,  0,  0],
                [0,  0,  1,  0],
                [dx, dy, dz, 0]
            ])
        )

    def get_intersection(self, ray):
        # return closest point, distance to it and normal vector
        # find intersection with each polygon, if it exists
        # get the closest point from list
        # function of normal finding is needed
        return np.array([0, 0, 0])


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