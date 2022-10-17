# IN3190-project
Midterm project in IN3190 - Digital Signal Processing

## Usage
There is a `Makefile` here, to ease usage. Running `make project.pdf` should perform all the actions required to get the end report ready, except for one thing: You need to supply the raw data as a file called `project_data.zip` in the root of this repository.

The makefile is primarily a wrapper around the `src/main.py` file, which works as a CLI. It can be used with
```
usage: main.py [-h] [--parse-data] [--plot-map] [--plot-distances] [--plot-fir] [--plot-freq-spec] [--filter-signals] [--plot-sections] [--mark-arrival-times] [--plot-arrival-times]

optional arguments:
  -h, --help            show this help message and exit
  --parse-data          Load the data, and make derivative files from it that is easier to read and use.
  --plot-map            Plot a map of all the locations measurements were made.
  --plot-distances      Get the distances between all the stations and Hunga Tonga.
  --plot-fir            Plot the three given filter input responses, h1, h2 and h3.
  --plot-freq-spec      Plot the absolute values of the frequency spectrums from h1, h2 and h3.
  --filter-signals      Filter all 201 signals from the different stations with h1, h2 and h3.
  --plot-sections       Plot all the signals from the different stations, filtered through h3.
  --mark-arrival-times  Mark the arrival times of the wave at all the different stations.
  --plot-arrival-times  Plot the arrival times of the wave at all the different stations against their distances.
  ```
  The makefile calls these actions, but does so in the correct order making sure all the prerequisites are met. The only one of these not called to make `project.pdf`, is `--mark-arrival-times`, because it takes so long that we have just placed the files it generates in `data/arrival_times`. If you want to mark them yourself, please remove the files in that folder, and then call `make tasks/mark_arrival_times`.

## Issues with installing cartopy
If you are having issues installing cartopy, please follow the instructions on [their website](https://scitools.org.uk/cartopy/docs/latest/installing.html).
