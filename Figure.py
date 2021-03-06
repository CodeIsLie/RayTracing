import numpy as np

EPS = 1e-10


def cross_product(a, b):
    x = a[1] * b[2] - a[2] * b[1]
    y = a[2] * b[0] - a[0] * b[2]
    z = a[0] * b[1] - a[1] * b[0]
    return np.array([x, y, z])


class PlaneEq:
    def __init__(self, p1, p2, p3, center):
        v1 = p2 - p1
        v2 = p2 - p3

        vec_cent = center - p2
        ort_vec = cross_product(v1, v2)

        dir_vec = np.dot(vec_cent, ort_vec)
        sign_dir = 1 if dir_vec < 0 else -1
        normal = ort_vec * sign_dir

        self.A, self.B, self.C = normal
        self.D = -np.dot(normal, p1)

    def __str__(self):
        return "A {} B {} C {} D {}".format(self.A, self.B, self.C, self.D)


class LineEq:
    def __init__(self, p1, p2):
        self.A = p2[1] - p1[1]
        self.B = p1[0] - p2[0]
        self.C = -(self.A * p1[0] + self.B * p1[1])

    def side(self, point):
        return point[0] * self.A + point[1] * self.B + self.C > 0

    def __str__(self):
        return "A {} B {} C {} ".format(self.A, self.B, self.C)


class Polygon:
    def __init__(self, points=None, figure_center=np.array([0,0,0]), color=(255,0,0),
                 transparency=0, reflection=0, refraction=1):
        """

        :param points: точки полигона
        :param figure_center: центер фигуры (по факту только куба), которйо принадлежит этот полигон
        :param color:
        :param transparency: прозрачность объекта,
            какую часть в итоговом цвете будет составлять преломлённый луч,от 0 до 1
        :param reflection: зеркальность объекта, аналогично прозрачности от 0 до 1
        :param refraction: коэфиициент преломления, 1 - угол при преломлении не меняется,
            чем ближе к 0, тем больше меняется угол
        """
        self.points = [] if points is None else points
        self.figure_center = figure_center
        self.color = color
        self.transparency = transparency
        self.reflection = reflection
        self.refraction=refraction
        # нормаль
        self.normal = None
        self.eq = None
        self.calc_norm()

    def calc_norm(self):
        self.eq = PlaneEq(self.points[0], self.points[1], self.points[2], self.figure_center)
        normal = np.array([self.eq.A, self.eq.B, self.eq.C])
        dir_to_center = self.figure_center - self.points[0]
        sign = np.sign(np.dot(normal, dir_to_center))
        normal *= -sign/np.linalg.norm(normal)
        self.normal = normal

    def transform(self, matrix):
        tensors = [np.array([x, y, z, 1]) for x, y, z in self.points]
        self.points = [np.dot(tensor, matrix)[:3] for tensor in tensors]
        x, y, z = self.figure_center
        self.figure_center = np.dot(np.array([x, y, z, 1.0]), matrix)[:3]
        self.calc_norm()

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
        t -= EPS
        p = p0 + t * v
        normal = self.normal
        # check if point in polygon or not
        return (p, np.linalg.norm(t*v), normal, self) if t > -EPS else None

    def __str__(self):
        return ",".join([str(p) for p in self.points]) + " norm {}".format(self.normal)


