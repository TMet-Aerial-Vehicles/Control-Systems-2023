import osmnx as ox
import networkx as nx
from shapely.geometry import LineString, Point
import pyproj

def find_detour_route(start: Waypoint, rejoin, bounding_box):
    # Project all coordinates to x,y plan
    utm_proj = pyproj.Proj(proj='utm', zone=10, ellps='WGS84')
    xy_start = utm_proj(start)

def find_route(start_coord, rejoin_coord, bbox):
    # define minimum offset boundary
    min_offset = 10  # in meters

    # create a network graph for the bounding box
    G = ox.graph_from_bbox(bbox[0], bbox[1], bbox[2], bbox[3], network_type='drive')

    # create Shapely Point objects for start and rejoin coordinates
    start_point = Point(start_coord[::-1])
    rejoin_point = Point(rejoin_coord[::-1])

    # find the nearest nodes in the graph for start and rejoin points
    start_node = ox.get_nearest_node(G, start_coord[::-1], method='euclidean')
    rejoin_node = ox.get_nearest_node(G, rejoin_coord[::-1], method='euclidean')

    # create a LineString object between start and rejoin points
    route = LineString([start_point, rejoin_point])

    # create a buffer around the bounding box to avoid crossing it
    bbox_polygon = LineString(bbox).buffer(min_offset)

    # check if the route intersects the buffer polygon
    if route.intersects(bbox_polygon):
        # find the intersection point between the route and the buffer polygon
        intersection_point = route.intersection(bbox_polygon)

        # create a LineString object for the new route
        new_route = LineString([start_point, intersection_point, rejoin_point])

        # find the shortest path between the start and rejoin nodes that does not cross the buffer polygon
        shortest_path = nx.shortest_path(G, source=start_node, target=rejoin_node, weight='length', method='dijkstra',
                                         predicate=lambda u, v, d: LineString([(G.nodes[u]['x'], G.nodes[u]['y']),
                                                                               (G.nodes[v]['x'], G.nodes[v]['y'])]).intersection(bbox_polygon).is_empty())

        # create a list of LineString objects for the shortest path
        path_lines = [LineString([(G.nodes[shortest_path[i]]['x'], G.nodes[shortest_path[i]]['y']),
                                  (G.nodes[shortest_path[i+1]]['x'], G.nodes[shortest_path[i+1]]['y'])]) for i in range(len(shortest_path)-1)]

        # concatenate the new route and the shortest path
        final_route = new_route.union(LineString(path_lines))
    else:
        # find the shortest path between the start and rejoin nodes
        shortest_path = nx.shortest_path(G, source=start_node, target=rejoin_node, weight='length', method='dijkstra')

        # create a list of LineString objects for the shortest path
        path_lines = [LineString([(G.nodes[shortest_path[i]]['x'], G.nodes[shortest_path[i]]['y']),
                                  (G.nodes[shortest_path[i+1]]['x'], G.nodes[shortest_path[i+1]]['y'])]) for i in range(len(shortest_path)-1)]

        # concatenate all the LineString objects to create the final route
        final_route = LineString(path_lines)

    return final_route, G, start_node, rejoin_node


# define starting coordinate, rejoin coordinate, and bounding box
start_coord = (-74.0059, 40.7128)
rejoin_coord = (-73.9862, 40.6934)
bbox = [(-74.0202, 40.7261), (-73.9806, 40.7261), (-73.9806, 40.7044), (-74.0202, 40.7044)]

# find the route that does not cross the bounding box
route = find_route(start_coord, rejoin_coord, bbox)

# plot the route on a map
print(route)
from shapely.geometry import Polygon, Point, LineString
poly = Polygon(self.points)
x,y = poly.exterior.coords.xy
#fig takes in entire figure while ax takes in individual plots (plt.subplots() returns figure object and array of axes)
self.fig,self.ax = plt.subplots()
self.ax.plot(x, y)
x1 = [p.x for p in route]
y1 = [p.y for p in route]
self.ax.plot(x1,y1)
self.ax.scatter(self.x,self.y)
self.ax.scatter(x1,y1)
self.ax.plot(self.rejoin[0],self.rejoin[1],'ro')
self.ax.set_aspect('equal')
plt.show()
