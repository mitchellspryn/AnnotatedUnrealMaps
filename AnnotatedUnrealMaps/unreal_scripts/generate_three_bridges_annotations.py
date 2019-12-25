# Do not run this from visual studio or the command prompt!
# This can only be run from within the unreal editor. 
# 
# To run, first ensure that the following plugins are enabled:
#  Editor Scripting Utilities
#  Python Editor Script Plugin
#  Sequencer Scripting
# 
# Then, from the output log, run this script with the following command
#   <path_to_script> <interpolation_step_size> <output_file_path>
#
# If modifications need to be made, note that the UE python scripting editor only supports python 2.7, and very few external libraries
#  (e.g. Numpy does not import properly)
print "Running script GeneratePathPointsFromMeshes..."
import os
import sys
import json
import math
print "Running script with {0}".format(sys.version)

import unreal
print "unreal library imported"

DIRECTED_PATH_ANNOTATION_TYPE = 'DirectedPath'
POLYGON_ANNOTATION_TYPE = 'AnnotatedPolygon'
POI_ANNOTATION_TYPE = 'AnnotatedPoi'
MAZE_ANNOTATION_TYPE = 'MazeAnnotation'

def split_actor_name(actor_name):
    split = str(actor_name).split('_')
    
    if (len(split) != 3):
        error_message = 'Invalid actor name for split: {0}.\n'.format(actor_name)
        error_message += '\tExpected name of form "Type_PathName_Index", but found {0} segments after splitting on "_".'.format(len(split))
        raise ValueError(error_message)
    
    result = {}
    result['Type'] = split[0]
    result['PathName'] = split[1]
    result['Index'] = int(split[2])
    
    return result
    
def is_path_annotation(actor_name):
    name = str(actor_name)
    if name.startswith(DIRECTED_PATH_ANNOTATION_TYPE):
        return True
    if name.startswith(POLYGON_ANNOTATION_TYPE):
        return True
    if name.startswith(POI_ANNOTATION_TYPE):
        return True
    return False
    
def sort_paths_by_index(annotations_of_interest):
    for path_type in annotations_of_interest:
        for path_name in annotations_of_interest[path_type]:
            annotations_of_interest[path_type][path_name] = sorted(annotations_of_interest[path_type][path_name], key=lambda x: x['IdChunks']['Index'])
    
    return annotations_of_interest
    
def extract_path_meshes():
    all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
    
    annotations_of_interest = {}
    
    for actor in [a for a in all_actors if is_path_annotation(a.get_fname())]:
            
        actor_name_chunks = split_actor_name(actor.get_fname())
        actor_location = actor.get_actor_location()
        actor_rotation = actor.get_actor_rotation()
        
        if (actor_name_chunks['Type'] not in annotations_of_interest):
            annotations_of_interest[actor_name_chunks['Type']] = {}
        
        typed_annotation = annotations_of_interest[actor_name_chunks['Type']]
        if actor_name_chunks['PathName'] not in typed_annotation:
            typed_annotation[actor_name_chunks['PathName']] = []
            
        path = typed_annotation[actor_name_chunks['PathName']]
        
        waypoint = {}
        waypoint['IdChunks'] = actor_name_chunks
        waypoint['Location'] = actor_location
        waypoint['Rotation'] = actor_rotation
        
        path.append(waypoint)

    sort_paths_by_index(annotations_of_interest)
    return annotations_of_interest
    
def make_point(x, y, z, is_manual, index=None):
    point = {}
    
    point['X'] = x
    point['Y'] = y
    point['Z'] = z
    point['Index'] = index
    point['IsManual'] = is_manual
    
    return point
    
# Does not include the endpoints
def generate_lerp_path(point_a, point_b, interpolation_step_size):
    output_path = []
    a_b_vec = point_b - point_a
    vec_length = a_b_vec.length()
    a_b_vec = a_b_vec / vec_length
    num_steps = int(math.floor(vec_length / interpolation_step_size))
    
    for i in range(1, num_steps + 1, 1):
        tmp_point = point_a + (a_b_vec.multiply_float(float(i) * interpolation_step_size))
        output_path.append(make_point(tmp_point.x, tmp_point.y, tmp_point.z, False))
    
    return output_path
    
