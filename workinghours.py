#-*- coding_ utf-8 -*-
from datetime import datetime, date, timedelta


MON, TUE, WED, THU, FRI, SAT, SUN = range(7)


class WorkingHours:
    """
    This class help you calculate the working hours between two days. You can
    define your own parameters for WORK_TIMING, LUNCH_TIME, WEEKENDS and
    HOLIDAYS.
    """
    WORK_TIMING = {
        MON: (9, 18.5),
        TUE: (9, 18.5),
        WED: (9, 18.5),
        THU: (9, 18.5),
        FRI: (9, 18.5),
    }
    LUNCH_TIME = [13, 14]
    WEEKENDS = (SAT, SUN)
    HOLIDAYS = [
        (12, 25) # Christmas!
    ]

    def __init__(self, date1, date2, work_timing=WORK_TIMING,
                 lunch_time=LUNCH_TIME, weekends=WEEKENDS, holidays=HOLIDAYS):
        self.date1 = date1
        self.date2 = date2
        self.work_timing = work_timing
        self.lunch_time = lunch_time
        self.weekends = weekends
        self.holidays = self._get_holidays(holidays)

    def _get_holidays(self, holidays):
        """
        Returns a list of date objects from holidays
        """
        year = date.today().year
        return [date(year, holiday[0], holiday[1]) for holiday in holidays]

    def _get_ordered_dates(self, date1, date2):
        """
        Returns (start, end) dates
        """
        if date1 > date2:
            return (date2, date1)
        return (date1, date2)

    def _get_working_time_by_weekday(self, weekday):
        """
        Returns the working time for a day
        """
        if weekday in self.weekends:
            return self.work_timing[MON]
        return self.work_timing[weekday]

    def _get_hours_per_day(self, work_time):
        """
        Returns the total hours of a given work time
        """
        if work_time[1] <= self.lunch_time[0] or work_time[0] >= self.lunch_time[1]:
            return work_time[1] - work_time[0]

        return (self.lunch_time[0] - work_time[0]) + (work_time[1] - self.lunch_time[1])

    def get_hours(self):
        """
        Returns the total hours between two dates
        """
        total_hours = 0

        if self.date1 == self.date2:
            return total_hours

        start, end = self._get_ordered_dates(self.date1, self.date2)
        start_hour = start.time().hour + round(start.time().minute / 60.0, 2)
        end_hour = end.time().hour + round(end.time().minute / 60.0, 2)
        days = (end - start).days

        if start.date() == end.date():
            work_time = (start_hour, end_hour)
            total_hours += self._get_hours_per_day(work_time)
        else:
            start_wt = self._get_working_time_by_weekday(start.weekday())
            end_wt = self._get_working_time_by_weekday(end.weekday())
            work_times = (
                (start_hour, start_wt[1]),
                (end_wt[0], end_hour)
            )
            for wt in work_times:
                total_hours += self._get_hours_per_day(wt)

        if days:
            temp = start

            if end.time() > start.time():
                days -= 1

            while days:
                days -= 1
                temp = temp + timedelta(days=1)

                if temp.weekday() in self.weekends or temp.date() in self.holidays:
                    continue

                work_time = self._get_working_time_by_weekday(temp.weekday())
                hours_per_day = self._get_hours_per_day(work_time)
                total_hours += hours_per_day

        return total_hours


if __name__ == '__main__':
    # Simple test
    date1 = datetime(2013, 12, 23, 9, 0)
    date2 = datetime(2013, 12, 31, 16, 0)

    wh = WorkingHours(date1, date2)
    hours = wh.get_hours()
    print hours
