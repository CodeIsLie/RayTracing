
class Ray:
    def __init__(self, start, direction, power=1.0, distance_to_light=None, color=None):
        self.start_point = start
        self.direction = direction
        self.power = power
        self.color = color
        self.distance_to_light = distance_to_light
        self.children = []

    def add_child(self, child_ray):
        self.children.append(child_ray)

    def add_children(self, children_rays):
        self.children += children_rays

    def calc_power(self):
        r = sum([c.color[0] for c in self.children if c.power > 0])
        g = sum([c.color[1] for c in self.children if c.power > 0])
        b = sum([c.color[2] for c in self.children if c.power > 0])
        self.color = r, g, b
        self.power = sum([c.power for c in self.children])