import unittest as ut
import numpy as np
import random
from GPSUtils import gps_to_xy, pgps_to_xy, gps_distance
import utils

class GPSUtilsTest(ut.TestCase):
    ''' Meant to test the function according to our Manhattan grid.'''
    def setUp(self):
        self.orlon = -74.038971
        self.orlat =  40.709279
        self.tllon = -73.96834326
        self.tllat =  40.81703286
        self.brlon = -73.996317
        self.brlat =  40.68132125
        self.trlon = -73.92568926
        self.trlat =  40.78907511 
        
        # Each of the four corners
        # using the gps_to_xy and prebaked pgps_to_xy
        # Rounded to 4 decimal places to avoid error
        self.orcorner_g = tuple([round(ii, 4) for ii in gps_to_xy(self.orlon, self.orlat)])
        self.tlcorner_g = tuple([round(ii, 4) for ii in gps_to_xy(self.tllon, self.tllat)])
        self.brcorner_g = tuple([round(ii, 4) for ii in gps_to_xy(self.brlon, self.brlat)])
        self.trcorner_g = tuple([round(ii, 4) for ii in gps_to_xy(self.trlon, self.trlat)])
        self.orcorner_p = tuple([round(ii, 4) for ii in pgps_to_xy(self.orlon, self.orlat)])
        self.tlcorner_p = tuple([round(ii, 4) for ii in pgps_to_xy(self.tllon, self.tllat)])
        self.brcorner_p = tuple([round(ii, 4) for ii in pgps_to_xy(self.brlon, self.brlat)])
        self.trcorner_p = tuple([round(ii, 4) for ii in pgps_to_xy(self.trlon, self.trlat)])
        
    
    def tearDown(self):
        pass
    
    def test_equal_values(self):
        '''... Test that gps_to_xy and pgps_to_xy give the same values.'''
        self.assertEqual(self.orcorner_g, self.orcorner_p)
        self.assertEqual(self.brcorner_g, self.brcorner_p)
        self.assertEqual(self.trcorner_g, self.trcorner_p)
        self.assertEqual(self.tlcorner_g, self.tlcorner_p)
        
        for _ in range(1000):
            lon = self.orlon + 2*(random.random() - .5)
            lat = self.orlat + 2*(random.random() - .5)
            corner_g = tuple([round(ii, 4) for ii in gps_to_xy(lon, lat)])
            corner_p = tuple([round(ii, 4) for ii in pgps_to_xy(lon, lat)])
            self.assertEqual(corner_g, corner_p)
    
    def test_corners(self):
        '''... Test that gps_to_xy gives the proper values on the corners.
            Per the previous test, if this passes, pgps should too. '''
        self.assertEqual(self.orcorner_g, (0,0))
        self.assertEqual(self.brcorner_g, (1,0))
        self.assertEqual(self.tlcorner_g, (0,1))
        self.assertEqual(self.trcorner_g, (1,1))

    def test_gps_distance_equality(self):
        '''... Ensure gps_distance(a,b) == gps_distance(b,a) '''
        for _ in range(1000):
            slon = (random.random() - .5)*180
            slat = (random.random() - .5)*90
            dlon = (random.random() - .5)*180
            dlat = (random.random() - .5)*90
            
            d1 = gps_distance((slon, slat), (dlon, dlat))
            d2 = gps_distance((dlon, dlat), (slon, slat))
            
            self.assertEqual(round(d1), round(d2))

    def test_gps_distance(self):
        '''... Test we calculate distances properly. '''
        orcorner = (self.orlat, self.orlon)
        tlcorner = (self.tllat, self.tllon)
        brcorner = (self.brlat, self.brlon)
        trcorner = (self.trlat, self.trlon)
        # From the UT example
        self.assertEqual(round(gps_distance((48.1372, 11.5756),(52.5186, 13.4083)),-2),504200)
        # Zero-distances
        self.assertEqual(round(gps_distance(orcorner, orcorner)), 0)
        self.assertEqual(round(gps_distance(brcorner, brcorner)), 0)
        self.assertEqual(round(gps_distance(trcorner, trcorner)), 0)
        self.assertEqual(round(gps_distance(tlcorner, tlcorner)), 0)

        # From https://gps-coordinates.org/distance-between-coordinates.php
        or_to_br =  4753.49
        tl_to_tr =  4749.09
        or_to_tl = 13376.96
        br_to_tr = 13378.08
        or_to_tr = 13030.40
        br_to_tl = 15273.32
        
        gps_or_to_br = gps_distance(orcorner, brcorner)
        gps_tl_to_tr = gps_distance(tlcorner, trcorner)
        gps_or_to_tl = gps_distance(orcorner, tlcorner)
        gps_br_to_tr = gps_distance(brcorner, trcorner)
        gps_or_to_tr = gps_distance(orcorner, trcorner)
        gps_br_to_tl = gps_distance(brcorner, tlcorner)
        
        # Differences - must be within 1m of one another
        max_difference = 1
        d_or_to_br = abs(or_to_br - gps_or_to_br)
        d_tl_to_tr = abs(tl_to_tr - gps_tl_to_tr)
        d_or_to_tl = abs(or_to_tl - gps_or_to_tl)
        d_br_to_tr = abs(br_to_tr - gps_br_to_tr)
        d_or_to_tr = abs(or_to_tr - gps_or_to_tr)
        d_br_to_tl = abs(br_to_tl - gps_br_to_tl)
        
        self.assertTrue(max_difference >= d_or_to_br)
        self.assertTrue(max_difference >= d_tl_to_tr)
        self.assertTrue(max_difference >= d_or_to_tl)
        self.assertTrue(max_difference >= d_br_to_tr)
        self.assertTrue(max_difference >= d_or_to_tr)
        self.assertTrue(max_difference >= d_br_to_tl)

