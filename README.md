# Eskimo path  planning
### Goal - 2D problem, finding the best/shortest path (from start to end) with obstacles.

![img.png](project_data/img.png)

## Part 1: A review of algorithms for optimally solving the path planning problem.
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
-  [Algorithms review](project_data/algo_review.pdf)
-  [PPT FILE review](project_data/startup%20mission%20presentaion.pptx)


## Part 2: Create text file with parameters needed to the algorithm
### Input:
- field size
- starting point (x,y)
- end point (x,y)
- random polygons:
  - N - number of icebergs.
  - Dots - number of dots in each iceberg.
  - R - radius size for each iceberg.
  
### Output: text file
- field boundry (x-axis)
- field boundry (y-axis)
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
- **Example**
![img.png](project_data/feild-1.png)

## Part 3: Convex Hull problem (solving  with c++)
- Read the data_cpp.txt file in C++ and solve the Convex-Hull problem
- [Convex-Hull](https://en.wikipedia.org/wiki/Convex_hull)
- Possible solutions:
  - Jarvis’ Algorithm -  $O(n^2)$
  - **Graham Scan Algorithm - $O(nlog(n))$**
  - Quickhull Algorithm - $O(n^2)$
  - Divide and Conquer Algorithm - $O(nlog(n))$
  - Monotone Chain Algorithm - $O(nlog(n))$
  - Incremental Algorithm - $O(nlog(n))$
  - Kirkpatrick–Seidel Algorithm — $O(nlog(n))$
  - Chan's Algorithm — $O(nlog(n))$
- ### Graham Scan Algorithm
  - **Step 1:**
    - Find the point with the lowest y-coordinate
    ![img.png](project_data/GRAHM1.png)
  - **Step 2:**
    - Sort the points in increasing order of the angle they and the pivot point make with the x-axis
    ![img_1.png](project_data/GRAHM2.png)
  - **Step 3:**
    - Keep removing points from stack while orientation of following 3 points is not counterclockwise (or they don’t make a left turn). 
    ![img.png](project_data/GRAHM3.png)
    
      
- **Performing Graham Scan Algorithm for all  polygons we created in the previous step:**   
  - ![img.png](project_data/feild-2.png)



## Part 4: path planning solution - A*

## Part 5: Dubbins model

  
  
  
