import osmnx as ox
import networkx as nx
from shapely.geometry import LineString, Point, Polygon
from typing import List

def find_route_no_cross(start_coord: tuple, rejoin_coord: tuple, bounding_box: List[tuple]) -> List[tuple]:
    # Define a buffer around the bounding box with a minimum offset boundary of 15m
    bb_poly = Polygon(bounding_box)
    buffer_size = 0.00015  # degrees of latitude/longitude, approximately 15m at the equator
    bb_buffer = bb_poly.buffer(buffer_size)

    # Download the street network within the bounding box
    G = ox.graph_from_polygon(bb_poly, network_type='drive')

    # Find the nearest network nodes to the starting and rejoin coordinates
    start_node = ox.get_nearest_node(G, start_coord)
    rejoin_node = ox.get_nearest_node(G, rejoin_coord)

    # Find the shortest path between the starting and rejoin nodes that does not cross the bounding box
    path_edges = []
    try:
        path = nx.shortest_path(G, start_node, rejoin_node, weight='length')
        path_coords = ox.utils_graph.get_route_edge_attributes(G, path, 'geometry')
        for i in range(len(path_coords)-1):
            edge = LineString([path_coords[i], path_coords[i+1]])
            if not edge.crosses(bb_buffer):
                path_edges.append((path[i], path[i+1]))
            else:
                break
    except nx.NetworkXNoPath:
        print("No route found.")

    # Return the coordinates of the path
    path_coords = [start_coord]
    for edge in path_edges:
        edge_coords = G.edges[edge]['geometry'].coords
        path_coords.extend(edge_coords)
    path_coords.append(rejoin_coord)

    return path_coords
