import itertools
from shapely.geometry import Point, LineString, Polygon, mapping
import matplotlib.pyplot as plt
from ConvexHull.ConvexHull import ConvexHull
import networkx as nx
import math
from itertools import combinations
from shapely.ops import unary_union
from FieldManager.Field import Field


def distance_2f(vertex_a, vertex_b):
    """
    return the distance between 2 vertexes

    :type vertex_a: tuple(int, int)
    :type vertex_b: tuple(int, int)
    :rtype: float("%.2f" % dis)
    """
    x_1, y_1 = vertex_a[0], vertex_a[1]
    x_2, y_2 = vertex_b[0], vertex_b[1]
    dis = math.sqrt((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2)
    return float("%.2f" % dis)


def centroid(vertexes):
    _x_list = [vertex[0] for vertex in vertexes]
    _y_list = [vertex[1] for vertex in vertexes]
    _len = len(vertexes)
    _x = sum(_x_list) / _len
    _y = sum(_y_list) / _len
    return (_x, _y)


def line_crosses_convex_shape(start_point, end_point, convex_shape):
    """
    Check if a line between start_point and end_point crosses a convex_shape.
    return True if the line crosses the shape, False otherwise.

    :type start_point: tuple(int, int)
    :type end_point: tuple(int, int)
    :type convex_shape: List(tuple(int, int),tuple(int, int),...]
    :rtype: bool
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
    # return line.intersects(polygon)


def get_2_points(vertex_a, vertex_b, convex_shape):
    """
    this function do convex hull for exist convex shape, with 2 points.
    return - the 2 neighbors points to vertex_a.

    :type vertex_a: tuple(int, int)
    :type vertex_b: tuple(int, int)
    :type convex_shape: List(tuple(int, int),tuple(int, int),...]
    :rtype: (tuple(int, int), tuple(int, int))
    """

    new_convex = ConvexHull(convex_shape + [vertex_a, vertex_b]).graham_scan()
    start_index = new_convex.index(vertex_a)

    # return the neighbors to the start point

    if start_index == len(new_convex) - 1:
        before = (start_index - 1) % len(new_convex)
        after = (start_index + 1) % len(new_convex)
        return new_convex[before], new_convex[after]

    return new_convex[start_index - 1], new_convex[start_index + 1]


class GraphCreator:
    def __init__(self, field):
        self._graph = nx.Graph()
        self._start = field.start
        self._end = field.end
        self._real_polygons = field.polygons
        self._polygons = [_ for _ in self._real_polygons]
        self._polygons_center = self._polygons_center_calc()

    def _union_convex(self):
        """
        union crosses convexes shape to new convex shape - relevant to optimal solution.

        :rtype: None
        """
        pair_polygons = itertools.combinations(self._polygons, 2)
        for pair in pair_polygons:
            if Polygon(pair[0]).intersects(Polygon(pair[1])):
                new_convex = ConvexHull(pair[0] + pair[1]).graham_scan()
                self._polygons.append(new_convex)
                self._polygons.remove(pair[0])
                self._polygons.remove(pair[1])
                self._union_convex()
                return
        return

    def _union_not_convex(self):
        """
        union crosses convexes shape to new NOT convex shape - relevant only for naive solution.

        :rtype: None
        """
        pair_polygons = itertools.combinations(self._polygons, 2)
        for pair in pair_polygons:
            polygon1 = Polygon(pair[0])
            polygon2 = Polygon(pair[1])
            if polygon1.intersects(polygon2):
                new_convex = unary_union([polygon1, polygon2])
                #new_convex = cascaded_union([polygon1, polygon2])
                new_convex = mapping(new_convex)
                new_convex = [_ for _ in new_convex['coordinates'][0]]  # convert to list of tuple [(x,y),(x,y),(x,
                # y)...]
                self._polygons.append(new_convex)
                self._polygons.remove(pair[0])
                self._polygons.remove(pair[1])
                self._union_not_convex()
                return
        return

    def naive_graph(self):
        """
        create a naive graph.
        points = start, end, all convex dots
        create edge only if the edge not cross anything

        :rtype: nx Graph
        """
        self._graph = nx.Graph()
        self._union_not_convex()
        # all points in one list
        all_points = [self._start, self._end]
        for i in self._polygons:
            for j in i:
                all_points.append(j)

        # Get all combinations of points - no return
        comb = combinations(all_points, 2)

        # for each pair, check if it possible to create edge
        for pair in list(comb):
            vertex_a = pair[0]
            vertex_b = pair[1]
            self._add_edge_to_graph(vertex_a, vertex_b)

        return self._graph

    def _add_edge_to_graph(self, vertex_a, vertex_b):
        """
        add edge  between 2 points if its OK.
        :type end_point: tuple(int, int)
        :type end_point: tuple(int, int)
        :rtype: None
        """

        no_cross = True  # True - it is possible to connect
        for p in self._polygons:
            if line_crosses_convex_shape(vertex_a, vertex_b, p):
                no_cross = False  # False - Not possible to connect
                break

        if no_cross:
            weight = distance_2f(vertex_a, vertex_b)
            #print("new line", vertex_a, vertex_b)
            self._graph.add_edge(vertex_a, vertex_b, weight=weight)
            # self.draw_graph()

    def optimal_graph(self):
        """
        create optimal graph (using recrsive function - self._rec_optimal_graph
        """
        self._graph = nx.Graph()
        self._union_convex()
        self._rec_optimal_graph(self._start)

    def _rec_optimal_graph(self, start_vertex):
        """
        create optimal graph recursively.
        only vertexes in the relevant direction.

        :type start_vertex: tuple(int, int)
        :rtype: None
        """

        direct_line = True  # if it possible to get from start_vertex to end point

        #if (start_vertex, self._end) in self._graph.edges:
         #  return

        _relevant_polygons = dict()

        for index, polygon in enumerate(self._polygons):
            if line_crosses_convex_shape(start_vertex, self._end, polygon):
                direct_line = False
                _relevant_polygons[index] = distance_2f(start_vertex, self._polygons_center[index])

        if not direct_line:

            p = self._polygons[min(_relevant_polygons, key=_relevant_polygons.get)]
            ch = get_2_points(start_vertex, self._end, p)
            for vertex in ch:
                self._add_edge_to_graph(start_vertex, vertex)
                found = any(vertex == tup[0] for tup in self._graph.edges)
                if not found:
                    self._rec_optimal_graph(vertex)
        else:
            self._add_edge_to_graph(start_vertex, self._end)
            return

    def _polygons_center_calc(self):
        """
        return dictionary with the center of the polygons

        :rtype: Dict
        """
        polygons_dict = dict()
        for index, polygon in enumerate(self._polygons):
            polygons_dict[index] = centroid(polygon)
        return polygons_dict

    def calc_graph(self):
        try:
            self.optimal_graph()
        except Exception as e:
            print("Error: An unexpected error occurred -", e)
        else:
            self._polygons = [_ for _ in self._real_polygons]
            self.naive_graph()

    def draw_graph(self):
        pos = {point: point for point in self._graph.nodes}

        # add axis
        fig, ax = plt.subplots()
        for p in self._polygons:
            polygon1 = Polygon(p)
            x, y = polygon1.exterior.xy
            plt.plot(x, y)
        # figure title
        fig.suptitle("Eskimo field", fontsize=15)

        nx.draw(self._graph, pos=pos, node_size=15, ax=ax)  # draw nodes and edges
        # nx.draw_networkx_labels(self._graph, pos=pos)  # draw node labels/names
        # draw edge weights
        # labels = nx.get_edge_attributes(self._graph, 'weight')
        # nx.draw_networkx_edge_labels(self._graph, pos=pos, edge_labels=labels, ax=ax)
        plt.axis("on")
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)

        # plot START + END point
        ax.scatter(self._start[0], self._start[1], color="blue", marker="p", s=50, label="Start")
        ax.scatter(self._end[0], self._end[1], color="red", marker="*", s=50, label="End")

        # grid configurations
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=5)
        ax.grid()
        plt.show()
