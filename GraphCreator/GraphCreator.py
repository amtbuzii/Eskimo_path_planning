import itertools
import random
import shapely
from shapely.geometry import Point, LineString, Polygon, mapping
import matplotlib.pyplot as plt
import constant
from ConvexHull.ConvexHull import ConvexHull
import networkx as nx
from FieldManager.Field import Field
from itertools import combinations
from shapely.ops import unary_union
from Point import Point
from math import sqrt
from Dubins import Dubins
import logging
import math


def step_point(
    node_a: tuple[float, float], node_b: tuple[float, float], step: float
) -> tuple[float, float]:
    dis = distance(node_a, node_b)
    num_step = dis / step
    x_increment = (node_b[0] - node_a[0]) / num_step
    y_increment = (node_b[1] - node_a[1]) / num_step
    new_x = node_a[0] + (step * x_increment)
    new_y = node_a[1] + (step * y_increment)
    return new_x, new_y


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception("lines do not intersect")

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def line_crosses_convex_shape(
    start_point: tuple[float, float],
    end_point: tuple[float, float],
    convex_shape: list[tuple[float, float]],
) -> bool:
    """
    Check if a line between start_point and end_point crosses a convex_shape.
    return True if the line crosses the shape, False otherwise.
    """

    # Check if points are in the same convex
    if (start_point in convex_shape) and (end_point in convex_shape):
        dist = abs(convex_shape.index(start_point) - convex_shape.index(end_point))
        if dist > 1 and dist != len(convex_shape) - 1:
            return True

    # convert the convex shape to a Shapely polygon
    polygon = Polygon(convex_shape)

    # create a Shapely LineString from the start and end points
    line = LineString([start_point, end_point])

    # check if the line intersects the polygon
    return line.crosses(polygon) or polygon.contains(line)


def get_2_points(
    vertex_a: tuple[float, float],
    vertex_b: tuple[float, float],
    convex_shape: list[tuple[float, float]],
) -> tuple[tuple[float, float], tuple[float, float]]:
    """
    this function do convex hull for exist convex shape, with 2 points.
    return - the 2 neighbors points to vertex_a.
    """
    convex_shape = [Point.Point(pt) for pt in convex_shape]
    vertex_a = Point.Point(vertex_a)
    vertex_b = Point.Point(vertex_b)
    new_convex = ConvexHull(convex_shape + [vertex_a, vertex_b]).graham_scan()
    start_index = new_convex.index(vertex_a)

    # return the neighbors to the start point
    before = (start_index - 1) % len(new_convex)
    after = (start_index + 1) % len(new_convex)

    return new_convex[before].to_tuple(), new_convex[after].to_tuple()


def distance(vertex_a: tuple[float, float], vertex_b: tuple[float, float]) -> float:
    return round(
        sqrt((vertex_a[0] - vertex_b[0]) ** 2 + (vertex_a[1] - vertex_b[1]) ** 2),
        2,
    )


def get_incline(vertex_a: tuple[float, float], vertex_b: tuple[float, float]) -> float:
    if vertex_a[0] == vertex_b[0]:
        return 0
    return (vertex_b[1] - vertex_a[1]) / (vertex_b[0] - vertex_a[0])


