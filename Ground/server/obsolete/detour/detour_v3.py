import osmnx as ox
import networkx as nx
import sklearn
from shapely.geometry import LineString, Point, Polygon
import matplotlib.pyplot as plt
from typing import List

def find_route_no_cross(start_coord: tuple, rejoin_coord: tuple, bounding_box: List[tuple]) -> List[tuple]:
    # Define a buffer around the bounding box with a minimum offset boundary of 15m
    bb_poly = Polygon(bounding_box)
    buffer_size = 0.00015  # degrees of latitude/longitude, approximately 15m at the equator
    bb_buffer = bb_poly.buffer(buffer_size)

    # Download the street network within the bounding box
    G = ox.graph_from_polygon(bb_poly, network_type='drive')

    # Find the nearest network nodes to the starting and rejoin coordinates
    start_node = ox.distance.nearest_nodes(G, start_coord[1], start_coord[0])
    rejoin_node = ox.distance.nearest_nodes(G, rejoin_coord[1], rejoin_coord[0])

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

# define starting coordinate, rejoin coordinate, and bounding box
start_coord = (-71.639107, 48.508981)
rejoin_coord = (-71.626592, 48.504977)
bbox = [(-71.634186, 48.508072), (-71.629868, 48.506956), (-71.629971, 48.503998),  (-71.635331, 48.505351)]

# find the route that does not cross the bounding box
route = find_route_no_cross(start_coord, rejoin_coord, bbox)

# plot the route on a map
# def plot_route_bounding_box(start_coord: tuple, rejoin_coord: tuple, bounding_box: List[tuple]):
#     # Find the route that does not cross the bounding box
#     route = find_route_no_cross(start_coord, rejoin_coord, bounding_box)
#
#     if not route:
#         print("No valid route found.")
#         return
#
#     # Plot the bounding box and route using osmnx and matplotlib
#     bb_poly = Polygon(bounding_box)
#     G = ox.graph_from_polygon(bb_poly, network_type='drive')
#
#     if not G:
#         print("Error constructing graph.")
#         return
#
#     try:
#         fig, ax = ox.plot_graph_route(G, route, node_size=0, bbox=bb_poly.bounds, bgcolor='w')
#         ax.add_patch(plt.Polygon(bb_poly.exterior.coords[:], facecolor='none', edgecolor='red'))
#         plt.show()
#     except KeyError as e:
#         print("Error plotting route: {}".format(e))
import folium
from shapely.geometry import Polygon, LineString
from typing import List

# def plot_route_bounding_box(start_coord: tuple, rejoin_coord: tuple, bounding_box: List[tuple], margin=0.01):
#     # Find the route that does not cross the bounding box
#     route = find_route_no_cross(start_coord, rejoin_coord, bounding_box)
#
#     if not route:
#         print("No valid route found.")
#         return
#
#     # Construct the bounding box polygon and route line string
#     bb_poly = Polygon(bounding_box)
#     route_line = LineString(route)
#
#     # Determine the bounds of the map
#     map_bounds = bb_poly.buffer(margin).bounds
#
#     # Construct a folium map centered on the start coordinate
#     m = folium.Map(location=start_coord, zoom_start=12)
#
#     # Add the bounding box to the map
#     folium.GeoJson(bb_poly.__geo_interface__).add_to(m)
#
#     # Add the detour route to the map
#     folium.PolyLine(route, color='red', weight=3).add_to(m)
#
#     # Add the start and rejoin markers to the map
#     folium.Marker(start_coord, popup='Start').add_to(m)
#     folium.Marker(rejoin_coord, popup='Rejoin').add_to(m)
#
#     # Add a popup to the bounding box
#     # folium.GeoJsonPopup("Bounding Box", bb_poly.__geo_interface__).add_to(folium.GeoJson(bb_poly.__geo_interface__))
#     # folium.GeoJsonPopup(bb_poly.__geo_interface__, fields=["Bounding Box"]).add_to(folium.GeoJson(bb_poly.__geo_interface__))
#     folium.GeoJsonPopup(bb_poly.__geo_interface__, fields=["Bounding Box"]).add_to(folium.GeoJson(bb_poly.__geo_interface__))
#
#
#     # Add a popup to the detour route
#     folium.PolyLinePopup(route, "Detour Route").add_to(m)
#
#     # Add a layer control to toggle the visibility of the bounding box and route
#     folium.LayerControl().add_to(m)
#
#     # Fit the map to the bounds
#     m.fit_bounds([map_bounds[1::-1], map_bounds[3:1:-1]])
#
#     # Display the map
#     display(m)
# def plot_route_bounding_box(G, route, bb_poly):
#     # create map object
#     m = folium.Map()
#
#     # add the bounding box polygon to the map with a popup
#     folium.GeoJson(bb_poly.__geo_interface__, name="Bounding Box", show=False, popup=folium.Popup("Bounding Box")).add_to(m)
#
#     # create a feature group for the route and add it to the map
#     route_fg = folium.FeatureGroup(name="Route")
#     m.add_child(route_fg)
#
#     # add the route to the feature group
#     route_line = folium.PolyLine(locations=[(node[1], node[0]) for node in route], color="blue", weight=5, opacity=0.7)
#     route_popup = folium.Popup("Detour Route")
#     route_line.add_child(route_popup)
#     route_fg.add_child(route_line)
#
#     # add the bounding box to the feature group and fit the map to it
#     route_fg.add_child(folium.GeoJson(bb_poly.__geo_interface__))
#     m.fit_bounds(bb_poly.bounds)
#
#     # add layer control
#     folium.LayerControl().add_to(m)
#
#     return m


