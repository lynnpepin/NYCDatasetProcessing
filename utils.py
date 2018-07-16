''' A number of functions used in main.py to process the data.'''

import regex as re
from datetime import datetime
from GPSUtils import pgps_to_xy, gps_distance
from math import floor
import numpy as np

def get_t(day, hour, minute, n=4):
    ''' Returns the sample numbr given the day, hour, and minute.
    Day is 1-indexed, hour and minute is 0 indexed.'''
    return floor( ((((day-1)*24 + hour)*60) + minute)/floor((60/n)) )

def process_entry(line, n=4):
    ''' Given string line from the .csv,
        return a dict representing that entry. '''
    entry_strings = line.strip().split(",")
    regex_format = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
    
    # Extract the string out from scruff that might be around it
    start_time_string = re.search(regex_format, entry_strings[5]).group()
    end_time_string = re.search(regex_format, entry_strings[6]).group()
    
    # Parse the times using datetime
    time_format = "%Y-%m-%d %H:%M:%S"
    start_time = datetime.strptime(start_time_string, time_format)
    end_time = datetime.strptime(end_time_string, time_format)
    
    # Starting and ending GPS coordinates
    slon = float(entry_strings[10].strip())
    slat = float(entry_strings[11].strip())
    elon = float(entry_strings[12].strip())
    elat = float(entry_strings[13].strip())
    
    # Starting and ending grid coordinates and straight-line (l2) distance
    # Warning: Uses prebaked Manhattan values.
    sx, sy = pgps_to_xy(slon, slat)
    ex, ey = pgps_to_xy(elon, elat)
    l2distance = gps_distance((slat, slon), (elat, elon))
    # Get the starting and ending times
    st = get_t(day    = start_time.day,
               hour   = start_time.hour,
               minute = start_time.minute,
               n      = n)
    et = get_t(day    = end_time.day,
               hour   = end_time.hour,
               minute = end_time.minute,
               n      = n)
    
    # Get the change in time (deltat) in seconds.
    if end_time > start_time: # Normal case
        deltat = (end_time - start_time).seconds
    else: # Case: start_time is after end_time
        deltat = -(start_time - end_time).seconds
    
    # Convention:
    # 's' stands for 'start', 'e' stands for 'end',
    # 'x' and 'y' stand for x/y coordinates respectively,
    # 't' stands for time slot or seconds.
    entry = {
        'sx' : sx,
        'sy' : sy,
        'ex' : ex,
        'ey' : ey,
        'l2distance' : l2distance,
        'distance'   : float(entry_strings[9].strip()),
        'st' : st,
        'et' : et,
        'syear'  : start_time.year,
        'smonth' : start_time.month,
        'sday'   : start_time.day,
        'shour'  : start_time.hour,
        'smin'   : start_time.minute,
        'ssec'   : start_time.second,
        'eyear'  : end_time.year,
        'emonth' : end_time.month,
        'eday'   : end_time.day,
        'ehour'  : end_time.hour,
        'emin'   : end_time.minute,
        'esec'   : end_time.second,
        'pcount' : int(entry_strings[7].strip()), #Passenger count
        'deltat' : deltat
    }
    
    return entry

def check_valid(entry, year, month, min_time=59, max_speed=36, min_distance=100):
    ''' Ensure an entry meets these following rules:
    1. Starts during the same year/month as the provided parameters.
    2. l2 distance is at least min_distance  (100m)
    3. Trip lasts at least min_time (59s)
    4. Trip speed straight line distance doesn't exceed max speed (36m/s)
    
    Returns 'True' if valid, 'False' if not.
    '''
    if not entry['syear']  == year:   return False
    if not entry['smonth'] == month:  return False
    if not entry['l2distance'] >= min_distance:return False
    if not entry['deltat'] >= min_time: return False
    if not (entry['l2distance'] / entry['deltat']) <= max_speed: return False 
    return True
    

def generate_dates(start_year = 2010, start_month = 1, end_year = 2013, end_month = 12):
    ''' Returns a list of (year, month) tuples from
        (start_year, start_month) to (end_year, end_month), inclusive.'''
    year = start_year
    month = start_month
    dates = [(year, month)]
    while not (year, month) == (end_year, end_month):
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        dates.append((year, month))
    
    return dates

def no_days_in_mo(year, month):
    ''' Return int: the number of days in a given year-month combo.'''
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif month in (4, 6, 9, 11):
        return 30
    else: # month = 2 (February)
        if year % 4 != 0:
            return 28
        elif year % 100 != 0:
            return 29
        elif year % 400 != 0:
            return 28
        else:
            return 29