def generate_interpolated_path(path, interpolation_step_size, is_polygon):
    output_path = []
    
    for i in range(0, len(path) - 1, 1):
        this_point = path[i]['Location']
        next_point = path[i + 1]['Location']
        output_path.append(make_point(this_point.x, this_point.y, this_point.z, True, path[i]['IdChunks']['Index']))
        output_path += generate_lerp_path(this_point, next_point, interpolation_step_size)
    
    final_point = path[len(path) - 1]['Location']
    output_path.append(make_point(final_point.x, final_point.y, final_point.z, True))
    
    if (is_polygon):
        output_path += generate_lerp_path(final_point, path[0]['Location'], interpolation_step_size)
    
    return output_path
    
def generate_mesh_paths(interpolation_step_size):
    print('Getting annotated meshes...')
    annotations = extract_path_meshes()
    
    output = {}
    if DIRECTED_PATH_ANNOTATION_TYPE in annotations:
        print('Generating directed paths...')
        for path_name in annotations[DIRECTED_PATH_ANNOTATION_TYPE]:
            generated_path = {}
            generated_path['Type'] = DIRECTED_PATH_ANNOTATION_TYPE
            generated_path['Coordinates'] = generate_interpolated_path(annotations[DIRECTED_PATH_ANNOTATION_TYPE][path_name], interpolation_step_size, False)
            output[path_name] = generated_path
        
    if POLYGON_ANNOTATION_TYPE in annotations:
        print('Generating annotated polygons...')
        for poly_name in annotations[POLYGON_ANNOTATION_TYPE]:
            generated_polygon = {}
            generated_polygon['Type'] = POLYGON_ANNOTATION_TYPE
            generated_polygon['Coordinates'] = generate_interpolated_path(annotations[POLYGON_ANNOTATION_TYPE][poly_name], interpolation_step_size, True)
            output[poly_name] = generated_polygon
            
    if POI_ANNOTATION_TYPE in annotations:
        print('Generating POI annotations...')
        for poi_name in annotations[POI_ANNOTATION_TYPE]:
            generated_poi = {}
            generated_poi['Type'] = POI_ANNOTATION_TYPE
            generated_poi['X'] = annotations[POI_ANNOTATION_TYPE][poi_name][0]['Location'].x
            generated_poi['Y'] = annotations[POI_ANNOTATION_TYPE][poi_name][0]['Location'].y
            generated_poi['Z'] = annotations[POI_ANNOTATION_TYPE][poi_name][0]['Location'].z
            output[poi_name] = generated_poi
    
    return output
    
def is_maze_actor(actor_name):
    name = str(actor_name)
    
    # For some reason, the python API calls 'Hedge_40' 'Hedge_81'
    # The resulting blocking volume is the same, though.
    if (name.startswith('Hedge_')):
        return True
    return False
    
# Assumes a single box collision component
# For use with maze blocks, which are known to have a singular rectangular bounding box
def get_actor_collision_bounding_box(actor):
    static_mesh_component = actor.static_mesh_component
    static_mesh = static_mesh_component.static_mesh
    body_setup = static_mesh.get_editor_property('body_setup')
    agg_geometry = body_setup.get_editor_property('agg_geom')
    box = agg_geometry.get_editor_property('box_elems')[0]
    
    collision_center = box.get_editor_property('center')
    
    collision_x_bounds_half = box.get_editor_property('x') / 2.0
    collision_y_bounds_half = box.get_editor_property('y') / 2.0
    collision_z_bounds_half = box.get_editor_property('z') / 2.0
    
    box_rotator = box.get_editor_property('rotation').transform()
    
    upper_corner = unreal.Vector(collision_x_bounds_half, collision_y_bounds_half, collision_z_bounds_half)
    lower_corner = unreal.Vector(-collision_x_bounds_half, -collision_y_bounds_half, -collision_z_bounds_half)
    
    upper_corner = box_rotator.transform_direction(upper_corner)
    lower_corner = box_rotator.transform_direction(lower_corner)
    
    upper_corner = upper_corner.add(collision_center)
    lower_corner = lower_corner.add(collision_center)
    
    return (upper_corner, lower_corner)
    