def _move_waypoints(
    waypoints: list[tuple[float, float]], distance: float = constant.POLY_TOLERANCE
) -> list[tuple[float, float]]:
    """
    move each point in distance from the current position on the angle bisector
    """

    modified_waypoints = [waypoints[0]]  # Keep the first point unchanged

    # Calculate the bisector for each vertex
    for i in range(1, len(waypoints) - 1):
        prev_vertex = waypoints[i - 1]
        curr_vertex = waypoints[i]
        next_vertex = waypoints[i + 1]

        # Calculate vectors for the adjacent edges
        edge1 = (curr_vertex[0] - prev_vertex[0], curr_vertex[1] - prev_vertex[1])
        edge2 = (curr_vertex[0] - next_vertex[0], curr_vertex[1] - next_vertex[1])

        # Normalize the edge vectors
        edge1_norm = math.sqrt(edge1[0] ** 2 + edge1[1] ** 2)
        edge2_norm = math.sqrt(edge2[0] ** 2 + edge2[1] ** 2)
        edge1 = (edge1[0] / edge1_norm, edge1[1] / edge1_norm)
        edge2 = (edge2[0] / edge2_norm, edge2[1] / edge2_norm)

        # Calculate the angle bisector vector
        bisector = (edge1[0] + edge2[0], edge1[1] + edge2[1])

        # Normalize the bisector vector
        bisector_norm = math.sqrt(bisector[0] ** 2 + bisector[1] ** 2)
        bisector = (bisector[0] / bisector_norm, bisector[1] / bisector_norm)

        # Calculate new vertex coordinates
        new_x = curr_vertex[0] + distance * bisector[0]
        new_y = curr_vertex[1] + distance * bisector[1]
        modified_waypoints.append((new_x, new_y))

    modified_waypoints.append(waypoints[-1])  # Keep the last point unchanged
    return modified_waypoints


