"""Module with functions to make the plots necessary for the report.
"""
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np

def geography(center_coordinates, other_coordinates, filename=None):
    """Plot a map of the world with some coordinates marked.

    Arguments:
        center_coordinates: Tuple with two floats, the latitude and longitude
                            of the location to put in the center of the map.
        other_coordinates: 2D arraylike with coordinates to mark.
        filename: Path to location to save resulting image in. If None, as 
                  default, it isn't saved just shown.
    """
    projection = ccrs.AzimuthalEquidistant(*reversed(center_coordinates))
    ax = plt.axes(projection=projection)
    ax.stock_img()
    
    ax.scatter(other_coordinates[1,:], other_coordinates[0,:], s=20, color="xkcd:bright blue")
    ax.scatter([center_coordinates[0]], [center_coordinates[1]], marker="^", s=50, color="xkcd:brick red")
    
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)
        plt.close()