import folium
from shapely.geometry import Polygon, Point


def plot_detour_route_bounding_box(start, rejoin, bbox):
    # convert the bbox coordinates to a Polygon object
    bb_poly = Polygon(bbox)

    # download the street network within the bounding box
    G = ox.graph_from_polygon(bb_poly, network_type='drive')

    # get the nearest network nodes to the start and rejoin points
    start_node = ox.get_nearest_node(G, start)
    rejoin_node = ox.get_nearest_node(G, rejoin)

    # find the detour route between the start and rejoin nodes, avoiding the bounding box
    detour_route = ox.shortest_path(G, start_node, rejoin_node, weight='length', nodes_matching='avoid', polygon=bb_poly, dist=15)

    # create a folium map object
    m = folium.Map(location=(start[1], start[0]), zoom_start=13, tiles='cartodbpositron')

    # add the bounding box polygon to the map with a popup
    folium.GeoJson(bb_poly.__geo_interface__, name="Bounding Box", show=False, popup=folium.Popup("Bounding Box")).add_to(m)

    # create a feature group for the detour route and add it to the map
    route_fg = folium.FeatureGroup(name="Detour Route")
    m.add_child(route_fg)

    # add the detour route to the feature group
    route_line = folium.PolyLine(locations=[(node[1], node[0]) for node in detour_route], color="blue", weight=5, opacity=0.7)
    route_popup = folium.Popup("Detour Route")
    route_line.add_child(route_popup)
    route_fg.add_child(route_line)

    # add the bounding box to the feature group and fit the map to it
    route_fg.add_child(folium.GeoJson(bb_poly.__geo_interface__))
    m.fit_bounds(bb_poly.bounds)

    # add layer control
    folium.LayerControl().add_to(m)

    return m


# plot_detour_route_bounding_box(start_coord, rejoin_coord, bbox)
import pandas as pd
data = {'longitude': [-74.0202, -73.9806, -73.9806, -74.0202], 'latitude': [40.7261, 40.7261, 40.7044, 40.7044]}
# Create DataFrame.
df = pd.DataFrame(data)
# Print the output.
print(df)

def plt_plot():
    start_coord = (-71.639107, 48.508981)
    rejoin_coord = (-71.626592, 48.504977)
    bbox = [(-71.634186, 48.508072), (-71.629868, 48.506956), (-71.635331, 48.505351), (-71.629971, 48.503998)]
    BBox = (df.longitude.min()-0.1,   df.longitude.max()+0.1,
            df.latitude.min()-0.1, df.latitude.max()+0.1)

    # Downloaded using this tutorial: https://medium.com/@abuqassim115/thanks-for-your-response-frank-fb869824ede2
    # map_img = plt.imread('map.png')

    # Plotting the points on the graph
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.plot(df.longitude, df.latitude, 'xb-')

    ax.plot(start_coord[0], start_coord[1], 'xr-')
    ax.plot(rejoin_coord[0], rejoin_coord[1], 'xr-')

    for r in route:
        ax.plot(r[0], r[1], 'xg-')

    # Setting limits for the plot
    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])

    # Showing the image behind the points
    # ax.imshow(map_img, zorder=0, extent=BBox, aspect='equal')

    plt.show()
    print(route)
plt_plot()