def get_maze_actor_collision_bounding_box(actor):
    actor_location = actor.get_actor_location()
    actor_rotation = actor.get_actor_rotation().transform()
    (upper_collision_corner, lower_collision_corner) = get_actor_collision_bounding_box(actor)
    
    upper_collision_corner = actor_rotation.transform_direction(upper_collision_corner)
    lower_collision_corner = actor_rotation.transform_direction(lower_collision_corner)
    
    upper_collision_corner = upper_collision_corner.add(actor_location)
    lower_collision_corner = lower_collision_corner.add(actor_location)
    
    output = {}
    output['MaxX'] = max(upper_collision_corner.x, lower_collision_corner.x)
    output['MaxY'] = max(upper_collision_corner.y, lower_collision_corner.y)
    output['MaxZ'] = max(upper_collision_corner.z, lower_collision_corner.z)
    
    output['MinX'] = min(upper_collision_corner.x, lower_collision_corner.x)
    output['MinY'] = min(upper_collision_corner.y, lower_collision_corner.y)
    output['MinZ'] = min(upper_collision_corner.z, lower_collision_corner.z)
    
    return output
    
    
def generate_maze_annotations():
    all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
    
    maze_min_x = float('inf')
    maze_min_y = float('inf')
    maze_min_z = float('inf')
    maze_max_x = -1 *float('inf')
    maze_max_y = -1 * float('inf')
    maze_max_z = -1 * float('inf')
    
    wall_width = None
    
    actor_collisions = []
    
    for actor in [a for a in all_actors if is_maze_actor(a.get_fname())]:
    
        actor_collision = get_maze_actor_collision_bounding_box(actor)
        
        maze_min_x = min(actor_collision['MinX'], maze_min_x)
        maze_max_x = max(actor_collision['MaxX'], maze_max_x)
        maze_min_y = min(actor_collision['MinY'], maze_min_y)
        maze_max_y = max(actor_collision['MaxY'], maze_max_y)
        maze_min_z = min(actor_collision['MinZ'], maze_min_z)
        maze_max_z = max(actor_collision['MaxZ'], maze_max_z)
        
        # Wall width is the thinnest component
        if (wall_width == None):
            x_width = actor_collision['MaxX'] - actor_collision['MinX']
            y_width = actor_collision['MaxY'] - actor_collision['MinY']
            z_width = actor_collision['MaxZ'] - actor_collision['MinZ']
            wall_width = min(min(x_width, y_width), z_width)
        
        actor_collisions.append(actor_collision)
        
    output = {}
    output['MinX'] = maze_min_x
    output['MaxX'] = maze_max_x
    output['MinY'] = maze_min_y
    output['MaxY'] = maze_max_y
    output['MinZ'] = maze_min_z
    output['MaxZ'] = maze_max_z
    output['WallWidth'] = wall_width
    output['BlockingVolumes'] = actor_collisions
    output['Type'] = MAZE_ANNOTATION_TYPE
    
    print '***'
    print '{0}'.format(len(actor_collisions))
    print '***'
    
    return output
    
def main():
    if (len(sys.argv) != 3):
        print "Error: incorrect usage."
        print ""
        print "Usage: GeneratePathPointsFromMeshes.py <InterpolationStepSize> <OutputFileName>"
        print "\t<InterpolationStepSize> The step size to use for linear interpolation between manually placed points."
        print "\t<OutputFileName> The output file name to which to write the points."
        print ""
        print "The arguments provided were {0}".format(sys.argv)
        return
        
    interpolation_step_size = float(sys.argv[1])
    output_file_name = sys.argv[2]
    
    print 'Generating paths with linear interpolation size of {0}'.format(interpolation_step_size)
    output_data = generate_mesh_paths(interpolation_step_size)
    
    print 'Generating maze annotations...'
    output_data['MazeAnnotations'] = generate_maze_annotations()
    
    print 'Writing output to {0}'.format(output_file_name)
    output_str = json.dumps(output_data, indent=4)
    
    f = None
    try:
        f = open(output_file_name, 'w')
        f.write(output_str)
    finally:
        if (f != None):
            f.close()
    
    print('Graceful termination.')

if __name__ == "__main__":
    main()