class GraphCreator:
    def __init__(self, field: Field):
        self._graph = nx.Graph()
        self._field = field
        self._start = self._field.start.to_tuple()
        self._end = self._field.end.to_tuple()
        self._graph_type = None
        self._polygons = None
        self._polygons_center = None
        self._short_path = None
        self._dubins_path = None
        self._dubins_graph = None
        self._dubins_radius = None

    def create_graph(self, graph_type: str = "Naive") -> None:
        self._graph = nx.Graph()
        self._graph_type = graph_type
        self._polygons = [[] for _ in self._field.polygons]
        for inx, polygon in enumerate(self._field.polygons):
            for point in polygon:
                self._polygons[inx].append(point.to_tuple())

        self._short_path = None

        if graph_type == "Naive":
            self._union_not_convex
            self._naive_graph
        elif graph_type == "Optimal":
            self._union_convex
            self._optimal_graph
        elif graph_type == "RRT":
            self._union_not_convex
            self._random_graph()
        elif graph_type == "RRT*":
            self._union_not_convex
            self._random_graph_RRT_star()
        elif graph_type == "Dubins":
            self._union_convex
            self._optimal_graph
            self.dubins_graph(vel=13, phi=45)
        else:
            logging.warning("invalid graph type (naive / optimal / RRT)")
            raise ValueError("invalid graph type")

    @property
    def _union_not_convex(self) -> None:
        """
        union crosses convexes shape to new NOT convex shape - relevant only for naive solution.
        """

        pair_polygons = itertools.combinations(self._polygons, 2)

        for poly_a, poly_b in pair_polygons:
            polygon1 = Polygon(poly_a)
            polygon2 = Polygon(poly_b)
            if polygon1.intersects(polygon2):
                new_convex = unary_union([polygon1, polygon2])
                new_convex = mapping(new_convex)
                new_convex = [
                    _ for _ in new_convex["coordinates"][0]
                ]  # convert to list of tuple [(x,y),(x,y)...]
                self._polygons.append(new_convex)
                self._polygons.remove(poly_a)
                self._polygons.remove(poly_b)
                self._union_not_convex
                return
        return

    @property
    def _naive_graph(self) -> None:
        """
        create a naive graph.
        points = start, end, all convex dots
        create edge only if the edge not cross anything
        """

        # All points in one list
        all_points = [self._start, self._end] + sum(self._polygons, [])

        # remove not in the map points
        all_points = [point for point in all_points if self._vertex_inside_map(point)]

        # Get all combinations of points - no return.
        comb = combinations(all_points, 2)

        # For each pair, check if it is possible to create edge. (except if the vertexes are equal)
        for vertex_a, vertex_b in list(comb):
            if vertex_a != vertex_b:
                self._add_edge_to_graph(vertex_a, vertex_b)

        return

    def _add_edge_to_graph(
        self, vertex_a: tuple[float, float], vertex_b: tuple[float, float]
    ) -> bool:
        """
        add edge  between 2 points if it is OK.
        """
        for p in self._polygons:
            if line_crosses_convex_shape(vertex_a, vertex_b, p):
                line1 = LineString([vertex_a, vertex_b])
                polygon = shapely.Polygon(p)
                points = polygon.intersection(line1)
                return points

        # it is possible to connect
        weight = distance(vertex_a, vertex_b)
        self._graph.add_edge(vertex_a, vertex_b, weight=weight)
        return True

    @property
    def _optimal_graph(self) -> None:
        """
        create optimal graph (using recursive function - self._rec_optimal_graph
        """

        for p in self._polygons:
            polygon = Polygon(p)
            if (polygon.contains(shapely.geometry.Point(self._start))) or (
                polygon.contains(shapely.geometry.Point(self._end))
            ):
                logging.info(
                    "No optimal solution - start/end point inside convex shape, try naive way"
                )
                exit()

        self._polygons_center = self._polygons_center_calc
        self._rec_optimal_graph(self._start, self._end)

    @property
    def _union_convex(self) -> None:
        """
        union crosses convexes shape to new convex shape - relevant to optimal solution.

        :rtype: None
        """
        pair_polygons = itertools.combinations(self._polygons, 2)
        for poly_a, poly_b in pair_polygons:
            if Polygon(poly_a).intersects(Polygon(poly_b)):
                temp_a = [Point.Point(pt) for pt in poly_a]
                temp_b = [Point.Point(pt) for pt in poly_b]
                new_convex = ConvexHull(temp_a + temp_b).graham_scan()
                self._polygons.append([pt.to_tuple() for pt in new_convex])
                self._polygons.remove(poly_a)
                self._polygons.remove(poly_b)
                self._union_convex
                return
        return

    def _get_polygon_between_2_points(
        self, start_vertex: tuple[float, float], end_vertex: tuple[float, float]
    ) -> int:
        """
        return the polygon index if it is between 2 points.
        """
        for index, polygon in enumerate(self._polygons):
            if start_vertex in polygon:
                if line_crosses_convex_shape(start_vertex, end_vertex, polygon):
                    return index

        for index, polygon in enumerate(self._polygons):
            if line_crosses_convex_shape(start_vertex, end_vertex, polygon):
                return index
        return -1

    def _rec_optimal_graph(
        self, start_vertex: tuple[float, float], end_vertex: tuple[float, float]
    ) -> None:
        """
        create optimal graph recursively.
        only vertexes in the relevant direction.
        """
        middle_polygon = self._get_polygon_between_2_points(start_vertex, end_vertex)

        if middle_polygon == -1:  # it is possible to get from start_vertex to end point
            self._add_edge_to_graph(start_vertex, end_vertex)
            return

        else:
            next_points = get_2_points(
                start_vertex, end_vertex, self._polygons[middle_polygon]
            )
            for vertex in next_points:
                if self._vertex_inside_map(vertex):  # vertex inside the map
                    if (start_vertex, vertex) not in self._graph.edges:
                        self._rec_optimal_graph(start_vertex, vertex)
                        if (vertex, end_vertex) not in self._graph.edges:
                            self._rec_optimal_graph(vertex, end_vertex)

    def _vertex_inside_map(self, vertex: tuple[float, float]) -> bool:
        x, y = vertex
        if not (0 < x < self._field.size) or not (0 < y < self._field.size):
            return False
        return True

    def _get_random_point(self) -> tuple[float, float]:
        while True:
            _x = random.uniform(0, self._field.size)
            _y = random.uniform(0, self._field.size)
            if self._vertex_inside_map((_x, _y)):
                return _x, _y
        # if not self._collision_detector((_x, _y)):

    def _find_neighbors(self, vertex) -> dict[tuple[float, float] : float]:
        neighbors = dict()
        for node in self._graph.nodes:
            neighbors[node] = distance(vertex, node)

        return sorted(neighbors, key=neighbors.get)

    def _random_graph(self) -> None:
        """
        create random graph - RRT
        """
        n_iter = constant.ITERATION
        random.seed(random.randint(0, 1555))
        self._graph.add_node(self._start)
        for _ in range(n_iter):
            random_vertex = self._get_random_point()
            neighbors = self._find_neighbors(random_vertex)
            for node in neighbors:
                new_node = step_point(node, random_vertex, constant.STEP_SIZE)
                if self._vertex_inside_map(new_node):
                    if self._add_edge_to_graph(node, new_node):
                        break

        neighbors = self._find_neighbors(self._end)
        for node in neighbors:
            if self._add_edge_to_graph(node, self._end):
                break
        return

    def dubins_graph(
        self, vel: float = constant.DUBINS_VEL, phi: float = constant.DUBINS_PHI
    ) -> None:
        """
        create dubins graph
        vel = constant velocity
        phi =  maximum allowable roll angle
        """
        wptz = []
        self._dubins_radius = (vel * vel) / (9.8 * math.tan(phi * math.pi / 180))
        self.shortest_path()
        self._dubins_path = self._update_dubins_points(self._short_path[1])

        for inx in range(len(self._dubins_path) - 1):
            pt = self._dubins_path[inx]
            psi = Dubins.angle_between_points(pt, self._dubins_path[inx + 1])
            temp_pt = Dubins.Waypoint(pt[0], pt[1], psi)
            wptz.append(temp_pt)
        wptz.append(
            Dubins.Waypoint(self._dubins_path[-1][0], self._dubins_path[-1][1], psi)
        )

        self._dubins_graph = nx.Graph()

        xx = []
        yy = []
        i = 0
        valid_dubins = True
        while i < len(wptz) - 1:
            param_dict = Dubins.calc_dubins_path(
                wptz[i], wptz[i + 1], vel=vel, phi_lim=phi
            )
            param_dict = list(sorted(param_dict.items()))
            for j, param_j in enumerate(param_dict):
                param = param_j[1]
                path = Dubins.dubins_traj(param=param, step=1)
                if self._check_dubins_collision(path[:, 0:2]):
                    xx.extend(path[:, 0])
                    yy.extend(path[:, 1])
                    break
                if j == len(param_dict) - 1:
                    valid_dubins = False
            i += 1

        if not valid_dubins:
            logging.debug("No valid dubins path found")
        else:
            logging.debug("Valid dubins path found")
            for i in range(len(xx) - 1):
                vertex_a = (xx[i], yy[i])
                vertex_b = (xx[i + 1], yy[i + 1])
                weight = distance(vertex_a, vertex_b)
                self._dubins_graph.add_edge(vertex_a, vertex_b, weight=weight)
            self.dubins_last_vertex = vertex_b

    def _check_dubins_collision(self, dubins_path: list[tuple[float, float]]) -> bool:
        """
        check if dubins path is valid == not inside polygons
        """
        for vertex in dubins_path:
            for p in self._polygons:
                polygon = Polygon(p)
                if polygon.contains(shapely.geometry.Point(vertex)):
                    return False

        return True

    def _update_dubins_points(
        self, points: list[tuple[float, float]]
    ) -> list[tuple[float, float]]:
        """
        update point for dubins path. increase the distance between the point and polygon border.
        and remove redundant points.
        """
        # increase the distance between the point and polygon border
        new_points = _move_waypoints(waypoints=points, distance=self._dubins_radius)

        # remove redundant points
        point_poly = [self._get_point_polygon(point) for point in points]
        for jj in range(1, len(point_poly) - 1):
            if (
                point_poly[jj] == point_poly[jj - 1]
                and point_poly[jj] == point_poly[jj + 1]
            ):
                new_points.pop(jj)
                point_poly.pop(jj)
                jj -= 1
            if distance(new_points[jj], new_points[jj - 1]) < self._dubins_radius * 2:
                new_points.pop(jj)
        return new_points

    def _get_point_polygon(self, point) -> int:
        """
        return the polygon index that the point located on it border.
        """
        for index, poly in enumerate(self._polygons):
            if point in poly:
                return index
        return -1

    @property
    def _polygons_center_calc(self) -> dict[int, tuple]:
        """
        return dictionary with the center of the polygons
        """
        polygons_dict = dict()
        for index, polygon in enumerate(self._polygons):
            _x_list = [vertex[0] for vertex in polygon]
            _y_list = [vertex[1] for vertex in polygon]
            _len = len(polygon)
            _x = sum(_x_list) / _len
            _y = sum(_y_list) / _len
            polygons_dict[index] = (_x, _y)

        return polygons_dict

    def shortest_path(self) -> nx.Graph:
        """
        get the shortest path using dijkstra
        """
        try:
            self._short_path = nx.single_source_dijkstra(
                self._graph, self._start, self._end, weight="weight"
            )
            return self._short_path[0]

        except nx.exception.NodeNotFound:
            logging.warning("No path found, try naive way.")
        except nx.exception.NetworkXNoPath:
            logging.warning("No optimal path")

    def get_dubins_path_length(self) -> nx.Graph:
        try:
            dubins_length = nx.single_source_dijkstra(
                self._dubins_graph,
                self._start,
                self.dubins_last_vertex,
                weight="weight",
            )
            return dubins_length[0]

        except nx.exception.NodeNotFound:
            logging.warning("No Dubins path found.")
        except nx.exception.NetworkXNoPath:
            logging.warning("No Dubins path")

    def draw_graph(self, dubins: bool = False, save: bool = False, t: int = 0) -> None:
        pos = {point: point for point in self._graph.nodes}

        # add axis
        fig, ax = plt.subplots()
        for i, p in enumerate(self._polygons):
            polygon1 = Polygon(p)
            x, y = polygon1.exterior.xy
            plt.plot(x, y, alpha=0.5)

        # figure title
        fig.suptitle("Eskimo field", fontsize=15)
        ax.set_title(self._graph_type)

        # draw nodes and edges
        if self._dubins_graph is None:
            nx.draw(self._graph, pos=pos, node_size=5, ax=ax, style="-.")

        # plot START + END point
        ax.scatter(
            self._start[0],
            self._start[1],
            color="blue",
            marker="p",
            s=50,
            label="Start",
        )
        ax.scatter(
            self._end[0],
            self._end[1],
            color="red",
            marker="*",
            s=50,
            label="End",
        )
        # plt.xlim(-50, 350)
        # plt.ylim(-50, 350)

        # Shortest path
        if self._short_path is not None:
            # draw path in red

            path = self._short_path[1]
            path_edges = list(zip(path, path[1:]))

            nx.draw_networkx_nodes(
                self._graph,
                pos,
                nodelist=path,
                node_size=2,
                node_color="r",
                ax=ax,
            )
            nx.draw_networkx_edges(
                self._graph,
                pos,
                edgelist=path_edges,
                width=2,
                alpha=0.3,
                edge_color="r",
                ax=ax,
            )
            # Adding text
            if self._dubins_graph is None:
                plt.text(
                    100,
                    310,
                    "Path length " + str(("%.2f" % self._short_path[0])),
                    fontsize=10,
                    bbox=dict(facecolor="red", alpha=0.5),
                )

        if self._dubins_graph is not None:
            pos = {point: point for point in self._dubins_graph.nodes}
            x = [point[0] for point in self._dubins_path]
            y = [point[1] for point in self._dubins_path]
            ax.scatter(
                x,
                y,
                color="red",
                marker=".",
                s=50,
            )
            nx.draw(
                self._dubins_graph,
                pos=pos,
                node_size=0.01,
                ax=ax,
                style="-.",
            )  # draw nodes and edges

            plt.text(
                100,
                310,
                "Path length " + str(("%.2f" % self.get_dubins_path_length())),
                fontsize=10,
                bbox=dict(facecolor="red", alpha=0.5),
            )

        # grid configurations
        plt.axis("on")
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=5)
        # ax.grid()
        # if save: plt.savefig(f'./img/img_{t}.png', transparent=False,facecolor='white')
        plt.show()
