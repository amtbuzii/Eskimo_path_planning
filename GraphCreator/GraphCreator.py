from shapely.geometry import Point, LineString, Polygon
import matplotlib.pyplot as plt
from ConvexHull.ConvexHull import ConvexHull
import networkx as nx
import math
from itertools import combinations


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
    if start_point in convex_shape and end_point in convex_shape:
        return True

    # convert the convex shape to a Shapely polygon
    polygon = Polygon(convex_shape)

    # create a Shapely LineString from the start and end points
    line = LineString([start_point, end_point])

    # check if the line intersects the polygon
    return line.crosses(polygon)


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
    def __init__(self, start, end, polygons):
        self._graph = nx.Graph()
        self._start = start
        self._end = end
        self._polygons = polygons

    def naive_graph(self):
        """
        create a naive graph.
        points = start, end, all convex dots
        create edge only if the edge not cross anything

        :rtype: nx Graph
        """
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

        no_cross = True                     # True - it is possible to connect
        for p in self._polygons:
            if line_crosses_convex_shape(vertex_a, vertex_b, p):
                no_cross = False            # False - Not possible to connect
                break

        if no_cross:
            weight = distance_2f(vertex_a, vertex_b)
            self._graph.add_edge(vertex_a, vertex_b, weight=weight)



    def optimal_graph(self, start_vertex):
        """
        create optimal graph
        only vertexes in the relevent direction
        """

        direct_line = True # if it possible to get from start_vertex to end point
        for p in self._polygons:
            polygon1 = Polygon(p)
            if line_crosses_convex_shape(start_vertex, self._end, p):
                #print("start", start, "end", end)
                #print("no dir")
                direct_line = False
                ch = get_2_points(start_vertex, self._end, p)
                for vertex in ch:
                    self._add_edge_to_graph(start_vertex, vertex)
                    # draw_grpah(graph)
                    # plt.show()
                    self.optimal_graph(vertex)
        if direct_line:
            #print("directLine")
            self._add_edge_to_graph(start_vertex, self._end)
            # draw_grpah(graph)

    def draw_graph(self):
        pos = {point: point for point in self._graph.nodes}

        # add axis
        fig, ax = plt.subplots()

        for p in self._polygons:
            polygon1 = Polygon(p)
            x, y = polygon1.exterior.xy
            plt.plot(x, y)

        nx.draw(self._graph, pos=pos, node_size=15, ax=ax)  # draw nodes and edges
        #nx.draw_networkx_labels(self._graph, pos=pos)  # draw node labels/names
        # draw edge weights
        #labels = nx.get_edge_attributes(self._graph, 'weight')
        #nx.draw_networkx_edge_labels(self._graph, pos=pos, edge_labels=labels, ax=ax)
        plt.axis("on")
        # ax.set_xlim(0, 11)
        # ax.set_ylim(0, 11)
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)

        # plot START + END point
        plt.scatter(self._start[0], self._start[1], color="blue", s=10)
        plt.text(self._start[0] - 8, self._start[1] + 5, "Start")
        plt.scatter(self._end[0], self._end[1], color="red", s=10)
        plt.text(self._end[0] - 8, self._end[1] + 5, "End")

        plt.show()



