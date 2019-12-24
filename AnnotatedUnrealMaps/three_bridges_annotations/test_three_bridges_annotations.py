import airsim
import airsim.airsim_types as at
import annotations_common.map_annotation
import math
import time
import numpy as np
import pandas as pd
import random
import time
import os

import matplotlib.pyplot as plt

def add_annotated_path(path, existing_shapes_request, client):
    height_offset = 0.1
    for i in range(0, len(path.manual_points), 1):
        world_point = path.manual_points[i]

        color_r = 0
        if (world_point.is_manual):
            color_g = 255
            color_b = 0
        else:
            color_g = 0
            color_b = 255


        existing_shapes_request = client.addDrawableShapeSphere(existing_shapes_request, 
                                                                  '{0}_{1}'.format(path.name, i),
                                                                  '',
                                                                  world_point.x,
                                                                  world_point.y,
                                                                  world_point.z + height_offset,
                                                                  1, 
                                                                  32,
                                                                  32,
                                                                  color_r,
                                                                  color_g,
                                                                  color_b,
                                                                  0)
        
        if (i < len(path.manual_points) - 1):
            next_point = path.manual_points[i+1]
            
            existing_shapes_request = client.addDrawableShapeLine(existing_shapes_request,
                                                                    '{0}_{1}_line'.format(path.name, i),
                                                                    '',
                                                                    world_point.x,
                                                                    world_point.y,
                                                                    world_point.z + height_offset,
                                                                    next_point.x,
                                                                    next_point.y,
                                                                    next_point.z + height_offset,
                                                                    30,
                                                                    0,
                                                                    0,
                                                                    255,
                                                                    0)

    return existing_shapes_request

def add_annotated_poi(poi, existing_shapes_request, client):
    color_r = 255
    color_g = 0
    color_b = 255

    existing_shapes_request = client.addDrawableShapeBox(existing_shapes_request, 
                                                         poi.name,
                                                         '',
                                                         poi.x,
                                                         poi.y,
                                                         poi.z,
                                                         1,
                                                         1,
                                                         1,
                                                         40,
                                                         color_r,
                                                         color_g,
                                                         color_b,
                                                         0)

    return existing_shapes_request;

def add_annotated_polygon(poly, existing_shapes_request, client):
    height_offset = 0.1
    for i in range(0, len(poly.manual_points), 1):
        world_point = poly.manual_points[i]

        if (world_point.is_manual):
            color_r = 255
            color_g = 0
        else:
            color_r = 0
            color_g = 255
        color_b = 0

        existing_shapes_request = client.addDrawableShapeSphere(existing_shapes_request, 
                                                                  '{0}_{1}'.format(poly.name, i),
                                                                  '',
                                                                  world_point.x,
                                                                  world_point.y,
                                                                  world_point.z + height_offset,
                                                                  1, 
                                                                  32,
                                                                  32,
                                                                  color_r,
                                                                  color_g,
                                                                  color_b,
                                                                  0)
        
        next_point = poly.manual_points[(i+1) % len(poly.manual_points)]
        
        existing_shapes_request = client.addDrawableShapeLine(existing_shapes_request,
                                                                '{0}_{1}_line'.format(poly.name, i),
                                                                '',
                                                                world_point.x,
                                                                world_point.y,
                                                                world_point.z + height_offset,
                                                                next_point.x,
                                                                next_point.y,
                                                                next_point.z + height_offset,
                                                                30,
                                                                0,
                                                                255,
                                                                0,
                                                                0)

    return existing_shapes_request

def add_maze_bounds(maze_annotation, existing_shapes_request, client):
    color_r = 255
    color_g = 255
    color_b = 0

    x_width = (maze_annotation.max_x - maze_annotation.min_x)
    y_width = (maze_annotation.max_y - maze_annotation.min_y)
    z_width = (maze_annotation.max_z - maze_annotation.min_z)

    x_center = maze_annotation.min_x + (x_width / 2)
    y_center = maze_annotation.min_y + (y_width / 2)
    z_center = maze_annotation.min_z + (z_width / 2)

    existing_shapes_request = client.addDrawableShapeBox(existing_shapes_request, 
                                                         'maze_outline',
                                                         '',
                                                         x_center,
                                                         y_center,
                                                         z_center,
                                                         x_width/2,
                                                         y_width/2,
                                                         z_width/2,
                                                         40,
                                                         color_r,
                                                         color_g,
                                                         color_b,
                                                         0)

    return existing_shapes_request;


def main():
    client = airsim.UrdfBotClient()

    random.seed(42)

    print('Reading annotations...')
    annotations = annotations_common.map_annotation.MapAnnotation(client, 'three_bridges_annotations/three_bridges_annotations.json')

    drawable_shape_request = at.DrawableShapeRequest(shapes={}, persist_unmentioned=True)

    print('Drawing directed paths...')
    for key in annotations.annotations[annotations.DIRECTED_PATH_ANNOTATION_TYPE]:
        drawable_shape_request = add_annotated_path(annotations.annotations[annotations.DIRECTED_PATH_ANNOTATION_TYPE][key], drawable_shape_request, client)

    print('Drawing points of interest...')
    for key in annotations.annotations[annotations.POI_ANNOTATION_TYPE]:
        drawable_shape_request = add_annotated_poi(annotations.annotations[annotations.POI_ANNOTATION_TYPE][key], drawable_shape_request, client)

    print('Drawing polygons...')
    for key in annotations.annotations[annotations.POLYGON_ANNOTATION_TYPE]:
        drawable_shape_request = add_annotated_polygon(annotations.annotations[annotations.POLYGON_ANNOTATION_TYPE][key], drawable_shape_request, client)

    print('Drawing maze bounds...')
    for key in annotations.annotations[annotations.MAZE_ANNOTATION_TYPE]:
        drawable_shape_request = add_maze_bounds(annotations.annotations[annotations.MAZE_ANNOTATION_TYPE][key], drawable_shape_request, client)

    print('Sending draw request...')
    client.simSetDrawableShapes(drawable_shape_request)

    print('Creating maze grid image...')
    maze_grid = annotations.annotations[annotations.MAZE_ANNOTATION_TYPE]['MazeAnnotations'].grid
    
    fig = plt.figure(figsize=(10,10))
    plt.title('Visual representation of maze occupancy matrix.')
    plt.imshow(maze_grid, cmap='cool')
    plt.show()

    print('Done!')

if __name__ == '__main__':
    main()