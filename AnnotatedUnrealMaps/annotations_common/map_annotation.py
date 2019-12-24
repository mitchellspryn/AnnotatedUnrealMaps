import airsim
import json

import annotations_common.annotated_poi as annotated_poi
import annotations_common.annotated_polygon_point as annotated_polygon_point
import annotations_common.directed_path_point as directed_path_point
import annotations_common.annotated_polygon as annotated_polygon
import annotations_common.directed_path as directed_path
import annotations_common.maze_occupancy_matrix as maze_occupancy_matrix

class MapAnnotation(object):
    def __init__(self, client, file_path, scale_factor = 100):

        self.DIRECTED_PATH_ANNOTATION_TYPE = 'DirectedPath'
        self.POLYGON_ANNOTATION_TYPE = 'AnnotatedPolygon'
        self.POI_ANNOTATION_TYPE = 'AnnotatedPoi'
        self.MAZE_ANNOTATION_TYPE = 'MazeAnnotation'
        
        self.scale_factor = scale_factor

        self.annotations = {}
        self.annotations[self.DIRECTED_PATH_ANNOTATION_TYPE] = {}
        self.annotations[self.POLYGON_ANNOTATION_TYPE] = {}
        self.annotations[self.POI_ANNOTATION_TYPE] = {}
        self.annotations[self.MAZE_ANNOTATION_TYPE] = {}

        with open(file_path, 'r') as f:
            raw_string_data = f.read()
        json_data = json.loads(raw_string_data)

        for key in json_data:
            annotation_type = json_data[key]['Type']
            if (annotation_type == self.POI_ANNOTATION_TYPE):
                self.annotations[self.POI_ANNOTATION_TYPE][key] = self.__parse_annotated_poi(json_data, key, client)
            elif (annotation_type == self.DIRECTED_PATH_ANNOTATION_TYPE):
                self.annotations[self.DIRECTED_PATH_ANNOTATION_TYPE][key] = self.__parse_directed_path(json_data, key, client)
            elif (annotation_type == self.MAZE_ANNOTATION_TYPE):
                self.annotations[self.MAZE_ANNOTATION_TYPE][key] = self.__parse_maze_occupancy_matrix(json_data, key)
            elif (annotation_type == self.POLYGON_ANNOTATION_TYPE):
                self.annotations[self.POLYGON_ANNOTATION_TYPE][key] = self.__parse_annotated_polygon(json_data, key, client)
            else:
                raise ValueError('Invalid annotation type: {0}'.format(annotation_type))

    def __parse_annotated_poi(self, json_data, field_name, client):
        poi = annotated_poi.AnnotatedPoi(field_name, 
                                               float(json_data[field_name]['X']) / self.scale_factor,
                                               float(json_data[field_name]['Y']) / self.scale_factor,
                                               float(json_data[field_name]['Z']) / self.scale_factor)

        poi.set_geo(client.simXyzToGeoPoints([poi.location_xyz()])[0])


        return poi

    def __parse_directed_path(self, json_data, field_name, client):
        points = []
        for point in json_data[field_name]['Coordinates']:
            point = directed_path_point.DirectedPathPoint(
                float(point['X']) / self.scale_factor,
                float(point['Y']) / self.scale_factor,
                float(point['Z']) / self.scale_factor,
                point['Index'],
                point['IsManual'])

            points.append(point)

        points_geo = client.simXyzToGeoPoints([p.location_xyz() for p in points])
        for i in range(0, len(points_geo), 1):
            points[i].set_geo(points_geo[i])

        path = directed_path.DirectedPath(
            field_name, points)

        return path

    def __parse_annotated_polygon(self, json_data, field_name, client):
        points = []
        for point in json_data[field_name]['Coordinates']:
            point = annotated_polygon_point.AnnotatedPolygonPoint(
                float(point['X']) / self.scale_factor,
                float(point['Y']) / self.scale_factor,
                float(point['Z']) / self.scale_factor,
                point['IsManual'])

            points.append(point)

        points_geo = client.simXyzToGeoPoints([p.location_xyz() for p in points])
        for i in range(0, len(points_geo), 1):
            points[i].set_geo(points_geo[i])

        poly = annotated_polygon.AnnotatedPolygon(
            field_name, points)

        return poly


    def __parse_maze_occupancy_matrix(self, json_data, field_name):
        blocking_volumes = []
        for blocking_volume in json_data[field_name]['BlockingVolumes']:
            converted_volume = {}

            converted_volume['MaxX'] = blocking_volume['MaxX'] / self.scale_factor
            converted_volume['MaxY'] = blocking_volume['MaxY'] / self.scale_factor
            converted_volume['MaxZ'] = blocking_volume['MaxZ'] / self.scale_factor
            converted_volume['MinX'] = blocking_volume['MinX'] / self.scale_factor
            converted_volume['MinY'] = blocking_volume['MinY'] / self.scale_factor
            converted_volume['MinZ'] = blocking_volume['MinZ'] / self.scale_factor

            blocking_volumes.append(converted_volume)

        maze = maze_occupancy_matrix.MazeOccupancyMatrix(
            float(json_data[field_name]['MinX']) / self.scale_factor,
            float(json_data[field_name]['MaxX']) / self.scale_factor,
            float(json_data[field_name]['MinY']) / self.scale_factor,
            float(json_data[field_name]['MaxY']) / self.scale_factor,
            float(json_data[field_name]['MinZ']) / self.scale_factor,
            float(json_data[field_name]['MaxZ']) / self.scale_factor,
            float(json_data[field_name]['WallWidth']) / self.scale_factor,
            blocking_volumes, 
            0.5)

        return maze