class UtilsMiscTest(ut.TestCase):
    # Test the simpler utils
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_get_t(self):
        self.assertEqual(utils.get_t(day=4, hour=13, minute=15, n=12), 546)
        self.assertEqual(utils.get_t(day=4, hour=14, minute=10, n=12), 550)

    def test_generate_dates(self):
        list_1 = utils.generate_dates(start_year = 2010, start_month = 4, end_year = 2010, end_month = 6)
        list_2 = utils.generate_dates(start_year = 2011, start_month = 11, end_year = 2012, end_month = 2)
        list_3 = utils.generate_dates(start_year = 2011, start_month = 1, end_year = 2011, end_month = 1)
        
        self.assertEqual(list_1, [(2010, 4), (2010, 5), (2010, 6)])
        self.assertEqual(list_2, [(2011, 11), (2011, 12), (2012, 1), (2012, 2)])
        self.assertEqual(list_3, [(2011, 1)])

    def test_no_days_in_mo(self):
        for year in range(2000, 2040):
            for mo in (1, 3, 5, 7, 8, 10, 12):
                self.assertEqual(utils.no_days_in_mo(year=year, month=mo), 31)
            for mo in (4, 6, 9, 11):
                self.assertEqual(utils.no_days_in_mo(year=year, month=mo), 30)
        self.assertEqual(utils.no_days_in_mo(month=2, year=2010), 28)
        self.assertEqual(utils.no_days_in_mo(month=2, year=2011), 28)
        self.assertEqual(utils.no_days_in_mo(month=2, year=2012), 29)
        self.assertEqual(utils.no_days_in_mo(month=2, year=2013), 28)

    def test_no_samples_in_mo(self):
        self.assertEqual(utils.no_samples_in_mo(year=2010, month=2, n=12), 8064)
        self.assertEqual(utils.no_samples_in_mo(year=2010, month=3, n=12), 8928)
        self.assertEqual(utils.no_samples_in_mo(year=2010, month=4, n=4),  2880)
        self.assertEqual(utils.no_samples_in_mo(year=2012, month=2),  2784) # Default n=4

    def test_gen_empty_vfdata(self):
        for _ in range(100):
            year = random.randint(2010, 2013)
            month = random.randint(1, 12)
            w = random.randint(1,3)
            h = random.randint(1,6)
            n = random.randint(1,3)
            vdata = utils.gen_empty_vdata(year=year, month=month, w=w, h=h, n=n)
            fdata = utils.gen_empty_fdata(year=year, month=month, w=w, h=h, n=n)
            
            expected_number_of_samples = utils.no_samples_in_mo(year=year, month=month, n=n)
            
            # Make sure they are of proper dtype
            self.assertEqual(vdata.dtype, np.int16)
            self.assertEqual(fdata.dtype, np.int16)
            
            # Make sure they are of proper shape
            self.assertEqual(vdata.shape[0], expected_number_of_samples)
            self.assertEqual(vdata.shape[1], w)
            self.assertEqual(vdata.shape[2], h)
            self.assertEqual(vdata.shape[3], 2)
            self.assertEqual(vdata.shape[4], 2)
            self.assertEqual(fdata.shape[0], 2)
            self.assertEqual(fdata.shape[1], expected_number_of_samples)
            self.assertEqual(fdata.shape[2], w)
            self.assertEqual(fdata.shape[3], h)
            self.assertEqual(fdata.shape[4], w)
            self.assertEqual(fdata.shape[5], h)
            self.assertEqual(fdata.shape[6], 2)
            
            # Test some random values, check for zeroes!
            for _ in range(10):
                t = random.randint(0, expected_number_of_samples-1)
                x = random.randint(0, w-1)
                y = random.randint(0, h-1)
                a1 = random.randint(0, 1)
                a2 = random.randint(0, 1)
                
                self.assertEqual(vdata[t,x,y,a1,a2], 0)
                self.assertEqual(fdata[a1,t,x,y,x,y,a2], 0)
    
    def test_check_valid(self):
        start_year = 2011
        start_month = 3
        n = 4
        # Shows a 5 minute trip spanning midnight boundary, over 1.1 miles within Manhattan
        valid_lines    = ['2010000001,2010000001,"VTS",1,,"2011-03-14 23:59:10","2011-03-15 00:04:11",4,301,1.1,-73.970610,40.793724,-73.974672,40.783098\n', # Short trip; 5min 1.1 mile, l2dist 1.23km
                          '2010000002,2010000002,"VTS",1,,"2011-03-14 22:10:10","2011-03-14 22:42:16",4,1926,9.7,-73.954559,40.799313,-74.005135,40.721522\n'] # Long trip; 32min 9.7 mile, l2dist 9.64km
                         # start_year, start_month don't match
        invalid_lines = ['2010000001,2010000001,"VTS",1,,"2011-02-14 23:59:10","2011-03-15 00:04:11",4,301,1.1,-73.970610,40.793724,-73.974672,40.783098\n',
                         '2010000001,2010000001,"VTS",1,,"2011-04-14 23:59:10","2011-03-15 00:04:11",4,301,1.1,-73.970610,40.793724,-73.974672,40.783098\n',
                         '2010000001,2010000001,"VTS",1,,"2010-03-14 23:59:10","2011-03-15 00:04:11",4,301,1.1,-73.970610,40.793724,-73.974672,40.783098\n',
                         '2010000001,2010000001,"VTS",1,,"2012-03-14 23:59:10","2011-03-15 00:04:11",4,301,1.1,-73.970610,40.793724,-73.974672,40.783098\n',
                         '2010000001,2010000001,"VTS",1,,"2010-02-14 23:59:10","2011-03-15 00:04:11",4,301,1.1,-73.970610,40.793724,-73.974672,40.783098\n',
                         '2010000001,2010000001,"VTS",1,,"2012-02-14 23:59:10","2011-03-15 00:04:11",4,301,1.1,-73.970610,40.793724,-73.974672,40.783098\n',
                         '2010000001,2010000001,"VTS",1,,"2010-04-14 23:59:10","2011-03-15 00:04:11",4,301,1.1,-73.970610,40.793724,-73.974672,40.783098\n',
                         '2010000001,2010000001,"VTS",1,,"2012-04-14 23:59:10","2011-03-15 00:04:11",4,301,1.1,-73.970610,40.793724,-73.974672,40.783098\n',
                         # Invalid due to zero trip distance, or very short trip distance
                         '2010000001,2010000001,"VTS",1,,"2011-03-14 23:59:10","2011-03-15 01:04:11",4,301,1.1,-73.970610,40.793724,-73.970610,40.793724\n',
                         '2010000001,2010000001,"VTS",1,,"2011-03-14 23:59:10","2011-03-15 01:04:11",4,301,1.1,-73.970610,40.793724,-73.970620,40.793734\n',
                         # Invalid due to high trip speed; long trip l2distance is 9640m; 9.64m in 3 minutes is too fast!
                         '2010000002,2010000002,"VTS",1,,"2011-03-14 22:10:10","2011-03-14 22:13:10",4,180,9.7,-73.954559,40.799313,-74.005135,40.721522\n',
                         # Invalid due to very short trip time; 55s. (~23 m/s)
                         '2010000001,2010000001,"VTS",1,,"2011-03-14 23:59:00","2011-03-14 23:59:55",4,55,1.1,-73.970610,40.793724,-73.974672,40.783098\n',
                         # Invalid due to negative trip time (-115 s!)
                         '2010000001,2010000001,"VTS",1,,"2011-03-14 23:59:55","2011-03-14 23:58:00",4,-55,1.1,-73.970610,40.793724,-73.974672,40.783098\n']
        for line in valid_lines:
            entry = utils.process_entry(line=line, n=4)
            self.assertTrue(utils.check_valid(entry=entry, year=start_year, month=start_month))
        for line in invalid_lines:
            entry = utils.process_entry(line=line, n=4)
            self.assertFalse(utils.check_valid(entry=entry, year=start_year, month=start_month))

