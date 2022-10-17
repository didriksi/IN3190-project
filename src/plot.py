"""Module with functions to make the plots necessary for the report.
"""
import cartopy.crs as ccrs
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime

import signal_processing

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
    
    ax.set_xticks([])
    ax.set_yticks([])
    
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


def frequency_spectrum(fir, fir_label=None, side_by_side=False, filename=None):
    """Plot the DTFT-transformations of filtered input response (FIR).

    Arguments:
        fir: Array with the filter input response(s). If either iterable of
             1-d arrays, or a 2-d array, several plots are made.
        title: Title of plot. 'Filter input responses (FIR)' by default.
        fir_label: Either a single string or a list of strings with labels for
                   the response or responses. None by default, meaning no label
                   is given.
        side_by_side: Boolean indicating whether to plot all the results in the
                      different axes side by side or in the same (False, default).
        filename: Path to location to save resulting image in. If None, as 
                  default, it isn't saved just shown.
        
    """
    if isinstance(fir, np.ndarray) and fir.ndims == 1:
        fir = [fir]
        fir_label = fir_label if (fir_label is None) else [fir_label]

    dtft_fir = map(lambda h: np.abs(signal_processing.dtft(h, fs=0.1)[1]), fir)

    fig, axs = plt.subplots(1, 1 if not side_by_side else len(fir),
                            figsize=(7, 4), sharey=side_by_side)
    axs_iter = [axs]*len(fir) if isinstance(axs, matplotlib.axes.Axes) else axs.flat

    for i, (single_dtft_fir, ax) in enumerate(zip(dtft_fir, axs_iter)):
        if fir_label is not None:
            if side_by_side:
                ax.plot(*single_dtft_fir)
                ax.set_title(fir_label[i])
            else:
                ax.plot(*single_dtft_fir, label=fir_label[i])
                ax.legend()
        else:
            ax.plot(*single_dtft_fir)

        ax.set_xlabel("$Hz$")

    axs_iter[0].set_ylabel("$|H(e^{j \\omega})|$")

    fig.suptitle("Absolute values of the frequency spectrums of the FIRs")

    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)
        plt.close()


def sections(signal_filenames, times, distances, plot_filename=None):
    """Plot many signals from many different files, all transformed by filter 3.

    Arguments:  
        signal_filenames: Paths to numpy files with arrays for each signal.
        times: 2-d array giving the times of each of the measurements.
        distances: 1-d array stating how far away from Hunga Tunga each signal is
                   from.
        plot_filename: Path to location to save resulting image in. If None, as 
                       default, it isn't saved just shown.
    """
    fig, ax = plt.subplots(1, 1, figsize=(7, 4))
    
    max_distance = np.max(distances)
    for i, (signal_filename, _times, distance) in enumerate(zip(signal_filenames, times, distances)):
        y = np.abs(np.load(signal_filename))
        # Remove measurements from before the event
        keep_inds = _times > 4.92e06
        scaled_y = (max_distance/100 * y[keep_inds]/max(1, np.max(y)) + distance)/1000
        ax.plot(_times[keep_inds], scaled_y, color="black", alpha=0.7, linewidth=0.2)

    ticks = np.linspace(np.min(times[0]), np.max(times[0]), 8)
    ticklabels = [datetime.datetime.fromtimestamp(tick).strftime("%H:%M") for tick in ticks]
    ax.set_xticks(ticks, labels=ticklabels)
    ax.set_xlabel("Time")
    ax.set_ylabel("Distance (km)")

    if plot_filename is None:
        plt.show()
    else:
        plt.savefig(plot_filename)
        plt.close()


def mark_arrival_time(station_id, signal_times, **signals):
    """Use pyplot.ginput to mark the arrival time of the wave at a station.

    Opens a plot, and lets the user click once to mark the arrival time of the
    infrasound wave.

    Arguments:
        station_id: Index of the station to plot for
        signal_times: 1-d slice of the 'times'-array in the processed data 
                      npz-file
        **signals: Named 1-d slice of the 'data'-array in the processed data
                   npz-file, or processed versions of it.

    Return:
        Float indicating the arrival time estimated by the user.
    """
    fig, axs = plt.subplots(2, int(np.ceil(len(signals)/2)), figsize=(12, 7))

    fig.suptitle(f"Station number {station_id}")

    for ax, (signal_name, signal) in zip(axs.flat, signals.items()):
        ax.plot(signal_times, signal)
        ax.fill_between([signal_times[0], signal_times[-1]], 0, np.max(signal), color="xkcd:light green", alpha=0.4)
        ax.fill_between([signal_times[0], signal_times[-1]], np.min(signal), 0, color="xkcd:burnt orange", alpha=0.4)
        ax.set_title(signal_name)

    arrival_time, height = plt.ginput()[0]
    plt.close()
    validness = 1 if height > 0 else height/np.max(np.abs(signal))
    return arrival_time, validness


def arrival_time_vs_distance(distances, arrival_times, alphas=None,
                             polynomial=None, filename=None):
    """Plot the arrival time of the signal against distance.

    Arguments:
        distances: Array of distances between Hunga Tunga and the stations, given
                   in meters.
        arrival_times: Manually marked times of arrival of the infrasound wave 
                       at each station, given in seconds since the UNIX epoch.
        alphas: Optional array that gives a sort of weight to the markings.
                   1 means it is completely valid, 0 means it is completely 
                   invalid, while values in between denote some estimated 
                   probability of its validity.
        polynomial: Numpy polynomial fitted to the data. None by default, meaning
                    not polynomial is plotted.
        filename: Path to location to save resulting image in. If None, as 
                  default, it isn't saved just shown.
    """
    fig, ax = plt.subplots(1, 1, figsize=(7, 4))
    fig.suptitle("Arrival times for different stations. Alpha denotes confidence in label")

    colors = (np.array([117, 187, 253, 1])/256)[np.newaxis,:].repeat(len(distances), axis=0)
    if alphas is not None:
        colors[:,3] = alphas
    
    if polynomial is not None:
        label = "$" + " + ".join([f"{coef:.4g} \\cdot x^{i}" for i, coef in enumerate(polynomial.convert().coef)]) +  "$"
        ax.plot(arrival_times, polynomial(arrival_times), label=label)

    ax.scatter(arrival_times, distances, c=colors)

    ticks = np.linspace(np.min(arrival_times), np.max(arrival_times), 8)
    ticklabels = [datetime.datetime.fromtimestamp(tick).strftime("%H:%M") for tick in ticks]
    ax.set_xticks(ticks, labels=ticklabels)
    ax.set_xlabel("Time")
    ax.set_ylabel("Distance (km)")
    plt.legend()

    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)
        plt.close()
