
class Ray:
    def __init__(self, start, direction):

        self.start_point = start
        self.direction = direction
        self.power = 1
        self.color = None
        self.children = []

    def add_child(self, child_ray):
        self.children.append(child_ray)

    def add_children(self, children_rays):
        self.children += children_rays