import math

import annotations_common.directed_path_point as directed_path_point

class DirectedPath():
    def __init__(self, name, points):
        self.points = points
        self.name = name

        self.manual_points = [p for p in points if p.is_manual]

    def reinterpolate(interpolation_step_size):
        self.points = []
        for i in range(0, len(self.manual_points) - 1, 1):
            first_point = self.points[i]
            second_point = self.points[i+1]

            self.points.append(first_point)
            second_first_vec = second_point - first_point
            length = __l2(second_first_vec)

            second_first_vec.x /= length
            second_first_vec.y /= length
            second_first_vec.z /= length

            num_steps = int(math.floor(length / interpolation_step_size))

            for j in range(1, num_steps + 1, 1):
                mult_vec = second_first_vec * (float(j) * interpolation_step_size)
                new_point = directed_path_point.DirectedPathPoint(
                    first_point.x + mult_vec.x,
                    first_point.y + mult_vec.y,
                    first_point.z + mult_vec.z,
                    None,
                    False)
                self.points.append(new_point)

        self.points.append(self.manual_points[len(self.manual_points)-1])

    def __l2(self, vec):
        return ( (vec.x*vec.x) + (vec.y*vec.y) + (vec.z*vec.z) ) ** 0.5

