# NYCDatasetProcessing
Pre-processing for this NYC traffic dataset: https://databank.illinois.edu/datasets/IDB-9610843
See also: https://lab-work.github.io/data/

Processed data format is targeting the Spatial Temporal Dynamics Network.

(See: https://github.com/tangxianfeng/STDN and https://arxiv.org/abs/1803.01254)

Chances are, unless you are replicating the (yet unpublished) paper this is for, this is not the code you're looking for! This is not a general-purpose Python library.

## Usage

This is a command-line Python3 program used to preprocess data from the aforementioned dataset. It splits the island of Manhattan into a w*h grid and discritizes information about taxi into n slots per hour.


### Some warnings

**Warning 1:** With the default parameters, this data saves ~50GB of data! The 'flow' array takes the most space, roughly w^2 * h^2 * n * 5.7 KB of data. By changing the parameters from the defaults (w=10, h=20, n=4) to w=5, h=10, n=2, the total space reuired drops to ~2GB.

**Warning 2:** Because of the large sizes of the files, data is processed per-month. Some trips start in one month and end in another (e.g. February 28th 2011 to March 1st 2011). This means, if you are starting or restarting data processing (e.g. on April 2013) then you need to set the start month to the *previous* month (e.g. March 2013) and run with the --restart flag.

**Warning 3:** Because there is are many errors in the data, some entries are discarded. See utils.check_valid() to see the rules for discarding entries. Entries are discarded if their start times are erroneous or if their trip straight-line (l2) distance and/or delta-t are nonsensical (too short or too fast).

**Warning 4:** We sample with a grid of 10x20 with n=4 slots per hour, but we train the model on a grid size of 5x10 with n=2 slots per hour. Because these are integer multiples, it is easy to resize the *-data.npz files. If we want the higher-resolution data, it is already processed and available.

### Data format

This program loads in csv files from ../decompressed/FOIL(year)/trip\_data\_month/.csv. (E.g. ../decompresed/FOIL2010/trip\_data\_1.csv)

Then, it saves the processed data to (year)-(month)-data.npz. (E.g. 2010-01-data.npz) The format of the vdata (volume-data) and fdata (flow-data) follow the structure used with the data provided for the STDN. This example from the Python interpreter shows how to load the data:

```
>>> import numpy as np; data = np.load("2010-01-data.npz")
>>> vdata = data['vdata']; vdata.shape
(2976, 10, 20, 2, 2)
>>> fdata = data['fdata']; fdata.shape
(2, 2976, 10, 20, 10, 20, 2)
>>> trips = data['trips']; trips.shape
(2, 2, 2)
>>> errors = data['errors']; errors.shape
(2,)
```

Above, the data has 4 time slots per hour (there are 2976 such slots in January), with a grid of size 10x20. *Note:* vdata and fdata both have an extra axis of size 2. This is to store the tripcount and passenger count separately.

#### vdata axes

For a trip, the starting volume data is stored if the trip starts in Manhattan. The ending volume data is stored if the trip ends in Manhattan. This means a trip can start inside but end outside, or start outside and end inside, and still be counted in the volume data.

* Axis 0: The time slot that the trip starts/ends in. (See axis 3)
* Axis 1: The x location that the trip starts/ends in. (See axis 3)
* Axis 2: The y location that the trip starts/ends in. (See axis 3)
* Axis 3: 0 if we are looking at the *start* time and location of a trip. 1 if we are looking at the *end* time and location of a trip.
* Axis 4: 0 if we are concerned with *passenger count*. 1 if we are concerned with *trip count*.

E.g. vdata[113, 2, 4, 1, 0] gives the total number of passengers across all taxis in NYC for trips ending during time slot 113 in grid location (2, 4).

#### fdata axes

For a trip, the flow data is stored *only* if it starts and ends within Manhattan.

* Axis 0: 0 if we are concerned with the flow of trips that start and end within the same time slot. 1 if we are concerned with the flow of trips from an earlier time slot to the current time slot.
* Axis 1: The time slot that the trip ends in.
* Axis 2, 3: The x-y location of where the trip starts in.
* Axis 4, 5: The x-y location of where the trip ends in.
* Axis 6: 0 if we are concerned with *passenger count*. 1 if we are concerned with *trip count*.

E.g. fdata[1, 117, 2, 4, 3, 5, 1] gives the total number of trips from (2,4) to (3,5) that end in time slot 117 but starts in an earlier time slot.

#### trips and errors axes

The 'trips' and 'errors' array records statistical information about the trips.

*errors*: Has one axis. 0 for the number of invalid trips (per utils.check_valid()), 1 for the number of unparsable trips.

*trips*:

* Axis 0: 0 if the trip started in Manhattan, 1 if it started outside.
* Axis 1: 0 if the trip ended in Manhattan, 1 if it ended outside.
* Axis 2: 0 if we are concerned with *passenger count*. 1 if we are concerned with *trip count*.

E.g. The number of all trips that started in Manhattan = np.sum(trips[0,:,1]).

#### To be done:

We intend to merge the resulting data into two large fdata and vdata arrays, spanning Jan 2010 to Dec 2013, with w=5, h=10, n=2.

### Command line arguments

* *--startyear*, *-sy* The year to start processing from. Default: 2010
* *--startmonth*, *-sm* The month to start processing from. Default: 1 (January)
* *--endyear*, *-ey* The year to end processing. Default: 2013.
* *--endmonth*, *-em* The month to end processing. Default: 12 (December)
* *--width*, *-x* The number of x-cells in the grid. Default: 10
* *--height*, *-y* The number of y-cells in the grid. Default: 20
* *--nslotsperhour*, *-n* The number of slots in an hour. Must be an integer divisor of 60. Default: 4
* *--verbose*, *-v* Prints out helpful information while running if set.
* *--restart*, *-r* Processes the first month but does not save it. Useful for restarting computation in an event of a crash. (E.g. if it crashs during 2011 08, start on 2011 07 with the --restart argument.)

### Examples

Run the code on the default settings

```
python3.6 main.py -v
```

After a crash on May 2011, restart the script

```
python3.6 main.py -v -sm 4 -sy 2011 --restart
```

Get just the data for 2012

```
python3.6 main.py -v -sm 12 -sy 2011 -ey 2012 -em 12 --restart
```


Get the data for the default 2010-2013 period, but save it in a 5x10 array with only 2 samples per hour
```
python3.6 main.py -v -x 5 -y 10 -n 2
```
