import numpy as np
from utils import generate_dates

for (year, month) in generate_dates(

data = np.load("2010-01-data.npz")
vdata = data['vdata'][:,:,:,:,1]
fdata = data['fdata'][:,:,:,:,:,:,1]