class UtilsProcessEntryTest(ut.TestCase):
    def setUp(self):
        self.example_line_1 = '2010000001,2010000001,"VTS",1,,"2011-11-04 13:15:12","2011-11-04 14:10:11",3,34,31.45,-73.96834,40.81703,-73.99632,40.68132\n'
        self.example_line_2 = '2010001927,2010001927,VTS,1,,2011-11-04 13:15:12,2011-11-04 14:10:11,3,18,31.45,-73.96834,40.81703,-73.99632,40.68132\n'
        # Made up entry! Both are the same start time, end time, pcount, and start/end locations except example_line_2 is formatted only a little differently.
        # Trip time are reported incorrectly!
        # Trip distance is recorded as 31.45km for both
        # Corresponds to top-left to bottom-right, 3 passengers, started on the 6555th minute and ended on the 6610th minute;
        # Means, over 55 min, displaced self at 15.27km, which is at most 4.63m/s.
        self.entry_1 = utils.process_entry(line=self.example_line_1, n=12)
        self.entry_2 = utils.process_entry(line=self.example_line_2, n=12)
    
    def tearDown(self):
        pass
    
    def test_example_line_1_and_2(self):
        for entry in [self.entry_1, self.entry_2]:
            self.assertEqual(round(entry['sx'],2), 0)
            self.assertEqual(round(entry['sy'],2), 1)
            self.assertEqual(round(entry['ex'],2), 1)
            self.assertEqual(round(entry['ey'],2), 0)
            self.assertEqual(round(entry['l2distance'], -2), 15300)  # Straight-shot distance in meters
            self.assertEqual(entry['distance'], 31.45)
            self.assertEqual(entry['st'], 546)  # 546th time slot; = floor(((4*24 + 13)*60+15)/n)
            self.assertEqual(entry['et'], 550)  # Same math as above, but for the end time    
            self.assertEqual(entry['syear'],  2011)
            self.assertEqual(entry['smonth'], 11)
            self.assertEqual(entry['sday'],   4)
            self.assertEqual(entry['shour'],  13)
            self.assertEqual(entry['smin'],   15)
            self.assertEqual(entry['ssec'],   12)
            self.assertEqual(entry['eyear'],  2011)
            self.assertEqual(entry['emonth'], 11)
            self.assertEqual(entry['eday'],   4)
            self.assertEqual(entry['ehour'],  14)
            self.assertEqual(entry['emin'],   10)
            self.assertEqual(entry['esec'],   11)
            self.assertEqual(entry['pcount'], 3,)
            self.assertEqual(entry['deltat'], 3299)