class Cube:
    """
    figure assembled from polygons
    have center
    """
    def __init__(self, polygons, color, center=np.array([0, 0, 0]), transparency=0, reflection=0, refraction=1):
        self.polygons = [Polygon(p.points, center, p.color, transparency, reflection) for p in polygons]
        self.color = color
        self.center = center
        self.reflection = reflection
        self.transparency = transparency
        self.refraction=refraction
        self.calc_bounds()

    def set_color(self, color):
        self.color = color
        for p in self.polygons:
            p.color = color

    def set_refraction(self, refraction):
        self.refraction = refraction
        for p in self.polygons:
            p.refraction = refraction

    def set_reflection(self, reflection):
        self.reflection = reflection
        for p in self.polygons:
            p.reflection = reflection

    def set_transparency(self, transparency):
        self.transparency = transparency
        for p in self.polygons:
            p.transparency = transparency

    def calc_bounds(self):
        xs = [x for polygon in self.polygons for x, _, _ in polygon.points]
        ys = [y for polygon in self.polygons for _, y, _ in polygon.points]
        zs = [z for polygon in self.polygons for _, _, z in polygon.points]
        self.x_left = min(xs)
        self.x_right = max(xs)
        self.y_left = min(ys)
        self.y_right = max(ys)
        self.z_left = min(zs)
        self.z_right = max(zs)

    def transform(self, matrix):
        x, y, z = self.center[:3]
        self.center = np.dot(np.array([x, y, z, 1]), matrix)
        for plane in self.polygons:
            plane.transform(matrix)
        self.calc_bounds()

    def move(self, dx, dy, dz):
        self.transform(
            np.array([
                [1,  0,  0,  0],
                [0,  1,  0,  0],
                [0,  0,  1,  0],
                [dx, dy, dz, 0]
            ])
        )

    def scale(self, mx, my, mz):
        self.transform(
            np.array([
                [mx, 0,  0,  0],
                [0,  my, 0,  0],
                [0,  0,  mz, 0],
                [0,  0,  0,  0]
            ])
        )

    def point_inside(self, point):
        x, y, z = point
        return self.x_left-2*EPS < x < self.x_right + 2*EPS\
            and self.y_left-2*EPS < y < self.y_right + 2*EPS\
            and self.z_left - 2*EPS < z < self.z_right + 2*EPS

    def get_intersection(self, ray):
        """
        return closest point, distance to it, normal vector and color
        find intersection with each polygon, if it exists, None instead

        intersection = tuple(point(np.array), distance from ray start to intersection(double),
                norm vector(np.array), object of intersection - sphere or polygon)
        """
        min_distance = 1e+20
        closest_intersection = None
        for polygon in self.polygons:
            intersection = polygon.polygon_intersection(ray)
            if intersection is None:
                continue

            point, dist, _, o = intersection
            if dist < min_distance and self.point_inside(point):
                min_distance = dist
                closest_intersection = intersection

        return closest_intersection

    def __str__(self):
        return "\n".join([str(p) for p in self.polygons]) + "\ncenter " + str(self.center)


class Sphere:
    def __init__(self, center, radius, color=(200, 10, 10), transparency=0, reflection=0, refraction=1):
        """
        :param center:
        :param radius:
        :param color:
        :param transparency: прозрачность объекта,
            какую часть в итоговом цвете будет составлять преломлённый луч,от 0 до 1
        :param reflection: зеркальность объекта, аналогично прозрачности от 0 до 1
        :param refraction: коэфиициент преломления, 1 - угол при преломлении не меняется,
            чем ближе к 0, тем больше меняется угол
        """
        self.center = center
        self.radius = radius
        self.color = color
        self.transparency = transparency
        self.reflection = reflection
        self.refraction = refraction


    def get_intersection(self, ray):
        """
        :param ray:
        :return: intersection = tuple(point(np.array), distance from ray start to intersection(double),
                norm vector(np.array), object of intersection - sphere or polygon)
        """
        # return closest point, distance to it and normal vector, and object
        diff = ray.start_point - self.center
        dir = ray.direction / np.linalg.norm(ray.direction)
        rad = self.radius
        discriminant = np.dot(diff, dir) ** 2 - (np.linalg.norm(diff)**2 - rad*rad)
        if discriminant < 0:
            return None
        # нет пересечений со сферой
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

        # print(t)
        t -= 2*EPS
        inters_point = ray.start_point + t * dir
        distance = np.linalg.norm(t * dir)
        normal = inters_point - self.center

        return inters_point, distance, normal, self

    def __str__(self):
        return str(self.center) + " " + str(self.radius)