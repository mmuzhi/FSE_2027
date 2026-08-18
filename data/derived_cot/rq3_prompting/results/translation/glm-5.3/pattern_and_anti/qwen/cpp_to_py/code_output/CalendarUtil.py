from dataclasses import dataclass
from datetime import datetime, timedelta


class CalendarUtil:
    @dataclass
    class Event:
        date: datetime
        start_time: datetime
        end_time: datetime
        description: str

        def __eq__(self, other):
            if not isinstance(other, CalendarUtil.Event):
                return NotImplemented
            return (self.date == other.date and
                    self.start_time == other.start_time and
                    self.end_time == other.end_time and
                    self.description == other.description)

    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def remove_event(self, event):
        if event in self.events:
            self.events.remove(event)

    def get_events(self, date):
        events_on_date = []
        for event in self.events:
            if (date.year == event.date.year and
                    date.month == event.date.month and
                    date.day == event.date.day):
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
        end_time = date + timedelta(hours=24, seconds=-1)

        while start_time < end_time:
            slot_end_time = start_time + timedelta(hours=1)
            if self.is_available(start_time, slot_end_time):
                available_slots.append((start_time, slot_end_time))
            start_time = slot_end_time

        return available_slots

    def get_upcoming_events(self, num_events):
        now = datetime.now()
        upcoming_events = []
        for event in self.events:
            if event.start_time >= now:
                upcoming_events.append(event)
                if len(upcoming_events) == num_events:
                    break
        return upcoming_events


def time_from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp)