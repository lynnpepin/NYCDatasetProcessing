import numpy as np
from utils import generate_dates

''' Use this to take all the individual STDN files in data/
    and put them into four large numpy arrays.
    
    This is split first by flow/volume, and second by the
    break in data (no data from 2011-06 to 2011-09).
'''


# First batch of filenames
fns_f = ["STDN-flow-2010-01.npz",
        "STDN-flow-2010-02.npz",
        "STDN-flow-2010-03.npz",
        "STDN-flow-2010-04.npz",
        "STDN-flow-2010-05.npz",
        "STDN-flow-2010-06.npz",
        "STDN-flow-2010-07.npz",
        "STDN-flow-2010-08.npz",
        "STDN-flow-2010-09.npz",
        "STDN-flow-2010-10.npz",
        "STDN-flow-2010-11.npz",
        "STDN-flow-2010-12.npz",
        "STDN-flow-2011-01.npz",
        "STDN-flow-2011-02.npz",
        "STDN-flow-2011-03.npz",
        "STDN-flow-2011-04.npz",
        "STDN-flow-2011-05.npz",
        "STDN-flow-2011-06.npz",
        "STDN-flow-2011-07.npz",
        "STDN-flow-2011-08.npz",
        "STDN-flow-2011-09.npz",
        "STDN-flow-2011-10.npz",
        "STDN-flow-2011-11.npz",
        "STDN-flow-2011-12.npz",
        "STDN-flow-2012-01.npz",
        "STDN-flow-2012-02.npz",
        "STDN-flow-2012-03.npz",
        "STDN-flow-2012-04.npz",
        "STDN-flow-2012-05.npz",
        "STDN-flow-2012-06.npz",
        "STDN-flow-2012-07.npz",
        "STDN-flow-2012-08.npz",
        "STDN-flow-2012-09.npz",
        "STDN-flow-2012-10.npz",
        "STDN-flow-2012-11.npz",
        "STDN-flow-2012-12.npz",
        "STDN-flow-2013-01.npz",
        "STDN-flow-2013-02.npz",
        "STDN-flow-2013-03.npz",
        "STDN-flow-2013-04.npz",
        "STDN-flow-2013-05.npz",
        "STDN-flow-2013-06.npz",
        "STDN-flow-2013-07.npz",
        "STDN-flow-2013-08.npz",
        "STDN-flow-2013-09.npz",
        "STDN-flow-2013-10.npz",
        "STDN-flow-2013-11.npz",
        "STDN-flow-2013-12.npz"]

fns_v = ["STDN-volume-2010-01.npz",
        "STDN-volume-2010-02.npz",
        "STDN-volume-2010-03.npz",
        "STDN-volume-2010-04.npz",
        "STDN-volume-2010-05.npz",
        "STDN-volume-2010-06.npz",
        "STDN-volume-2010-07.npz",
        "STDN-volume-2010-08.npz",
        "STDN-volume-2010-09.npz",
        "STDN-volume-2010-10.npz",
        "STDN-volume-2010-11.npz",
        "STDN-volume-2010-12.npz",
        "STDN-volume-2011-01.npz",
        "STDN-volume-2011-02.npz",
        "STDN-volume-2011-03.npz",
        "STDN-volume-2011-04.npz",
        "STDN-volume-2011-05.npz",
        "STDN-volume-2011-06.npz",
        "STDN-volume-2011-07.npz",
        "STDN-volume-2011-08.npz",
        "STDN-volume-2011-09.npz",
        "STDN-volume-2011-10.npz",
        "STDN-volume-2011-11.npz",
        "STDN-volume-2011-12.npz",
        "STDN-volume-2012-01.npz",
        "STDN-volume-2012-02.npz",
        "STDN-volume-2012-03.npz",
        "STDN-volume-2012-04.npz",
        "STDN-volume-2012-05.npz",
        "STDN-volume-2012-06.npz",
        "STDN-volume-2012-07.npz",
        "STDN-volume-2012-08.npz",
        "STDN-volume-2012-09.npz",
        "STDN-volume-2012-10.npz",
        "STDN-volume-2012-11.npz",
        "STDN-volume-2012-12.npz",
        "STDN-volume-2013-01.npz",
        "STDN-volume-2013-02.npz",
        "STDN-volume-2013-03.npz",
        "STDN-volume-2013-04.npz",
        "STDN-volume-2013-05.npz",
        "STDN-volume-2013-06.npz",
        "STDN-volume-2013-07.npz",
        "STDN-volume-2013-08.npz",
        "STDN-volume-2013-09.npz",
        "STDN-volume-2013-10.npz",
        "STDN-volume-2013-11.npz",
        "STDN-volume-2013-12.npz"]

# fdata
# Load from the first line
fdata = np.load("data/" + fns_f[0])['arr_0']

# And then concate from the rest of the lines
for fname in fns_f[1:]:
    print("Loading from",fname)
    fdata = np.concatenate((fdata, np.load("data/" + fname)['arr_0']), axis=1)

print("Saving to STDN-flow.npz")
np.savez_compressed("data/STDN-flow.npz",fdata)
del(fdata) # Free from memory!

# vdata
# Load from the first line
print("Loading from", fns_v[0])
vdata = np.load("data/" + fns_v[0])['arr_0']
# And then concate from the rest of the lines
for fname in fns_v[1:]:
    print("Loading from", fname)
    vdata = np.concatenate((vdata, np.load("data/" + fname)['arr_0']), axis=0)

print("Saving to STDN-volume.npz")
np.savez_compressed("data/STDN-volume.npz",vdata)
del(vdata) # Free from memory!
