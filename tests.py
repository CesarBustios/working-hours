#-*- coding: utf-8 -*-
import unittest
from datetime import datetime

from workinghours import *


class TestWeekends(unittest.TestCase):
    def setUp(self):
        self.date1 = datetime.now()
        self.date2 = datetime.now()

    def test_standard_weekend(self):
        work_timing = {
            MON: (9, 18),
            TUE: (9, 18),
            WED: (9, 18),
            THU: (9, 18),
            FRI: (9, 18),
        }
        wh = WorkingHours(self.date1, self.date2, work_timing)

        self.assertEqual(wh.weekend, [SAT, SUN])

    def test_long_weekend(self):
        work_timing = {
            MON: (9, 17),
            WED: (9, 17),
            FRI: (9, 17),
        }
        wh = WorkingHours(self.date1, self.date2, work_timing)

        self.assertEqual(wh.weekend, [TUE, THU, SAT, SUN])

    def test_duplicated_work_timing_weekend(self):
        work_timing = {
            MON: (9, 17),
            MON: (9, 17),
            TUE: (9, 17),
            WED: (9, 17),
            WED: (9, 17),
            WED: (9, 17),
            THU: (9, 17),
            FRI: (9, 17),
            FRI: (9, 17),
            SAT: (9, 12),
            SAT: (9, 12),
            SAT: (9, 12),
        }
        wh = WorkingHours(self.date1, self.date2, work_timing)

        self.assertEqual(wh.weekend, [SUN])



class TestWorkingHours(unittest.TestCase):
    def setUp(self):
        self.work_timing = {
            MON: (9, 17),
            TUE: (9, 17),
            WED: (9, 17),
            THU: (9, 17),
            FRI: (9, 17),
            SAT: (9, 12),
        }

    def test_weekend(self):
        date1 = datetime(2013, 1, 23, 9, 0)
        date2 = datetime(2013, 1, 23, 10, 0)
        wh = WorkingHours(date1, date2, self.work_timing)

        self.assertEqual(wh.weekend, [SUN])

    def test_same_dates(self):
        date1 = datetime(2013, 1, 22, 12, 8)
        wh = WorkingHours(date1, date1)

        self.assertEqual(wh.get_hours(), 0)

    def test_same_day(self):
        date1 = datetime(2013, 1, 23, 9, 30)
        date2 = datetime(2013, 1, 23, 16, 0)
        wh = WorkingHours(date1, date2, self.work_timing)

        self.assertEqual(wh.get_hours(), 5.5)

    def test_same_day_begin_in_lunch(self):
        date1 = datetime(2013, 1, 23, 13, 30)
        date2 = datetime(2013, 1, 23, 17, 0)
        wh = WorkingHours(date1, date2, self.work_timing)

        self.assertEqual(wh.get_hours(), 3.5)

    def test_same_day_end_in_lunch(self):
        date1 = datetime(2013, 1, 23, 10, 0)
        date2 = datetime(2013, 1, 23, 13, 30)
        wh = WorkingHours(date1, date2, self.work_timing)

        self.assertEqual(wh.get_hours(), 3.5)

    # TODO: Implement some "strict" behaviour for fixed hours
    # def test_date_below_wt(self):
        # 8AM should be considered as 9AM according to custom work time
        # date1 = datetime(2013, 1, 22, 8, 0)
        # date2 = datetime(2013, 1, 23, 12, 0)
        # wh = WorkingHours(date1, date2, self.work_timing)

        # self.assertEqual(wh.get_hours(), 10)


if __name__ == '__main__':
    unittest.main()
