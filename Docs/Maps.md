# Maps
This document contains information about the maps included in this repository, as well as the annotations available. 

## Three Bridges
This map is a large outdoor environment, which contains a variety of different landscape textures. It can be described as a grassy meadow surrounded by mountains on three sides, and water on the fourth. There is a river running through the environment, with three bridges of different sizes and styles crossing it at different points. One side of the map contains sandy beaches, while the other contains heavy tree and rock cover. There are multiple dirt paths that connect the different bridges, which have been annotated. There is also a hedge maze at one point in the map. The landscape contains rolling hills, except for the hedge maze, which is perfectly flat. Finally, there are two lakes in the map. Below is an overhead view of the environment with the annotations superimposed:

![Image]()

The available annotations are labeled in the image below. For more information about the basics of annotations and how to use them, see the [annotations documentation]().There are two annotated polygons, labeled **A** and **B**. They are shown in the image as red dots connected by thin green lines. These polygons are:
* **A**: **Lake1**. The boundary here represents the place where the ground meets the water plane for the lake.
* **B**: **Lake2**: The boundary here represents the place where the ground meets the water plane for the lake.

There are 16 labeled points of interest, labeled **C** through **R**. These show up in the image above as purple cubes. These points of interest are:
* **C**: **Beach1**: The ending point of the path and the beach on the left side of the water.
* **D**: **Beach2**: The ending point of the path and the beach on the right side of the water.
* **E**: **LowerBridge1**: The entrance of the bridge closest to the ocean on the left side.
* **F**: **LowerBridge2**: The entrance of the bridge closest to the ocean on the right side.
* **G**: **MidBridge1**: The entrance of the bridge in the middle on the left side.
* **H**: **MidBridge2**: The entrance of the bridge in the middle on the right side.
* **I**: **UpperBridge1**: The entrance of the bridge closest to the lake on the left side.
* **J**: **UpperBridge2**: The entrance of the bridge closest to the lake on the right side.
* **K**: **PathFork1**: The meeting of multiple paths. 
* **L**: **PathFork2**: The meeting of multiple paths.
* **M**: **PathFork3**: The meeting of multiple paths.
* **N**: **TrailEnd1**: The end of the first trail. There is an invisible blocking volume that will prevent further progress along this path. 
* **O**: **TrailEnd2**: The end of the second trail. There is an invisible blocking volume that will prevent further progress along this path.
* **P**: **TrailEnd3**: The end of the third trail. There is an invisible blocking volume that will prevent further progress along this path.
* **Q**: **Maze1**: The first entry point to the hedge maze.
* **R**: **Maze2**: The second entry point to the hedge maze.

In addition to the labeled points of interest, some of them have been connected with manually labeled waypoints. These waypoints appear in green, with the paths connected by blue lines. These directed paths are named **(StartPOI)to(EndPOI)**. For example, the path connecting Beach1 and PathFork1 is called "Beach1ToPathFork1." In genral, paths start at the waypoint closest to the bottom-left corner, and end at the waypoint closest to the top right.

Finally, there is a yellow box around the bounds of the hedge maze. This volume corresponds to the annotated (Min/Max)(X, Y, Z) annotations. This annotation is called **"MazeAnnotation"**, and also contains the locations of each of the individual hedges. 