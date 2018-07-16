import datetime
import argparse
import utils
import numpy as np

def print_time():
    print("  Timestamp:", datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S"))

def get_next(year, month):
    if month == 12:
        return (year + 1, 1)
    else:
        return (year, month + 1)

def process( startyear  = 2010,
             startmonth = 1,
             endyear    = 2013,
             endmonth   = 12,
             width      = 10,
             height     = 20,
             n          = 4,
             V          = False ):

    dates = utils.generate_dates(startyear, startmonth, endyear, endmonth)
    
    vdata_next_mo = utils.gen_empty_vdata(year=startyear, month=startmonth, w=width, h=height, n=n)
    fdata_next_mo = utils.gen_empty_fdata(year=startyear, month=startmonth, w=width, h=height, n=n)
    
    for (year, month) in dates:
        trips = np.zeros((2, 2, 2))
        invalid_count = 0    # Entries that are parsable, but are not a valid trip
        unparsable_count = 0 # Entries that raise an error on parsing
        line_number = 0
        
        # Shift the vdata in-focus to this month
        vdata = vdata_next_mo
        fdata = fdata_next_mo
        
        # Generate new, empty 'next-month' arrays
        #   (For trips that cross the boundary, e.g. 2-28 at 11:59 to 3:01 at 0:02
        next_year, next_month = get_next(year=year, month=month)
        vdata_next_mo = utils.gen_empty_vdata(year=next_year, month=next_month, w=width, h=height, n=n)
        fdata_next_mo = utils.gen_empty_fdata(year=next_year, month=next_month, w=width, h=height, n=n)
        
        load_filename = "../decompressed/FOIL"+str(year)+"/trip_data_"+str(month)+".csv"
        load_filename = "example.csv"
        
        if V:
            print("Starting on",year,month)
            print_time()
        
        with open(load_filename, "r") as read_f:
            read_f.readline() # Skip header
            for line in read_f:
                line_number += 1
                try:
                    entry = utils.process_entry(line=line, n=n)
                    if utils.check_valid(entry=entry, year=year, month=month):
                        utils.update_data(entry=entry,
                                          vdata=vdata,
                                          fdata=fdata,
                                          vdata_next_mo=vdata_next_mo,
                                          fdata_next_mo=fdata_next_mo,
                                          trips=trips,
                                          w=width,
                                          h=height,
                                          n=n)
                    else:
                        invalid_count += 1
                except E as e:
                    print("  ERROR - could not parse line", line_number)
                    print("  ########")
                    print("  ", e, sep='')
                    print("  ########")
         
        save_filename_date = str(year)+"-"+str(month).zfill(2)
        
        if V:
            print("Saving",save_filename_date)
            print_time()
        #with open(save_filename_date + "-data.npz", "w") as write_f:
        np.savez(save_filename_date + "-data.npz", vdata = vdata, fdata = fdata, trips = trips, errors = np.array([invalid_count, unparsable_count]))
        
    if V:
        print("All finished!")
        print_time()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="NYC Dataset processing")
    parser.add_argument("--startyear", "-sy",
                        help="Year to start processing from. Default 2010",
                        type=int, nargs=1)
    parser.add_argument("--startmonth", "-sm",
                        help="Month to start processing from. Default 1.",
                        type=int, nargs=1)
    parser.add_argument("--endyear", "-ey",
                        help="Year to finish processing (inclusive). Default 2013.",
                        type=int, nargs=1)
    parser.add_argument("--endmonth", "-em",
                        help="Month to finish processing (inclusive). Default 12.",
                        type=int, nargs=1)
    parser.add_argument("--width", "-x",
                        help="Width of grid (default 10)",
                        type=int, nargs=1)
    parser.add_argument("--height", "-y",
                        help="Width of grid (default 20)",
                        type=int, nargs=1)
    parser.add_argument("--nslotsperhour", "-n",
                        help="Discretize time into n slots per hour. Must be integer divisor of 60. (Default 4)",
                        type=int, nargs=1)
    parser.add_argument("--verbose", "-v",
                        help="",
                        action="store_true")

    args = parser.parse_args()
    
    V = args.verbose
    
    startyear   = 2010  if args.startyear   is None else args.startyear[0]
    startmonth  = 1     if args.startmonth  is None else args.startmonth[0]
    endyear     = 2013  if args.endyear     is None else args.endyear[0]
    endmonth    = 12    if args.endmonth    is None else args.endmonth[0]
    width       = 10    if args.width       is None else args.width[0]
    height      = 20    if args.height      is None else args.height[0]
    n           = 4     if args.nslotsperhour is None else args.nslotsperhour[0]
    
    print("NYCDataProcessing/main.py started.")
    
    if V:
        print_time()
        print("Running with arguments:")
        print("  Verbose")
        print("  ",startyear, ", ", startmonth, " to ", endyear, ", ", endmonth, ".",sep="")
        print("  With",n,"samples year hour.")
        print("  On a grid of size ",width,"x",height,".", sep="")

    process( startyear  = startyear,
             startmonth = startmonth,
             endyear    = endyear,
             endmonth   = endmonth,
             width      = width,
             height     = height,
             n          = n,
             V          = V)
    
