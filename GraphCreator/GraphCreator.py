import itertools
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
import logging


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def line_crosses_convex_shape(start_point: tuple[float, float], end_point: tuple[float, float],
                              convex_shape: list[tuple[float, float]]) -> bool:
    """
    Check if a line between start_point and end_point crosses a convex_shape.
    return True if the line crosses the shape, False otherwise.
    """

    # Check if points are in the same convex
    if (start_point in convex_shape) and (end_point in convex_shape) and (
            abs(convex_shape.index(start_point) - convex_shape.index(end_point)) > 1):
        return True

    # convert the convex shape to a Shapely polygon
    polygon = Polygon(convex_shape)

    # create a Shapely LineString from the start and end points
    line = LineString([start_point, end_point])

    # check if the line intersects the polygon
    return line.crosses(polygon)


def get_2_points(vertex_a: tuple[float, float], vertex_b: tuple[float, float],
                 convex_shape: list[tuple[float, float]]) -> tuple[tuple[float, float], tuple[float, float]]:
    """
    this function do convex hull for exist convex shape, with 2 points.
    return - the 2 neighbors points to vertex_a.
    """
    convex_shape = [Point.Point(x_y=pt) for pt in convex_shape]
    vertex_a = Point.Point(x_y=vertex_a)
    vertex_b = Point.Point(x_y=vertex_b)
    new_convex = ConvexHull(convex_shape + [vertex_a, vertex_b]).graham_scan()
    start_index = new_convex.index(vertex_a)

    # return the neighbors to the start point
    before = (start_index - 1) % len(new_convex)
    after = (start_index + 1) % len(new_convex)

    return new_convex[before].to_tuple(), new_convex[after].to_tuple()


def distance(vertex_a: tuple[float, float], vertex_b: tuple[float, float]) -> float:
    return round(sqrt((vertex_a[0] - vertex_b[0]) ** 2 + (vertex_a[1] - vertex_b[1]) ** 2), 2)


class GraphCreator:
    def __init__(self, field: Field):
        self._graph = nx.Graph()
        self._field = field
        self._start = self._field.start.to_tuple()
        self._end = self._field.end.to_tuple()
        self._polygons = None
        self._polygons_center = None
        self._short_path = None

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
        else:
            logging.warning('invalid graph type (naive or optimal')
            raise ValueError('invalid graph type (naive or optimal')

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
                new_convex = [_ for _ in new_convex['coordinates'][0]]  # convert to list of tuple [(x,y),(x,y)...]
                self._polygons.append(new_convex)
                self._polygons.remove(poly_a)
                self._polygons.remove(poly_b)
                self._union_not_convex
                return
        return

    @property
    def _naive_graph(self) -> nx.Graph:
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

        return self._graph

    def _add_edge_to_graph(self, vertex_a: tuple[float, float], vertex_b: tuple[float, float]) -> bool:
        """
        add edge  between 2 points if it is OK.
        """
        no_cross = True  # True - it is possible to connect
        for p in self._polygons:
            if line_crosses_convex_shape(vertex_a, vertex_b, p):
                no_cross = False  # False - Not possible to connect
                break
        if no_cross:
            weight = distance(vertex_a, vertex_b)
            self._graph.add_edge(vertex_a, vertex_b, weight=weight)
            return True
        return False

    @property
    def _optimal_graph(self) -> None:
        """
        create optimal graph (using recursive function - self._rec_optimal_graph
        """

        for p in self._polygons:
            polygon = Polygon(p)
            if (polygon.contains(shapely.geometry.Point(self._start))) or (polygon.contains(shapely.geometry.Point(self._end))):
                logging.debug('No optimal solution')
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
                temp_a = [Point.Point(x_y=pt) for pt in poly_a]
                temp_b = [Point.Point(x_y=pt) for pt in poly_b]
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
        direct_line = True  # if it is possible to get from start_vertex to end point
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
                    _relevant_polygons[index] = distance(start_vertex, center_point)
        if not direct_line:  # there isn't direct line between start_vertex to end
            if same_polygon:
                p = self._polygons[index]
            else:
                p = self._polygons[min(_relevant_polygons, key=_relevant_polygons.get)]

            ch = get_2_points(start_vertex, self._end, p)
            connect = False
            for vertex in ch:
                if self._add_edge_to_graph(start_vertex, vertex):
                    connect = True
                    found = any(vertex == edge[0] for edge in self._graph.edges)
                    if not found:
                        self._rec_optimal_graph(vertex)
# 231 to 240 need to correct
            if not connect:
                polygon = Polygon(p)
                line = LineString([start_vertex, self._end])
                coords = list(line.intersection(polygon).coords)
                avg_vertex = coords[0]
                if self._add_edge_to_graph(start_vertex, avg_vertex):
                    inx = self._polygons.index(p)
                    self._polygons[inx].append(avg_vertex)
                    self._rec_optimal_graph(avg_vertex)

        else:  # there is direct line between start_vertex to end
            self._add_edge_to_graph(start_vertex, self._end)
            return

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
        self._short_path = nx.single_source_dijkstra(self._graph, self._start, self._end, weight='weight')
        return self._short_path[0]

    def draw_graph(self, save=False, t=0) -> None:
        pos = {point: point for point in self._graph.nodes}

        # add axis
        fig, ax = plt.subplots()
        for i, p in enumerate(self._polygons):
            polygon1 = Polygon(p)
            x, y = polygon1.exterior.xy
            plt.plot(x, y, label = i)

        # figure title
        fig.suptitle("Eskimo field", fontsize=15)

        nx.draw(self._graph, pos=pos, node_size=15, ax=ax)  # draw nodes and edges
        # nx.draw_networkx_labels(self._graph, pos=pos)  # draw node labels/names

        # draw edge weights
        # labels = nx.get_edge_attributes(self._graph, 'weight')
        # nx.draw_networkx_edge_labels(self._graph, pos=pos, edge_labels=labels, ax=ax)

        # plot START + END point
        ax.scatter(self._start[0], self._start[1], color="blue", marker="p", s=50, label="Start")
        ax.scatter(self._end[0], self._end[1], color="red", marker="*", s=50, label="End")
        # plt.xlim(-20, 320)
        # plt.ylim(-20, 320)

        # Shortest path
        if self._short_path is not None:
            # draw path in red
            path = self._short_path[1]
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_nodes(self._graph, pos, nodelist=path, node_size=5, node_color='r', ax=ax)
            nx.draw_networkx_edges(self._graph, pos, edgelist=path_edges, width=6, alpha=0.3, edge_color='r', ax=ax)
            # Adding text
            plt.text(0, -5, 'Path length ' + str(("%.2f" % self._short_path[0])), fontsize=10,
                     bbox=dict(facecolor='red', alpha=0.5))

        # grid configurations
        plt.axis("on")
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=5)
        # ax.grid()
        # if save: plt.savefig(f'./img/img_{t}.png', transparent=False,facecolor='white')
        plt.show()
