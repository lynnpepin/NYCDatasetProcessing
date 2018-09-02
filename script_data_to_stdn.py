import numpy as np
from utils import generate_dates

'''
After being run through the data processor, use this script to:
    1. Remove the pcount/tcount axis, looking only at the trip count.
This assumes all data is in a /data folder.

Use 'script_compile_STDN' to further compile this data.
'''

fnames = ["2010-01-data.npz",
          "2010-02-data.npz",
          "2010-03-data.npz",
          "2010-04-data.npz",
          "2010-05-data.npz",
          "2010-06-data.npz",
          "2010-07-data.npz",
          "2010-08-data.npz",
          "2010-09-data.npz",
          "2010-10-data.npz",
          "2010-11-data.npz",
          "2010-12-data.npz",
          "2011-01-data.npz",
          "2011-02-data.npz",
          "2011-03-data.npz",
          "2011-04-data.npz",
          "2011-05-data.npz",
          "2011-06-data.npz",
          "2011-07-data.npz",
          "2011-08-data.npz",
          "2011-09-data.npz",
          "2011-10-data.npz",
          "2011-11-data.npz",
          "2011-12-data.npz",
          "2012-01-data.npz",
          "2012-02-data.npz",
          "2012-03-data.npz",
          "2012-04-data.npz",
          "2012-05-data.npz",
          "2012-06-data.npz",
          "2012-07-data.npz",
          "2012-08-data.npz",
          "2012-09-data.npz",
          "2012-10-data.npz",
          "2012-11-data.npz",
          "2012-12-data.npz",
          "2013-01-data.npz",
          "2013-02-data.npz",
          "2013-03-data.npz",
          "2013-04-data.npz",
          "2013-05-data.npz",
          "2013-06-data.npz",
          "2013-07-data.npz",
          "2013-08-data.npz",
          "2013-09-data.npz",
          "2013-10-data.npz",
          "2013-11-data.npz",
          "2013-12-data.npz"]


for fname in fnames:
    datestr = fname[0:7]
    data = np.load("data/"+fname)

    vdata = data['vdata'][:,:,:,:,1]
    fdata = data['fdata'][:,:,:,:,:,:,1]
    
    # Assuming vdata and fdata have the same size/resolution!!
    samples = vdata.shape[0]
    w = vdata.shape[1]
    h = vdata.shape[2]
    n = 2

    np.savez_compressed("data/STDN-volume-"+datestr+".npz", vdata)
    np.savez_compressed("data/STDN-flow-"+datestr+".npz", fdata)
