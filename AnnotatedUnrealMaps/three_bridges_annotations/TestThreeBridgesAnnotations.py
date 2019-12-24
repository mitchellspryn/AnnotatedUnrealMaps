import airsim
import airsim.airsim_types as at
import annotations_common.map_annotation
import math
import time
import numpy as np
import pandas as pd
import random
import time

import matplotlib.pyplot as plt

def main():
    client = airsim.UrdfBotClient()

    random.seed(42)

    annotations = annotations_common.map_annotation.MapAnnotation(client, 'F:/RMSpringAnnotations.json')

    maze_grid = annotations.MazeAnnotations.grid
    
    fig = plt.figure(figsize=(10,10))
    plt.imshow(maze_grid, cmap='cool')
    plt.savefig('F://mazegrid.png')


if __name__ == '__main__':
    main()