import itertools
import random
import shapely
from shapely import LineString
from shapely.geometry import Point, LineString, Polygon, mapping
import matplotlib.pyplot as plt
from ConvexHull.ConvexHull import ConvexHull
import networkx as nx
from FieldManager.Field import Field
from itertools import combinations
from shapely.ops import unary_union
from Point import Point
from math import sqrt
from Dubins import Dubins
import logging


def step_point(node_a: tuple[float, float], node_b: tuple[float, float], step: float) -> tuple[float, float]:
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
    if (
        (start_point in convex_shape)
        and (end_point in convex_shape)
        and (
            abs(convex_shape.index(start_point) - convex_shape.index(end_point))
            > 1
        )
    ):
        return True

    # convert the convex shape to a Shapely polygon
    polygon = Polygon(convex_shape)

    # create a Shapely LineString from the start and end points
    line = LineString([start_point, end_point])

    # check if the line intersects the polygon
    return line.crosses(polygon)


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


def distance(
    vertex_a: tuple[float, float], vertex_b: tuple[float, float]
) -> float:
    return round(
        sqrt(
            (vertex_a[0] - vertex_b[0]) ** 2 + (vertex_a[1] - vertex_b[1]) ** 2
        ),
        2,
    )


class GraphCreator:
    def __init__(self, field: Field):
        self._graph = nx.Graph()
        self._field = field
        self._start = self._field.start.to_tuple()
        self._end = self._field.end.to_tuple()
        self._polygons = None
        self._polygons_center = None
        self._short_path = None
        self._dubins_path = None

    def create_graph(self, graph_type: str = "naive") -> None:
        self._graph = nx.Graph()
        self._polygons = [[] for _ in self._field.polygons]
        for inx, polygon in enumerate(self._field.polygons):
            for point in polygon:
                self._polygons[inx].append(point.to_tuple())

        self._short_path = None

        if graph_type == "naive":
            self._union_not_convex
            self._naive_graph
        elif graph_type == "optimal":
            self._union_convex
            self._optimal_graph
        elif graph_type == "RRT":
            self._union_not_convex
            self._random_graph()
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

        # Get all combinations of points - no return.
        comb = combinations(all_points, 2)

        # For each pair, check if it is possible to create edge.
        for vertex_a, vertex_b in list(comb):
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
                return False

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
        self._rec_optimal_graph(self._start)

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

    def _rec_optimal_graph(self, start_vertex: tuple[float, float]) -> None:
        """
        create optimal graph recursively.
        only vertexes in the relevant direction.
        """
        direct_line = (
            True  # if it is possible to get from start_vertex to end point
        )
        _relevant_polygons = dict()
        same_polygon = False
        for index, polygon in enumerate(self._polygons):
            if line_crosses_convex_shape(start_vertex, self._end, polygon):
                direct_line = False
                if start_vertex in polygon:
                    same_polygon = True
                    break
                else:
                    center_point = self._polygons_center[index]
                    _relevant_polygons[index] = distance(
                        start_vertex, center_point
                    )
        if (
            not direct_line
        ):  # there isn't direct line between start_vertex to end
            if same_polygon:
                p = self._polygons[index]
            else:
                p = self._polygons[
                    min(_relevant_polygons, key=_relevant_polygons.get)
                ]
            ch = get_2_points(start_vertex, self._end, p)
            for vertex in ch:
                if self._add_edge_to_graph(start_vertex, vertex):
                    found = any(vertex == edge[0] for edge in self._graph.edges)
                    if not found:
                        self._rec_optimal_graph(vertex)
        else:  # there is direct line between start_vertex to end
            self._add_edge_to_graph(start_vertex, self._end)
            return

    def _get_random_point(self) -> tuple[float, float]:
        #while True:
        _x = random.uniform(self._start[0]-100.0, self._field.size)
        _y = random.uniform(self._start[1]-100.0, self._field.size)
            #if not self._collision_detector((_x, _y)):
        return _x, _y

    def _find_neighbors(self, vertex) -> dict[tuple[float,float]: float]:
        neighbors = dict()
        for node in self._graph.nodes:
            neighbors[node] = distance(vertex, node)

        return sorted(neighbors, key=neighbors.get)

    def _random_graph(self) -> None:
        """
        create random graph (using recursive function - self._rec_optimal_graph
        """
        n_iter = 900
        random.seed(random.randint(0, 1555))
        self._graph.add_node(self._start)
        for _ in range(n_iter):
            random_vertex = self._get_random_point()
            neighbors = self._find_neighbors(random_vertex)
            for node in neighbors:
                #new_node = random_vertex
                #if not self._add_edge_to_graph(node, new_node):
                new_node = step_point(node, random_vertex, 3)
                if self._add_edge_to_graph(node, new_node):
                    break
                #else:
                 #   break
            #if self._add_edge_to_graph(new_node, self._end):
             #   print("bla")
              #  logging.info("RTT iterations: {}".format(_))
               # return


        neighbors = self._find_neighbors(self._end)
        for node in neighbors:
            if self._add_edge_to_graph(node, self._end):
                break

        return

    def dubins_graph(self, vel: float = 50, phi: float = 10) -> None:
        """
        create dubins graph
        """

        xx, yy = Dubins.create_dubins_path(self._short_path[1], vel=vel, phi=phi)

        fig, ax = plt.subplots()
        for i, p in enumerate(self._polygons):
            polygon1 = Polygon(p)
            x, y = polygon1.exterior.xy
            plt.plot(x, y)

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
        plt.scatter(xx, yy, s=0.1, color = "gold")

        # grid configurations
        plt.axis("on")
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=5)
        plt.show()

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
        try:
            self._short_path = nx.single_source_dijkstra(
                self._graph, self._start, self._end, weight="weight"
            )
            return self._short_path[0]

        except nx.exception.NodeNotFound:
            logging.warning("No Path found, try naive way.")
        except nx.exception.NetworkXNoPath:
            logging.warning('No optimal path')

    def draw_graph(self, save=False, t=0) -> None:
        pos = {point: point for point in self._graph.nodes}

        # add axis
        fig, ax = plt.subplots()
        for i, p in enumerate(self._polygons):
            polygon1 = Polygon(p)
            x, y = polygon1.exterior.xy
            plt.plot(x, y)

        # figure title
        fig.suptitle("Eskimo field", fontsize=15)

        nx.draw(
            self._graph, pos=pos, node_size=15, ax=ax
        )  # draw nodes and edges
        # nx.draw_networkx_labels(self._graph, pos=pos)  # draw node labels/names

        # draw edge weights
        # labels = nx.get_edge_attributes(self._graph, 'weight')
        # nx.draw_networkx_edge_labels(self._graph, pos=pos, edge_labels=labels, ax=ax)

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
        plt.xlim(-20, 320)
        plt.ylim(-20, 340)

        # Shortest path
        if self._short_path is not None:
            # draw path in red
            path = self._short_path[1]
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_nodes(
                self._graph,
                pos,
                nodelist=path,
                node_size=5,
                node_color="r",
                ax=ax,
            )
            nx.draw_networkx_edges(
                self._graph,
                pos,
                edgelist=path_edges,
                width=6,
                alpha=0.3,
                edge_color="r",
                ax=ax,
            )
            # Adding text
            plt.text(
                100,
                310,
                "Path length " + str(("%.2f" % self._short_path[0])),
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
