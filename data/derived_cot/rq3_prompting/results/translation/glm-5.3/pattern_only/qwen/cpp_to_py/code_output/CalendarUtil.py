import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


def _to_utc_timestamp(dt):
    # system_clock semantics: treat naive datetimes as UTC instants
    return dt.replace(tzinfo=timezone.utc).timestamp()


def _localtime_of(dt):
    return time.localtime(_to_utc_timestamp(dt))


@dataclass
class Event:
    date: datetime
    start_time: datetime
    end_time: datetime
    description: str
    # dataclass __eq__ compares all four fields, matching the C++ operator==


class CalendarUtil:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def remove_event(self, event):
        for i, e in enumerate(self.events):
            if e == event:
                del self.events[i]
                break

    def get_events(self, date):
        d = _localtime_of(date)
        d_key = (d.tm_year, d.tm_mon, d.tm_mday)
        events_on_date = []
        for event in self.events:
            t = _localtime_of(event.date)
            if (t.tm_year, t.tm_mon, t.tm_mday) == d_key:
                events_on_date.append(event)
        return events_on_date

    def is_available(self, start_time, end_time):
        for event in self.events:
            if start_time < event.end_time and end_time > event.start_time:
                return False
        return True

    def get_available_slots(self, date):
        available_slots = []
        start_time = date
        end_time = date + timedelta(hours=24) - timedelta(seconds=1)

        while start_time < end_time:
            slot_end_time = start_time + timedelta(hours=1)
            if self.is_available(start_time, slot_end_time):
                available_slots.append((start_time, slot_end_time))
            start_time = slot_end_time

        return available_slots

    def get_upcoming_events(self, num_events):
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        upcoming_events = []
        for event in self.events:
            if event.start_time >= now:
                upcoming_events.append(event)
                if len(upcoming_events) == num_events:
                    break
        return upcoming_events


def time_from_timestamp(timestamp):
    # C++ round-trips through localtime/mktime, which is identity for valid
    # timestamps; result is the time_point for that instant (naive UTC here).
    ts = time.mktime(time.localtime(timestamp))
    return datetime.fromtimestamp(ts, tz=timezone.utc).replace(tzinfo=None)