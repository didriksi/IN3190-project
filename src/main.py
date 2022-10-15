import os
import sys
import argparse

import numpy as np

import constants
import process_data
import plot


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
                       os.path.join(constants.ROOT_DIR, "plots", "map.pdf"))


if __name__ == "__main__":
    main()
