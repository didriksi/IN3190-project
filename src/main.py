import os
import sys
import argparse

import numpy as np

import constants
import process_data
import plot
import signal_processing


def parse_arguments(argv=None):
    """Parse all the arguments given to the module.
    """
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()

    parser.add_argument("--parse-data", action="store_true",
                        help="Load the data, and make derivative files from it"\
                             " that is easier to read and use.")
    parser.add_argument("--plot-map", action="store_true",
                        help="Plot a map of all the locations measurements "\
                             "were made.")
    parser.add_argument("--plot-distances", action="store_true",
                        help="Get the distances between all the stations and "\
                             "Hunga Tonga.")
    parser.add_argument("--plot-fir", action="store_true",
                        help="Plot the three given filter input responses, "\
                             "h1, h2 and h3.")
    parser.add_argument("--plot-freq-spec", action="store_true",
                        help="Plot the absolute values of the frequency "\
                             "spectrums from h1, h2 and h3.")

    return parser.parse_args(argv)


def main():
    processed_data_filename = os.path.join(constants.ROOT_DIR, "data",
                                           "processed", "processed.npz")
    args = parse_arguments()
    if args.parse_data:
        process_data.process_data()
    if args.plot_map:
        data = np.load(processed_data_filename)
        lats, lons = data["lats"], data["lons"]
        stations_coordinates = np.concatenate((lats[:, np.newaxis],
                                               lons[:, np.newaxis]),
                                              axis=1)
        plot.geography(constants.TONGA_COORDINATES, stations_coordinates, 
                       os.path.join(constants.PLOTS_DIR, "map.pdf"))
    if args.plot_distances:
        data = np.load(processed_data_filename)
        distances = data["distances"]
        plot.distances(distances,
                       os.path.join(constants.PLOTS_DIR, "distances.pdf"))
    if args.plot_fir:
        plot.input_response([constants.h1, constants.h2, constants.h3],
                            ["$h_1$", "$h_2$", "$h_3$"],
                            os.path.join(constants.PLOTS_DIR, "fir.pdf"))
    if args.plot_freq_spec:
        plot.frequency_spectrum([constants.h1, constants.h2, constants.h3],
                                ["$H_1$", "$H_2$", "$H_3$"], side_by_side=True,
                                filename=os.path.join(constants.PLOTS_DIR, "freq_spec.pdf"))

if __name__ == "__main__":
    main()
