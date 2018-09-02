import numpy as np
from utils import generate_dates

''' Use this to take all the individual STDN files in data/
    and put them into four large numpy arrays
'''


# First batch of filenames
fns_f = ["STDN-flow-2013-01.npz",
        "STDN-flow-2013-02.npz"]

fns_v = ["STDN-volume-2013-01.npz",
        "STDN-volume-2013-02.npz"]

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

