import datetime
import argparse

def print_time():
    print("Timestamp:", datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S"))

def process( startyear  = 2010,
             startmonth = 1,
             endyear    = 2013,
             endmonth   = 12,
             width      = 10,
             height     = 20,
             n          = 4,
             V          = False ):
    pass

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
    
