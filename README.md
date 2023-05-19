# Eskimo path  planning exercise

### The objective is to solve a 2D problem by determining the optimal or most efficient route, from the starting point to the destination while navigating around obstacles.

![img.png](project_data/img.png)

## Section 1: An examination of techniques aimed at achieving optimal solutions to the path planning challenge:
- Grassfire Algorithm
- Dijkstra's Algorithm
- A* Algorithm
- D* Algorithm
- D* Lite Algorithm
- Potential Field Algorithm
- Probabilistic Road Map (PRM) Algorithm
- Rapidly Exploring Random Trees (RRT) Algorithm
- RRT* Algorithm
- LQR-RRT* Algorithm
- [Algorithms review](project_data/algo_review.pdf)
- [PPT FILE review](project_data/startup%20mission%20presentaion.pptx)

## Section 2: Generate a text file containing all the required parameters for the algorithm to execute.

### Input:

- Field size
- Start position (x,y)
- End position (x,y)
- Polygons parameters:
    - N - number of icebergs.
    - Dots - number of dots in each iceberg.
    - R - radius size for each iceberg.

### Output: text file

- Field boundry (x-axis)
- Field boundry (y-axis)
- x_start y_start
- x_end y_end
- Number of icebergs
- #1 (iceberg number)
- 1_dots (number of dots in iceberg #1)
- x_1 y_1
- x_2 y_2
- .....
- #2 (iceberg number)
- 1_dots (number of dots in iceberg #2)
- x_1 y_1
- x_2 y_2
- .....
- **Output example**
  ![img.png](project_data/feild-1.png)

## Section 3: Convex Hull problem

- Read the field_data.txt file and solve the [Convex-Hull](https://en.wikipedia.org/wiki/Convex_hull) problem.
- Possible solutions:
    - Jarvis’ Algorithm - $O(n^2)$
    - **Graham Scan Algorithm - $O(nlog(n))$**
    - Quickhull Algorithm - $O(n^2)$
    - Divide and Conquer Algorithm - $O(nlog(n))$
    - Monotone Chain Algorithm - $O(nlog(n))$
    - Incremental Algorithm - $O(nlog(n))$
    - Kirkpatrick–Seidel Algorithm — $O(nlog(n))$
    - Chan's Algorithm — $O(nlog(n))$
- ### Graham Scan Algorithm
    - **Step 1:**
        - Identify the point with the minimum y-coordinate.
          ![img.png](project_data/GRAHM1.png)
    - **Step 2:**
        - Arrange the points in ascending order based on the angle they form with the x-axis, with respect to the pivot point.
          ![img_1.png](project_data/GRAHM2.png)
    - **Step 3:**
        - Remove points from the stack until the orientation of the next three points is not clockwise (or they do not make a right turn).
          ![img.png](project_data/GRAHM3.png)

- **Execute the Graham Scan Algorithm for all the polygons-points generated in the preceding step:**
    - ![img.png](project_data/feild-2.png)

## Section 4: Path planning solution
The path planning process consists of two stages.
The first phase involves creating a graph, while the second stage entails 
determining the most efficient path on that graph.

- **Step 1: Creating a graph (using networkx library)**
    - There exist multiple techniques for graph construction:
        - **Grid** approach.
        - **Naive** approach.
        - **Greedy** approach.
        - **Optimal** approach.
        - **Random** approach.
      
      ## Naive approach: including all available nodes and vertices.
        1. Union of polygons that share a common boundary. (**not convex** polygon)
        2. Connect all possible nodes in the field while also ensuring collision detection and avoidance.

      ![img.png](project_data/naive.png)
  
      ## Greedy approach: select the shortest path to traverse the polygon.
        1. Union of polygons that share a common boundary. (inflation **convex** polygon)
            - **If** the starting or ending point is located inside the union of polygons, then the simple approach of including all available nodes and vertices should be used.
        2. Recursive_algorithm(start_point):
            - If it is possible to draw a straight line between the starting and ending points:
                - Done.
            - else:
                - p = first polygon that lies between the starting point and the ending point.
                - Do ConvexHull(start, end, p)
                - s_left, s_right = Identify two points on the new polygon that are positioned on opposite sides of the starting point.
                - Split the polygon into two smaller polygons and calculate their perimeters.
                - If the left_side is shorter:
                    - Recursive_algorithm(s_left)
                - else:
                    - Recursive_algorithm(s_right)
        ![img.png](project_data/naive.png)

      ## Optimal approach: generating a graph solely based on the relevant convex shapes.
        1. Union of polygons that share a common boundary. (inflation **convex** polygon)
            - **If** the starting or ending point is located inside the union of polygons, then the simple approach of including all available nodes and vertices should be used.
        2. Recursive_algorithm(start_point):
            - If it is possible to draw a straight line between the starting and ending points:
                - Done.
            - else:
                - p = first polygon that lies between the starting point and the ending point.
                - Do ConvexHull(start, end, p)
                - s_left, s_right = Identify two points on the new polygon that are positioned on opposite sides of the starting point.
                - Recursive_algorithm(s_left)
                - Recursive_algorithm(s_right)

      **Example GIF**
      ![img.png](project_data/example_gif.gif)

      ## Random approach: generate a graph in a random manner. (RRT/RRT*)
      1. Union of polygons that share a common boundary. (**not convex** polygon)
      2. Execute the following steps K number of times:
         - Generate a random point.
         - Determine the neighboring points for this randomly generated point and order them in a list.
         - Create a new node between the closest neighboring point and the random point, using a specified step size.
         - If the new node is in proximity to the target point or has reached it:
           - Done!

        ![img.png](project_data/random_graph.png)

- **Step 2:**
    - Utilize path planning algorithms such as A* or Dijkstra's algorithm to solve the path planning problem on this graph.
## Example #1
![img.png](project_data/Figure_1.png)
![img.png](project_data/Figure_2.png)
![img.png](project_data/Figure_3.png)
![img.png](project_data/Figure_4.png)
![img.png](project_data/Figure_5.png)

## Example #2
![img.png](project_data/waze_optimal.png)
![img.png](project_data/waze_rrt.png)


  # Performance Analysis
![img.png](project_data/runtime1.png)

  ### Runtime analysis
![img.png](project_data/runtime_all.png)
![img.png](project_data/runtime_3.png)
![img.png](project_data/runtime2.png)

*****************************************

  ### Comparison (100 attempts):
![img.png](project_data/per_1.png)

**Path length:** (straight line is: 290 sqrt(2)≈410.122)
1. Naive mean 415.398125 (s.d. 11.26)
2. Optimal mean 416.9352083333333 (s.d. 12.96)
3. Greedy mean 418.64572916666674 (s.d. 13.33)
5. Random mean 589.169255319149 (s.d. 54.56)

* Dubins mean 648.76875 (s.d. 200.65)

**Runtime [s]:** 
1. Greedy mean 0.042310516039530434 (s.d. 0.0086)
2. Optimal mean 0.08515359461307526 (s.d. 0.243)
3. Naive mean 3.513621009886265 (s.d. 0.442)
4. Random mean 24.165488650550444 (s.d. 4.52)

* Dubins mean 0.37494373818238574 (s.d. 0.144)


- TBD:
    * Is there room for improvement in the collision detection process in the naive method?
    * How to handle extreme cases in the optimal method?
    * For the random method, what would be the optimal step size? (dynamic step size?)
    * How to distribute the score points, should they be concentrated near the goal or uniformly distributed to avoid obstacles? (pros and cons)

## Part 5: Dubins model

- Lester Eli Dubins (1920–2010) demonstrated in 1957 that the shortest path can be achieved by connecting circular arcs with maximum curvature and straight lines.
- The Dubins model is commonly employed in robotics and motion planning to simplify the description of a vehicle's motion with a fixed turning radius.
- According to the model, the vehicle is restricted to moving in a straight line forwards or backwards, and can only make turns with a consistent radius.

- The parameters in the Dubins model are as follows:
  - **velocity** = constant velocity
  - **phi** = maximum allowable roll angle

- The radius of the turn can calculate by:
  -  $r={v^{2} \over {g\tan \theta }}$
  
- Assumes a constant gravitational acceleration of  (g=9.8 m/s²).

### Dubins algorithm:

1. Compute the optimal path.
2. Update the path:
   - Increase the distance from the obstacle by a constant value (bisector angle). 
   - Remove redundant points (close points).
3. Determine the angle between each point and the next point in the path. 
4. Calculate all six Dubins paths (RSR, LSL, etc.). 
5. Sort the paths based on their lengths. 
6. For each edge, select the shortest collision-free path.

## Example #1

![img.png](project_data/dub_1.png)
![img.png](project_data/dub_2.png)
![img.png](project_data/dub_3.png)
![img.png](project_data/dub_4.png)
![img.png](project_data/dub_5.png)

## Example #2
![img.png](project_data/per_1.png)
![img.png](project_data/per_2.png)
![img.png](project_data/per_3.png)
![img.png](project_data/per_4.png)
![img.png](project_data/per_5.png)
![img.png](project_data/per_6.png)






  
  
  
