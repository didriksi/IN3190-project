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
    parser.add_argument("--filter-signals", action="store_true",
                        help="Filter all 201 signals from the different "\
                             "stations with h1, h2 and h3.")
    parser.add_argument("--plot-sections", action="store_true",
                        help="Plot all the signals from the different stations,"\
                             " filtered through h3.")
    parser.add_argument("--mark-arrival-time", action="store_true",
                        help="Mark the arrival times of the wave at all the "\
                             "different stations")
    

    return parser.parse_args(argv)


def main():
    processed_data_filename = os.path.join(constants.ROOT_DIR, "data",
                                           "processed", "processed.npz")
    convolved_dir = os.path.join(constants.ROOT_DIR, "data", "processed",
                                     "convolved")

    h_list = [constants.h1, constants.h2, constants.h3]

    args = parse_arguments()
    
    if args.parse_data:
        process_data.process_data()
    
    if args.plot_map:
        processed_data = np.load(processed_data_filename)
        lats, lons = processed_data["lats"], processed_data["lons"]
        stations_coordinates = np.concatenate((lats[:, np.newaxis],
                                               lons[:, np.newaxis]),
                                              axis=1)
        plot.geography(constants.TONGA_COORDINATES, stations_coordinates, 
                       os.path.join(constants.PLOTS_DIR, "map.pdf"))
    
    if args.plot_distances:
        processed_data = np.load(processed_data_filename)
        distances = processed_data["distances"]
        plot.distances(distances,
                       os.path.join(constants.PLOTS_DIR, "distances.pdf"))
    
    if args.plot_fir:
        plot.input_response(h_list,
                            ["$h_1$", "$h_2$", "$h_3$"],
                            os.path.join(constants.PLOTS_DIR, "fir.pdf"))
    
    if args.plot_freq_spec:
        plot.frequency_spectrum(h_list,
                                ["$H_1$ - lowpass", "$H_2$ - bandpass", "$H_3$ - highpass"],
                                side_by_side=True,
                                filename=os.path.join(constants.PLOTS_DIR, "freq_spec.pdf"))
    
    if args.filter_signals:
        convolved_dir = os.path.join(constants.ROOT_DIR, "data", "processed",
                                     "convolved")
        processed_data = np.load(processed_data_filename)
        for i, x in enumerate(processed_data["data"]):
            for j, h in enumerate(h_list):
                y = signal_processing.convolution(x, h, ylen_choice=False)
                filename = os.path.join(convolved_dir, f"h{j+1}_x{i:03}.npy")
                np.save(filename, y)
    
    if args.plot_sections:
        signal_files = process_data.get_filenames(convolved_dir)
        signal_files = sorted(list(filter(lambda s: "h2" in s, signal_files)))

        processed_data = np.load(processed_data_filename)
        sort_inds = np.argsort(processed_data["distances"])
        distances = processed_data["distances"][sort_inds]
        times = processed_data["times"][sort_inds]
        signals = [signal_files[i] for i in sort_inds]

        plot_filename = os.path.join(constants.PLOTS_DIR, "sections.pdf")
        plot.sections(signals, times, distances, plot_filename)
    
    if args.mark_arrival_time:
        processed_data = np.load(processed_data_filename)
        data = processed_data["data"]
        times = processed_data["times"]

        arrival_times_filename = os.path.join(constants.ROOT_DIR, "data",
                                              "arrival_times", "arrival_times.npy")
        valids_filename = os.path.join(constants.ROOT_DIR, "data",
                                       "arrival_times", "valids.npy")

        load_convolved = lambda h, station_id: np.load(os.path.join(convolved_dir, f"h{h}_x{station_id:03}.npy"))
        
        if os.path.exists(arrival_times_filename):
            arrival_times = np.load(arrival_times_filename)
            valids = np.load(valids_filename)
        else:
            arrival_times = np.zeros(len(data), dtype=float)
            valids = np.zeros_like(arrival_times)
        
        for station_id, (x, t) in enumerate(zip(data, times)):
            if arrival_times[station_id] != 0:
                continue
            
            signals = {"Trace": x}
            signals.update({f"$h_{j+1}$": load_convolved(j+1, station_id) for j in range(3)})
            arrival_time, valid = plot.mark_arrival_time(station_id, t, **signals)
            arrival_times[station_id] = arrival_time
            valids[station_id] = valid
            
            # Continually save the arrays in case the script crashes
            np.save(arrival_times_filename, arrival_times)
            np.save(valids_filename, valids)

if __name__ == "__main__":
    main()
