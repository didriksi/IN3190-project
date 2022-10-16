"""Module with functions to make the plots necessary for the report.
"""
import cartopy.crs as ccrs
import matplotlib
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


def create_figure(nrows=1, ncols=1, height=4, axes_dict=None, title=None):
    """Create a figure and one ore more axes.

    Mainly used as a soft alias for plt.subplots to be able to make figures in
    the main.py file one abstraction level up from matplotlib.

    Arguments:
        nrows: Number of rows to make axes for. 1 by default.
        ncols: Number of columns to make axes for. 1 by default.
        height: Height of the plot. Used together with a width of 7. 4 by default.
        axes_dict: Keywords to set each created Axes object with. None by default
                   meaning nothing is done to them.
        title: Suptitle of the figure. None by default meaning no title is set.

    Return:
        Matplotlib Figure object, and either an array of Axes or a single Axes
        object.
    """
    fig, axs = plt.subplots(nrows, ncols, figsize=(7, height))

    if title is not None:
        fig.suptitle(title)

    if axes_dict is not None:
        axs_iter = [axs] if isinstance(axs, matplotlib.Axes) else axs.flat
        for ax in axs_iter:
            ax.set(**axes_dict)
    return fig, axs


def input_response(fir, fir_label=None, filename=None):
    """Plot the filtered input response (FIR).

    Arguments:
        fir: Array with the filter input response(s). If either iterable of
             1-d arrays, or a 2-d array, several plots are made.
        fir_label: Either a single string or a list of strings with labels for
                   the response or responses. None by default, meaning no label
                   is given.
        filename: Path to location to save resulting image in. If None, as 
                  default, it isn't saved just shown.
    """
    if isinstance(fir, np.ndarray) and fir.ndims == 1:
        fir = [fir]
        fir_label = fir_label if (fir_label is None) else [fir_label]

    fig, ax = plt.subplots(1, 1, figsize=(7, 4))

    for i, single_fir in enumerate(fir):
        if fir_label is not None:
            ax.plot(single_fir, label=fir_label[i])
        else:
            ax.plot(single_fir)

    fig.suptitle("Filter input responses (FIR)")
    ax.set_xlabel("$n$")
    ax.set_ylabel("$h$")
    plt.legend()

    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)
        plt.close()