def no_samples_in_mo(year, month, n=4):
    ''' Return the number of timeslots in a given year and month '''
    return no_days_in_mo(year=year, month=month)*24*n

def gen_empty_vdata(year, month, w=10, h=20, n=4):
    ''' Return an all-zero 'vdata' numpy array.
    Used to store volume data, as per the STDN.'''
    samples = no_samples_in_mo(year=year, month=month, n=n)
    return np.zeros((samples, w, h, 2, 2), dtype=np.int16)

def gen_empty_fdata(year, month, w=10, h=20, n=4):
    ''' Return an all-zero 'fdata' numpy array.
    Used to store flow data, as per the STDN.'''
    samples = no_samples_in_mo(year=year, month=month, n=n)
    return np.zeros((2, samples, w, h, w, h, 2), dtype=np.int16)

def update_data(entry, vdata, fdata, vdata_next_mo, fdata_next_mo, trips, w=10, h=20, n=4):
    ''' Updates the given numpy arrays with data from the provided entry.
        Returns nothing.
    
    # Arguments:
        entry: Dictionary providing pertinent values for a given trip.
        vdata, fdata: Numpy arrays representing the volume and flow
            data for a given month.
        vdata_next_mo, fdata_next_mo: Numpy array representing the
            volume and flow data for the next month. (Useful for those
            trips that start in this month and end in the next.)
        trips: Numpy array that stores statistical information about
            the total number of trips and passengers in the month.
        w, h: Ints; width and height of the grud
        n: Number of timeslots per hour.
    '''
    # starts_inside, ends_inside: Booleans.
    # True if the trip starts within Manhattan, false otherwise
    starts_inside = (0 <= entry['sx'] <= 1) and (0 <= entry['sy'] <= 1)
    ends_inside   = (0 <= entry['ex'] <= 1) and (0 <= entry['ey'] <= 1)
    
    starts_and_ends_in_same_month = (entry['smonth'] == entry['emonth'])
    
    # Variable names:
    #   s/e stands for start/end, g stands for grid, x/y are coordinates
    sgx = floor(entry['sx']*w) #start-x, mapped to grid coordinates
    sgy = floor(entry['sy']*w) #start-y, mapped to grid coordinates
    egx = floor(entry['ex']*w) #end-x, mapped to grid coordinates
    egy = floor(entry['ey']*w) #end-y, mapped to grid coordinates
    pcount = entry['pcount']
    
    # Trips is a (2,2,2) array: [starts in/outside, ends in/side, passenger/trip count]
    trips[int(not starts_inside), int(not ends_inside), 0] += pcount
    trips[int(not starts_inside), int(not ends_inside), 1] += 1
    
    # Data-update rules below come from the definition of volume and flow, per the STDN paper.
    # Data shape is taken from the shape used in the original STDN code.
    #   Note: Here, Passenger count and trip count are recorded separately.
    if starts_inside:
        # Update volume data for the start of the trip
        vdata[entry['st'], sgx, sgy, 0, 0] += pcount
        vdata[entry['st'], sgx, sgy, 0, 1] += 1
        
        if ends_inside:
            # Update volume data only if the trip starts and ends within Manhattan.
            if entry['st'] == entry['et']:
                # st == et, so we don't need to check if et is in the
                #    next month.
                fdata[0, entry['et'], sgx, sgy, egx, egy, 0] += pcount
                fdata[0, entry['et'], sgx, sgy, egx, egy, 1] += 1
            else:
                if starts_and_ends_in_same_month:
                    fdata[1, entry['et'], sgx, sgy, egx, egy, 0] += pcount
                    fdata[1, entry['et'], sgx, sgy, egx, egy, 1] += 1
                else: # End time crosses over to the next month
                    fdata_next_mo[1, entry['et'], sgx, sgy, egx, egy, 0] += pcount
                    fdata_next_mo[1, entry['et'], sgx, sgy, egx, egy, 1] += 1

    if ends_inside:
        # Update volume data for the end of the trip.
        if starts_and_ends_in_same_month:
            vdata[entry['et'], egx, egy, 1, 0] += pcount
            vdata[entry['et'], egx, egy, 1, 1] += 1
        
        else: # Ends during the next month, so use the array representing the next month
            vdata_next_mo[entry['et'], egx, egy, 1, 0] += pcount
            vdata_next_mo[entry['et'], egx, egy, 1, 1] += 1
            
    # Returns nothing - numpy arrays are updated by reference.