class UtilsUpdateDataTest(ut.TestCase):
    def setUp(self):
        self.line_1 = '2010000001,2010000001,"VTS",1,,"2011-03-01 00:00:32","2011-03-01 00:22:44",123,301,1.1,-73.970610,40.793724,-73.974672,40.783098\n'
        # Create an entry and an empty vdata, fdata; update it (w, h = 1 block); make sure the pcount and tcount work right!
        # x,y = 0,0; with n = 4, time slots are 0 and 1. trip count is 1, pcount is 123.
        
        self.line_2 = '2010000002,2010000002,"VTS",1,,"2011-03-01 00:16:12","2011-03-01 00:25:33",61,301,1.1,-73.970610,40.793724,-73.974672,40.783098\n'
        # Similar line, but both are in time slot 1, trip count is 1, pcount is 61
        
        # Parameters:
        self.year, self.month = (2011, 3)
        self.w = 1
        self.h = 1
        self.n = 4
        
        # Data:
        self.entry_1 = utils.process_entry(line=self.line_1, n=self.n)
        self.entry_2 = utils.process_entry(line=self.line_2, n=self.n)
        
        self.vdata = utils.gen_empty_vdata(year=self.year, month=self.month, w=self.w, h=self.h, n=self.n)
        self.fdata = utils.gen_empty_fdata(year=self.year, month=self.month, w=self.w, h=self.h, n=self.n)
        self.vdata_next_mo = utils.gen_empty_vdata(year=self.year, month=self.month, w=self.w, h=self.h, n=self.n)
        self.fdata_next_mo = utils.gen_empty_fdata(year=self.year, month=self.month, w=self.w, h=self.h, n=self.n)
        
        self.trips = np.zeros((2,2,2), dtype=np.int64)
        
    def tearDown(self):
        pass
    
    # Reminders about vdata, fdata, trips format:
    # vdata: (time, x, y, start/end, pcount/tcount)
    # fdata: (same_slot/dif_slots, time,  sx, sy, ex, ey, pcount/tcount)
    # trips: (sin/sout,  ein/eout,  pcount/tcount)
    # Reminder:
    # Entry1: x,y = 0,0; with n = 4, time slots are 0 and 1. trip count is 1, pcount is 123.
    # Entry2: Similar line, but both are in time slot 1, trip count is 1, pcount is 61

    def test_update_data_entry_1(self):
        utils.update_data(entry = self.entry_1,
                          vdata = self.vdata,
                          fdata = self.fdata,
                          vdata_next_mo = self.vdata_next_mo,
                          fdata_next_mo = self.fdata_next_mo,
                          trips = self.trips,
                          w = self.w,
                          h = self.h,
                          n = self.n)
        self.assertEqual(vdata[0,0,0,0,0], 123) # pcount at start
        self.assertEqual(vdata[0,0,0,0,1], 1)   # tcount at start
        self.assertEqual(vdata[1,0,0,0,0], 123) # pcount at end
        self.assertEqual(vdata[1,0,0,0,1], 1)   # tcount at end
        
        self.assertEqual(fdata[0,1,0,0,0,0,0], 0) # Dif time slots, so fdata[0] should be all 0s
        self.assertEqual(fdata[0,1,0,0,0,0,1], 0)
        self.assertEqual(fdata[1,1,0,0,0,0,0], 123) # Dif time slots, we're looking at the end time (t=1)
        self.assertEqual(fdata[1,1,0,0,0,0,1], 1)
        
        self.assertEqual(trips[0,0,0], 123)
        self.assertEqual(trips[0,0,1], 1)
        self.assertEqual(trips[0,1,0], 0)
        self.assertEqual(trips[0,1,1], 0)
        self.assertEqual(trips[1,0,0], 0)
        self.assertEqual(trips[1,0,1], 0)
        self.assertEqual(trips[1,1,0], 0)
        self.assertEqual(trips[1,1,1], 0)
    
    def test_update_data_entry_2(self):
        utils.update_data(entry = self.entry_2,
                      vdata = self.vdata,
                      fdata = self.fdata,
                      vdata_next_mo = self.vdata_next_mo,
                      fdata_next_mo = self.fdata_next_mo,
                      trips = self.trips,
                      w = self.w,
                      h = self.h,
                      n = self.n)
        
        self.assertEqual(vdata[0,0,0,0,0], 0)  # pcount at start
        self.assertEqual(vdata[0,0,0,0,1], 0)  # tcount at start
        self.assertEqual(vdata[1,0,0,0,0], 61) # pcount at end
        self.assertEqual(vdata[1,0,0,0,1], 1)  # tcount at end
        
        self.assertEqual(fdata[0,1,0,0,0,0,0], 61) # Dif time slots, so fdata[0] should be all 0s
        self.assertEqual(fdata[0,1,0,0,0,0,1], 1)
        self.assertEqual(fdata[1,1,0,0,0,0,0], 0) # Dif time slots, we're looking at the end time (t=1)
        self.assertEqual(fdata[1,1,0,0,0,0,1], 0)
        
        self.assertEqual(trips[0,0,0], 61)
        self.assertEqual(trips[0,0,1], 1)
        self.assertEqual(trips[0,1,0], 0)
        self.assertEqual(trips[0,1,1], 0)
        self.assertEqual(trips[1,0,0], 0)
        self.assertEqual(trips[1,0,1], 0)
        self.assertEqual(trips[1,1,0], 0)
        self.assertEqual(trips[1,1,1], 0)
    
    def test_update_data_entry_1_then_entry_2(self):
        utils.update_data(entry = self.entry_1,
              vdata = self.vdata,
              fdata = self.fdata,
              vdata_next_mo = self.vdata_next_mo,
              fdata_next_mo = self.fdata_next_mo,
              trips = self.trips,
              w = self.w,
              h = self.h,
              n = self.n)
        
        utils.update_data(entry = self.entry_2,
                          vdata = self.vdata,
                          fdata = self.fdata,
                          vdata_next_mo = self.vdata_next_mo,
                          fdata_next_mo = self.fdata_next_mo,
                          trips = self.trips,
                          w = self.w,
                          h = self.h,
                          n = self.n)
        
        self.assertEqual(vdata[0,0,0,0,0], 123)  # pcount at start, t=0
        self.assertEqual(vdata[0,0,0,0,1], 1)    # tcount at start, t=0
        self.assertEqual(vdata[1,0,0,0,0], 61)   # pcount at start, t=1
        self.assertEqual(vdata[1,0,0,0,1], 1)    # tcount at start, t=1
        self.assertEqual(vdata[0,0,0,1,0], 0)    # pcount at end, t=0
        self.assertEqual(vdata[0,0,0,1,1], 0)    # tcount at end, t=0
        self.assertEqual(vdata[1,0,0,1,0], 184)  # pcount at end, t=1
        self.assertEqual(vdata[1,0,0,1,1], 2)    # tcount at end, t=1
        
        self.assertEqual(fdata[0,1,0,0,0,0,0], 61)  # Trip 1 (dif time slots, 0 to 1, pcount)
        self.assertEqual(fdata[0,1,0,0,0,0,1], 1)   # Trip 1 (dif time slots, 0 to 1, tcoount)
        self.assertEqual(fdata[1,1,0,0,0,0,0], 123) # Trip 2 (same time slot, t=1, pcount)
        self.assertEqual(fdata[1,1,0,0,0,0,1], 1)   # Trip 2 (same time slot, t=1, pcount)
        
        self.assertEqual(trips[0,0,0], 184) # 184 passengers total, both start in and end in Manhattan
        self.assertEqual(trips[0,0,1], 2)   # 2 trips total, both start in and end in Manhattan
        self.assertEqual(trips[0,1,0], 0)   # No trips (or passengers) starting from or ending in Manhattan
        self.assertEqual(trips[0,1,1], 0)
        self.assertEqual(trips[1,0,0], 0)
        self.assertEqual(trips[1,0,1], 0)
        self.assertEqual(trips[1,1,0], 0)
        self.assertEqual(trips[1,1,1], 0)
        
        # TODO: More extensive tests could be good. (E.g. trips outside manhattan, trips that start outside and end up inside, vice versa, etc.)
    
    def test_update_data_entry_2_then_entry_1(self):
        utils.update_data(entry = self.entry_2,
              vdata = self.vdata,
              fdata = self.fdata,
              vdata_next_mo = self.vdata_next_mo,
              fdata_next_mo = self.fdata_next_mo,
              trips = self.trips,
              w = self.w,
              h = self.h,
              n = self.n)
        
        utils.update_data(entry = self.entry_1,
                          vdata = self.vdata,
                          fdata = self.fdata,
                          vdata_next_mo = self.vdata_next_mo,
                          fdata_next_mo = self.fdata_next_mo,
                          trips = self.trips,
                          w = self.w,
                          h = self.h,
                          n = self.n)
    


all_tests = [GPSUtilsTest,
             UtilsMiscTest,
             UtilsProcessEntryTest,
             UtilsUpdateDataTest]

for test in all_tests:
    ut.TextTestRunner(verbosity=2).run(ut.TestLoader().loadTestsFromTestCase(test))
