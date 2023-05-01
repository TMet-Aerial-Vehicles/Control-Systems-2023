from shapely.geometry import LineString, Point, Polygon
from typing import List
import pyproj
import networkx as nx
import matplotlib.pyplot as plt

from Ground.server.waypoint import Waypoint

BUFFER_DISTANCE = 25


def get_detour_route(start: Waypoint, rejoin: Waypoint,
                     bounding_box: List[Waypoint],
                     create_plot=False) -> List[Waypoint]:
    """
    Returns a list of intermediate waypoints to visit to reach rejoin waypoint
    and circumvent the bounding box
    Args:
        start: starting waypoint
        rejoin: ending waypoint
        bounding_box: list of waypoints to avoid
        create_plot: whether to plot a graph of the bounding box and detour
    Returns: list of intermediate waypoints
    """
    # Project all coordinates to x,y plan
    ll_to_m_proj = pyproj.Proj(proj='utm', zone=10, ellps='WGS84')
    xy_start = Point(ll_to_m_proj(start.longitude, start.latitude))
    xy_rejoin = Point(ll_to_m_proj(rejoin.longitude, rejoin.latitude))
    xy_bbox = []
    for waypoint in bounding_box:
        xy_bbox.append(ll_to_m_proj(waypoint.longitude, waypoint.latitude))

    # Set up Polygon bounding box using convex hull of points
    original_bbox = Polygon(xy_bbox)
    bb_poly = original_bbox.convex_hull

    # Add buffer distance with tolerance to polygon
    bb_poly_buff_no_tol = bb_poly.buffer(BUFFER_DISTANCE, join_style=2)
    bb_poly_buffer = bb_poly_buff_no_tol.buffer(1, join_style=2)

    if create_plot:
        plt.plot(*original_bbox.exterior.xy, "xr-")
        plt.plot(*xy_start.xy, "og-")
        plt.plot(*xy_rejoin.xy, ">m-")

        plt.plot(*bb_poly.exterior.xy, "purple")  # Convex hull of original bbox
        plt.plot(*bb_poly_buff_no_tol.exterior.xy, "black")
        plt.plot(*bb_poly_buffer.exterior.xy, "blue")

    # Create a LineString from the start and rejoin coordinates
    route = LineString([xy_start, xy_rejoin])

    # Check if the route intersects with the buffer polygon
    if route.intersects(bb_poly_buffer):
        # Create a graph with the starting, rejoin, bounding box nodes
        graph = nx.Graph()
        nodes = list(bb_poly_buffer.exterior.coords)
        nodes.append((xy_start.x, xy_start.y))
        nodes.append((xy_rejoin.x, xy_rejoin.y))
        for node in nodes:
            graph.add_node(node)

        # Add edges between nodes that do not intersect the buffer polygon
        for u in graph.nodes:
            for v in graph.nodes:
                edge = LineString([u, v])
                if edge.length > 0 and not edge.intersects(bb_poly_buff_no_tol):
                    graph.add_edge(u, v, weight=edge.length)

        # Find the shortest path between the start and rejoin nodes using Graph
        detour_xy_path = []
        try:
            detour_xy_path = nx.shortest_path(graph,
                                              source=(xy_start.x, xy_start.y),
                                              target=(xy_rejoin.x, xy_rejoin.y),
                                              weight='weight')
            print("Detour Path Found")

            if create_plot:
                x_coords = [coord[0] for coord in detour_xy_path]
                y_coords = [coord[1] for coord in detour_xy_path]
                plt.plot(x_coords, y_coords, "xg-")

            # Filter out starting and rejoin coordinate
            detour_xy_path = detour_xy_path[1:-1]
        except Exception as e:
            # If no valid path is found, return None
            print("NO DETOUR FOUND")
            print(e)
    else:
        # Return the Rejoin point if no intersection with bounding box
        print("No Detour Needed")
        if create_plot:
            plt.savefig("detourRoute.jpg")
            plt.show()
        return [rejoin]

    if create_plot:
        plt.savefig("detourRoute.jpg")
        plt.show()

    # Convert detour routes back to longitude, latitude
    xy_zone = pyproj.CRS(proj='utm', zone=10, ellps='WGS84')
    ll_proj = pyproj.CRS('epsg:4326')
    xy_to_ll_transformer = pyproj.Transformer.from_crs(xy_zone, ll_proj)

    detour_route = []
    inter_wp_num = 1
    for coordinate in detour_xy_path:
        detour_lat, detour_lon = xy_to_ll_transformer.transform(coordinate[0],
                                                                coordinate[1])
        detour_route.append(
            Waypoint(name=f"InterNode {inter_wp_num}",
                     number=(50 + inter_wp_num),
                     longitude=detour_lon,
                     latitude=detour_lat))
        inter_wp_num += 1

    print("Detour Intermediate Waypoints: ", detour_route)
    return detour_route
