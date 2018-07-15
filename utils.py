import regex as re
from datetime import datetime
from GPSUtils import pgps_to_xy, gps_distance
from math import floor
import numpy as np
# pgps to xy assumes the Manhattan grid specific to this project!

def get_t(day, hour, minute, n=4):
    return floor( (((day*24 + hour)*60) + minute)/n )

def process_entry(line, n=4):
    entry_strings = line.strip().split(",")
    
    regex_format = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
    
    # Extract the string out from any quote marks that might be around it
    start_time_string = re.search(regex_format, entry_strings[5]).group()
    end_time_string = re.search(regex_format, entry_strings[6]).group()
    
    # Parse it with datetime
    time_format = "%Y-%m-%d %H:%M:%S"
    start_time = datetime.strptime(start_time_string, time_format)
    end_time = datetime.strptime(end_time_string, time_format)
    
    # Starting and ending positions
    slon = float(entry_strings[10].strip())
    slat = float(entry_strings[11].strip())
    elon = float(entry_strings[12].strip())
    elat = float(entry_strings[13].strip())
    
    sx, sy = pgps_to_xy(slon, slat)
    ex, ey = pgps_to_xy(elon, elat)
    l2distance = gps_distance((slat, slon), (elat, elon))
    st = get_t(day = start_time.day, hour = start_time.hour, minute=start_time.minute, n=n)
    et = get_t(day = end_time.day, hour = end_time.hour, minute=end_time.minute, n=n)
    
    if end_time > start_time: # Normal case
        deltat = (end_time - start_time).seconds
    else: # start_time is after end_time
        deltat = (start_time - end_time).seconds
    
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
        'pcount' : int(entry_strings[7].strip()),
        'deltat' : deltat
    }
    
    return entry

def check_valid(entry, year, month, min_time=59, max_speed=36, min_distance=100):
    # Units in meters and seconds
    if not entry['syear']  == year:   return False
    if not entry['smonth'] == month:  return False
    if not entry['l2distance'] >= min_distance:return False
    if not entry['deltat'] >= min_time: return False
    if not (entry['l2distance'] / entry['deltat']) <= max_speed: return False 
    return True
    

def generate_dates(start_year = 2010, start_month = 1, end_year = 2013, end_month = 12):
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
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif month in (4, 6, 9, 11):
        return 30
    else: # month = 2
        if year % 4 != 0:
            return 28
        elif year % 100 != 0:
            return 29
        elif year % 400 != 0:
            return 28
        else:
            return 29

def no_samples_in_mo(year, month, n=4):
    return no_days_in_mo(year=year, month=month)*24*n

def gen_empty_vdata(year, month, w=10, h=20, n=4):
    samples = no_samples_in_mo(year=year, month=month, n=n)
    return np.zeros((samples, w, h, 2, 2), dtype=np.int16)

def gen_empty_fdata(year, month, w=10, h=20, n=4):
    samples = no_samples_in_mo(year=year, month=month, n=n)
    return np.zeros((2, samples, w, h, w, h, 2), dtype=np.int16)
