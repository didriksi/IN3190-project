"""Module for loading the data and making it easier to handle.
"""
import os
import h5py
from datetime import datetime
import time

import numpy as np
import haversine as hs

import constants

def get_filenames(path):
    """Get names of all files in `path`.

    Arguments:
        path: String of the place to look for files.

    Return: List of strings.
    """
    return [os.path.join(path, f) for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f))]


epoch = datetime.utcfromtimestamp(0)
def unix_time(dt):
    return (dt - epoch).total_seconds()


def distance(coordinates, other_coordinates):
    return hs.haversine(coordinates, other_coordinates, unit=hs.Unit.METERS)


def process_data():
    raw_filenames = get_filenames(os.path.join(constants.ROOT_DIR, "data", "raw"))

    data = np.zeros((len(raw_filenames), 720000), dtype=float)
    times = np.zeros_like(data)
    lats = np.zeros(len(raw_filenames), dtype=float)
    lons = np.zeros_like(lats)
    distances = np.zeros_like(lats)

    for i, filename in enumerate(raw_filenames):
        with h5py.File(filename, "r") as file:
            dataset_name = list(file["waveforms"].keys())[0]
            dataset = file[f"waveforms/{dataset_name}"][:]
            data[i][:len(dataset)] = dataset

            starttime_string = file[f"waveforms/{dataset_name}"].attrs.get("starttime")
            starttime = unix_time(datetime.strptime(starttime_string,
                                                    "%Y-%m-%dT%H:%M:%S.%fZ"))
            delta = file[f"waveforms/{dataset_name}"].attrs.get("delta")
            deltas = np.linspace(0, delta*len(dataset), len(dataset))
            times[i][:len(dataset)] = starttime + deltas

            lats[i] = file.attrs.get("latitude")
            lons[i] = file.attrs.get("longitude")
            distances[i] = distance(constants.TONGA_COORDINATES,
                                    (lats[i], lons[i]))

    np.savez(os.path.join(constants.ROOT_DIR, "data", "processed", "processed.npz"),
             data=data, times=times, lats=lats, lons=lons, distances=distances)

if __name__ == "__main__":
    process_data()
