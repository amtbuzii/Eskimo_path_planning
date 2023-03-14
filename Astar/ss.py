from shapely.geometry import Point, LineString, Polygon
import matplotlib.pyplot as plt
from ConvexHull.ConvexHull import ConvexHull
import networkx as nx
import math
from itertools import combinations


def line_crosses_convex_shape(start_point, end_point, convex_shape):
    """
    Check if a line between start_point and end_point crosses a convex_shape.
    return True if the line crosses the shape, False otherwise.

    :type start_point: tuple(int, int)
    :type end_point: tuple(int, int)
    :type convex_shape: List(tuple(int, int),tuple(int, int),...]
    :rtype: bool
    """

    # convert the convex shape to a Shapely polygon
    polygon = Polygon(convex_shape)

    # create a Shapely LineString from the start and end points
    line = LineString([start_point, end_point])

    # check if the line intersects the polygon
    return line.crosses(polygon)


def get_2_points(start_point, end_point, convex_shape):
    """
    this function do convex hull for exist convex shape, with 2 pionts.
    return - the 2 neighbors points to start point.

    :type start_point: tuple(int, int)
    :type end_point: tuple(int, int)
    :type convex_shape: List(tuple(int, int),tuple(int, int),...]
    :rtype: bool
    """
    new_convex = ConvexHull(convex_shape + [start_point, end_point]).graham_scan()
    start_index = new_convex.index(start_point)

    # return the neighbors to the start point

    if start_index == len(new_convex)-1:
        befor = (start_index - 1) % len(new_convex)
        after = (start_index + 1) % len(new_convex)
        return new_convex[befor], new_convex[after]

    return new_convex[start_index-1], new_convex[start_index+1]


def add_edge_to_graph(graph, vertex_a, vertex_b, polygons):
    # (v1,v2, weight)
    flag = True
    for p in polygons:
        if line_crosses_convex_shape(vertex_a, vertex_b, p):
            flag = False
            break
    if flag:
        weight = distance(vertex_a, vertex_b)
        graph.add_edge(vertex_a, vertex_b, weight=weight)

def distance(vertex_a, vertex_b):
    x_1, y_1 = vertex_a[0], vertex_a[1]
    x_2, y_2 = vertex_b[0], vertex_b[1]
    dis = math.sqrt((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2)
    return float("%.2f" % dis)

def create_graph(graph, start, end, polygons):
    direct_line = True
    for p in polygons:
        polygon1 = Polygon(p)
        if line_crosses_convex_shape(start, end, polygon1):
            print("start", start, "end", end)
            print("no dir")
            direct_line = False
            ch = get_2_points(start, end, p)
            for vertex in ch:
                add_edge_to_graph(graph, start, vertex, distance(start, vertex),polygons)
                #draw_grpah(graph)
                #plt.show()
                create_graph(graph, vertex, end, polygons)
    if direct_line:
        print("directLine")
        add_edge_to_graph(graph, start, end, distance(start, end),polygons)
        #draw_grpah(graph)


def draw_grpah(G):
    pos = {point: point for point in G.nodes}

    # add axis
    fig, ax = plt.subplots()

    for p in polygons:
        polygon1 = Polygon(p)
        x, y = polygon1.exterior.xy
        plt.plot(x, y)

    nx.draw(G, pos=pos, node_size=15, ax=ax)  # draw nodes and edges
    nx.draw_networkx_labels(G, pos=pos)  # draw node labels/names
    # draw edge weights
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=labels, ax=ax)
    plt.axis("on")
    #ax.set_xlim(0, 11)
    #ax.set_ylim(0, 11)
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.show()
def naive_graph(graph, start, end, polygons):
    all_points = [start, end]
    for i in polygons:
        for j in i:
            all_points.append(j)
    # Get all combinations of points - no return
    comb = combinations(all_points, 2)
    for pair in list(comb):
        vertex_a = pair[0]
        vertex_b = pair[1]
        add_edge_to_graph(graph, vertex_a, vertex_b, polygons)


# initialize graph
my_graph = nx.Graph()
start = (0, 0)
end = (20, 20)
polygons = [[(1, 3), (1, 1), (3, 0)], [(4, 8), (5, 4), (6, 9)], [(0, 15), (1, 16), (20, 17)]]



naive_graph(my_graph, start, end, polygons)
#create_graph(my_graph, start, end, polygons)
draw_grpah(my_graph)
plt.show()



