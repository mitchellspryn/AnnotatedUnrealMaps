# Annotations

## Mechanics
Annotations are locations of objects of interest inside the simulated environment. The locations of these objects can be useful, e.g. to test path-planning algorithms. Annotations are grouped into a few different kinds of annotation:

* **Points of Interest (AnnotatedPoi)**: These annotations consist of a single XYZ point. These generally mark a single location of interest, such as the end of a path or the entrance to a building. The Point of Interest annotation has the following special fields:
    * **X, Y, Z**: The XYZ coordinates of the point of interest.
* **Directed Path (DirectedPath)**: These annotations represent a series of directed waypoints forming a path. The path can be approximated linearly between each set of waypoints in the list. For example, the waypoint may mark the center of a footpath. The Directed Path annotation has the following special fields:
    * **Coordinates**: A list of points containing the path. Each point has the following fields:
        * **X, Y, Z**: The XYZ coordinates of the point of interest.
        * **IsManual**: True if the point has been manually marked. If false, then the point is linearly interpolated from the neighboring two manual points.
        * **Index**: For manually labled points, the index is the sequence in the path. The first point will have an index of 1, second 2, and so fourth. If the point is not manually labeled, then the index will be null. 
* **Maze Annotations (MazeAnnotations)**: These are a special type of annotation used for the hedge maze in the [Three Bridges map](). This annotation is used to mark the bounds of the maze, as well as each of the different "blocking volumes" within the maze. From this information, it is possible to construct an occupancy matrix for the maze to use for path planning. The MazeAnnotations contains the following special fields:
    * **(Min/Max)(X,Y,Z)**: The locations of the outer bounds of the hedge maze. 
    * **BlockingVolumes**: A list of blocking volumes of each hedge in the maze. Each list element contains the following fields:
        * **(Min/Max)(X, Y, Z)**: The cubical bounding volumes for each of the hedges.  
* **Annotated Polygon (AnnotatedPolygon)**: These annotations describe some sorted bounded volume of interest. For example, it may describe the boundaries of a lake or a stream. The Annotated Polygon annotation contains the following special fields:
    * **Coordinates**: A list of points containing the path. Each point has the following fields:
        * **X, Y, Z**: The XYZ coordinates of the point of interest.
        * **IsManual**: True if the point has been manually marked. If false, then the point is linearly interpolated from the neighboring two manual points.
        * **Index**: For manually labled points, the index is the sequence in the path. The first point will have an index of 1, second 2, and so fourth. If the point is not manually labeled, then the index will be null. Unlike the case of the DirectedPath, this field is mostly meaningless.

In addition to the special fields above, each annotation has the following common fields:
* **Type**: The type of the annotation. This will be one of the strings in the parenthesis above.
* **Name**: This is the name of the annotation. It will describe the annotation in a human readable format. For more information on the specific annotations, consult the [documentation for the map in question]().

Annotations will be stored in a .json file in the folder corresponding to the map name. For example, the annotations for the "three_bridges" map will be stored in "[three_bridges_annotations/three_bridges_annotations.json](https://github.com/mitchellspryn/AnnotatedUnrealMaps/blob/master/AnnotatedUnrealMaps/three_bridges_annotations/three_bridges_annotations.json)".

Annotations are generated via the scripts in the unreal_scripts folder. However, the map needs to be loaded in the unreal editor for the annotations to work; they cannot be generated from the binaries directly. In addition, the generation script will not run in a stand-along python environment, it can only be run from within the unreal environment ('import unreal' will fail to run as expected.)

## Using annotations
In addition to the annotation json, there is python code available to read and interpret the annotations. For a full code example, see [three_bridges_annotations/test_three_bridges_annotations.py](https://github.com/mitchellspryn/AnnotatedUnrealMaps/blob/master/AnnotatedUnrealMaps/three_bridges_annotations/test_three_bridges_annotations.py).

In general. the flow will be as follows:
* **Initialize the AirSim client**. This will be needed when reading the annotations in order to correctly convert the unreal coordinates into GPS geopoints.
* **Create an annotations_common.MapAnnotation class**. The constructor arguments will take the client and the path to the .json file. Note that there is a "scale" optional parameter - currentl this should be left at the default value of 100. This will parse the json file into a convenient data structure and perform any necessary coordinate transformations.
* **Use the annotations**: Once parsing completes, the annotations class will have a dictionary of (annotation_type->annotation). For example, "a.annotations[annotations.DIRECTED_PATH_ANNOTATION_TYPE]" will give all the directed paths. The example code shows how to parse, access, and draw the annotations on the three bridges environment. 