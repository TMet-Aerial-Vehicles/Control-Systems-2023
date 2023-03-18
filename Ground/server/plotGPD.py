import geopandas as gpd
from pyproj import CRS
from route_diversion import route
import matplotlib.pyplot as plt
#the purpose of this function is to plot the generated route using geopandas
def plot(evasion_route):
    rout = gpd.GeoDataFrame(geometry=evasion_route.finalRoute, crs='EPSG:4326')

    # Read in a world map shapefile using GeoPandas
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Project the route GeoDataFrame to the same CRS as the world map
    rout = rout.to_crs(world.crs)
    fig, ax = plt.subplots(figsize=(12,6))
    world.plot(ax=ax, facecolor='lightgray', edgecolor='white')
    rout.plot(ax=ax, marker='o', color='red', markersize=5)
    ax.set_title('Route Points on World Map')
    plt.show()
    