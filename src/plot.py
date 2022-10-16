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
    fig, ax = plt.subplots(1, 1, figsize=(7, 4))
    
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


def distances(distance_array, filename=None):
    """Plot out sorted distances.

    Arguments:
        distance_array: Array with all distances between stations and Hunga
                        Tunga.
        filename: Path to location to save resulting image in. If None, as 
                  default, it isn't saved just shown.
    """
    sorted_inds = np.argsort(distance_array)
    closest = distance_array[sorted_inds[0]]/1000
    farthest = distance_array[sorted_inds[-1]]/1000

    fig, ax = plt.subplots(1, 1, figsize=(7, 4))
    ax.plot(distance_array[sorted_inds]/1000)
    fig.suptitle("Distances between Hunga Tunga and stations")
    ax.set_ylabel("kilometers")
    ax.set_xticks([])
    ax.set_xlabel("Different stations, sorted by distance")
    ax.scatter([0], [closest],
               label=f"Closest station ({int(closest)}km)")
    ax.scatter([len(distance_array)], [farthest],
               label=f"Farthest station ({int(farthest)}km)")
    plt.legend()
    
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)
        plt.close()


