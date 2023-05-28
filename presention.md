---
marp: true
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')

---
![bg right](https://www.worldatlas.com/r/w960-q80/upload/60/f2/c4/shutterstock-372285280.jpg)


# Eskimo

Find the best path from A to B while avoiding obstacles in a 2D environment.

**Amit Bouzaglo** - [GitHub](https://github.com/amtbuzii/Eskimo_path_planning)


---


![bg 40%](https://cdn.freebiesupply.com/logos/large/2x/rafael-logo-svg-vector.svg)



---
## Path planning algorithms review:
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

[PDF](https://github.com/amtbuzii/Eskimo_path_planning/blob/main/project_data/algo_review.pdf)


---
## Generate field  

 Input:

    - Field size
    - Start position (x,y)
    - End position (x,y)
    - Polygons parameters:
        - N - number of icebergs.
        - Dots - number of dots in each iceberg.
        - R - radius size for each iceberg.

![bg right 90%](project_data/feild-1.png)

---

![bg right:25% 90%](https://ds055uzetaobb.cloudfront.net/uploads/tantSbEgDe-ch2.gif)

### Convex Hull
* Jarvis’ Algorithm - $O(n^2)$
* Quickhull Algorithm - $O(n^2)$
* Divide and Conquer Algorithm - $O(nlog(n))$
* Monotone Chain Algorithm - $O(nlog(n))$
* Incremental Algorithm - $O(nlog(n))$
* Kirkpatrick–Seidel Algorithm — $O(nlog(n))$
* Chan's Algorithm — $O(nlog(n))$
* **Graham Scan Algorithm - $O(nlog(n))$**

---
![bg vertical 80%](project_data/GRAHM1.png)
![bg right:40% 80%](project_data/GRAHM2.png)
![bg 80%](project_data/GRAHM3.png)

-  **Graham Scan Algorithm**
    - Pivot - minimum y-coordinate.
    - Sort points by angle with pivot.
    - Initialize stack with pivot point.
    - Iterate - for each point:
        - Push point onto stack.
        - removing points until a counterclockwise orientation is obtained.
    - The remaining points on the stack form the convex hull.
---

![bg 60%](project_data/feild-2.png)

---

## Path planning solution

1. Creating a graph: (using networkx library)
    - Gr**i**d approach (not implemented).
    - Naive approach.
    - Gr**ee**dy approach.
    - Optimal approach.
    - Random approach.

2. Once the graph is prepared, determine the optimal path:
    - Dijkstra, A*, etc.

---   
### Naive approach:
Including all available nodes and vertices.
1. Union polygons.
2. Connect all possible nodes in the field while also ensuring collision detection and avoidance.

![bg right 120%](project_data/Naive_ex.png)

---
### Greedy approach:
* The shortest path to traverse the polygon:
    1. Union polygons.
    2. Recursive algorithm.

![bg right:50% 120%](project_data/greedy_ex..png)
           
---
## Greedy approach algorithm

    def greedy(start, end):
        -if it is possible to draw a straight line:
            - Done.
        -else:
            - p = first polygon that lies between the starting point and the ending point.
            - Do ConvexHull(start, end, p)
            - s_left, s_right = Identify two points on the new polygon 
            - split the polygon into two polygons:
                - If the left_side perimeter is shorter:
                    - greedy(s_left)
                - else:
                    - greedy(s_right)

---
### Optimal approach:
1. Union polygons.
2. Recursive algorithm.
![bg right:50% 120%](project_data/optimal_ex.png)

---
## Optimal approach algorithm
    def optimal_path(start, end):
    - if it is possible to draw a straight line:
        - Done.
    - else:
        - p = first polygon that lies between the starting point and end point.
        - Do ConvexHull(start, end, p)
        - s_left, s_right = Identify two points on the new 
          polygon that are positioned on opposite sides of the starting point.
        - optimal_path(start, s_left), optimal_path(s_left, end)
        - optimal_path(start, s_right), optimal_path(s_right, end)
---
![bg 80%](project_data/example_gif.gif)

---


## Random approach
Generate a graph in a random manner. (RRT)
1. Union polygons.
2. do K times:
    - Generate a valid random point.
    - Find closet neighbor.
    - Create a new node between both. (step size)

![bg right 120%](project_data/RRT_ex.png)

---

Example
![bg 70%](project_data/waze_optimal.png)

---

Example
![bg 70%](project_data/waze_rrt.png)

---
# Performance Analysis
* Runtime
* Length


![bg right:45% 60%](project_data/growth.png)

---
![bg 80%](project_data/runtime_all.png)

---
![bg 80%](project_data/runtime_3.png)

---

### Comparison
*  100 attempts

![bg right 100%](project_data/per_1.png)

---

## Path length: 
* direct line $≈410.122$

1. **Naive** $\mu=415.34$, $\sigma=11.26$
2. **Optimal** $\mu=416.93$, $\sigma=12.96$
3. **Greedy** $\mu=418.64$, $\sigma=13.33$
4. **Random** $\mu=589.17$, $\sigma=54.56$

**Dubins** $\mu=648.77$, $\sigma=200.65$

![bg right:45% 120%](project_data/lengths_c.png)

---
![bg 75%](project_data/lengths_c2.png)

---

## Runtime [s]: 
1. **Greedy** $\mu=0.0423$, $\sigma=0.008$
2. **Optimal** $\mu=0.085$, $\sigma=0.243$
3. **Naive** $\mu=3.513$, $\sigma=0.442$
4. **Random** $\mu=24.165$, $\sigma=4.52$

* **Dubins** $\mu=0.374.77$, $\sigma=0.14$

![bg right:45% 120%](project_data/runtime_c.png)


---
## Dubins model

- Lester Eli Dubins (1920–2010)
- Model parameters:
  - **velocity**  $v$ = constant velocity
  - **phi** $\phi$ = maximum allowable roll angle

- The radius of the turn can be calculated by:
  -  $r={v^{2} \over {g\tan \phi }}$
  
- Assumes a constant gravitational acceleration of  (g=9.8 m/s²).
---
### Dubins algorithm:

1. Compute the optimal path.
2. Update the path:
   - Increase the distance from the obstacle by a constant value (bisector angle). 
   - Remove redundant points (close points).
3. Determine the angle between each point and the next point in the path. 
4. Calculate all six Dubins paths (RSR, LSL, etc.). 
5. Sort the paths based on their lengths. 
6. For each edge, select the shortest collision-free path.
---
## Example

![bg 75%](project_data/dub_1.png)

---
![bg 75%](project_data/dub_2.png)

---

![bg 75%](project_data/dub_3.png)

---

![bg 75%](project_data/dub_4.png)

---

![bg 75%](project_data/dub_5.png)

---
## Example #2
![bg 75%](project_data/per_3.png)

---
![bg 75%](project_data/per_6.png)

--- 
* Collision detection process improvements:
    * Use efficient data structures (BVHs or Octrees).
    * Employ hierarchical techniques and parallel processing.

* Random method:
    * Step size (fixed or dynamic).
    * Uniform or target-focused distribution.

* Dubins - finding a closer solution:
    * Utilize heuristics for feasible solutions.


    ![bg right:25% 85%](https://pbr-book.org/3ed-2018/Primitives_and_Intersection_Acceleration/LBVH%20treelet%20clusters.svg)

---

![bg 60%](https://cdn4.iconfinder.com/data/icons/iconsimple-logotypes/512/github-512.png)
![bg 90%](https://cdn.freebiesupply.com/logos/large/2x/rafael-logo-svg-vector.svg)
![bg 80%](https://marp.app/assets/marp.svg)

---

## Code

![bg right:70% 65%](project_data/development.png)

---
![bg 90%](project_data/eskimo_program.png)

---
## GUI

*  [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

![bg right:60% 90%](project_data/program_1.png)

---

# Questions?

Thank you

![bg](https://knowledge.wharton.upenn.edu/wp-content/uploads/2022/02/Questions-900x387.jpg)

---
    * Pseudorandom number generator
    * Rejection sampling
    * Git
    * *.MD file
    * pre-commit - hook, black, linter, flake
    * logger
    * Python libary: numpy, networkx, shapley, matplotlib, itertools
    * Exception Handling
    * Dependency injection
    * unitest
    * Debugging process
    * requirments.txt
    * Performance analysis

