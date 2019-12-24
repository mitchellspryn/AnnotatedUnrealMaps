import math
import numpy as np

class MazeOccupancyMatrix():
    def __init__(self, min_x, max_x, min_y, max_y, min_z, max_z, wall_width, blocking_volumes, default_grid_density = 50):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_z = min_z
        self.max_z = max_z
        self.wall_width = wall_width
        self.blocking_volumes = blocking_volumes
        
        self.width = self.max_x - self.min_x
        self.height = self.max_y - self.min_y
        self.grid_density = default_grid_density

        self.reinterpolate(self.grid_density)

    def reinterpolate_if_new(new_grid_density):
        if (self.grid_density == new_grid_density):
            return

        self.rebuild(new_grid_density)

    def reinterpolate(self, new_grid_density):
        self.grid_density = new_grid_density
        self.grid_height = int(math.ceil(self.height / new_grid_density))
        self.grid_width = int(math.ceil(self.width / new_grid_density))
        self.grid = np.zeros((self.grid_height, self.grid_width), np.uint8)

        for blocking_volume in self.blocking_volumes:
            max_y_coords, max_x_coords = self.__unreal_units_to_grid(
                blocking_volume['MaxY'], blocking_volume['MaxX'])

            min_y_coords, min_x_coords = self.__unreal_units_to_grid(
                blocking_volume['MinY'], blocking_volume['MinX'])

            self.grid[min_y_coords:max_y_coords+1, min_x_coords:max_x_coords+1] = 1

    def __unreal_units_to_grid(self, y, x):
        y_transformed = y - self.min_y
        x_transformed = x - self.min_x

        y_out = y_transformed / self.grid_density
        x_out = x_transformed / self.grid_density
        
        return (int(y_out), int(x_out))



