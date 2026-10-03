from datetime import datetime, timedelta, date, time
from typing import List, Tuple
import sys

class CalendarUtil:
    class Event:
        def __init__(self, date_time: datetime, start_time: datetime, end_time: datetime, description: str):
            self.date = date_time
            self.start_time = start_time
            self.end_time = end_time
            self.description = description

        def __eq__(self, other):
            if not isinstance(other, CalendarUtil.Event):
                return NotImplemented
            return (self.date == other.date and
                    self.start_time == other.start_time and
                    self.end_time == other.end_time and
                    self.description == other.description)

        def __repr__(self):
            return f"Event(date={self.date}, start={self.start_time}, end={self.end_time}, desc={self.description})"

    def __init__(self):
        self.events: List[CalendarUtil.Event] = []

    def add_event(self, event: Event) -> None:
        self.events.append(event)

    def remove_event(self, event: Event) -> None:
        try:
            self.events.remove(event)
        except ValueError:
            pass  # event not found, do nothing (matching C++ behavior)

    def get_events(self, date: datetime) -> List[Event]:
        events_on_date = []
        for ev in self.events:
            if (ev.date.year == date.year and
                ev.date.month == date.month and
                ev.date.day == date.day):
                events_on_date.append(ev)
        return events_on_date

    def is_available(self, start_time: datetime, end_time: datetime) -> bool:
        for ev in self.events:
            if start_time < ev.end_time and end_time > ev.start_time:
                return False
        return True

    def get_available_slots(self, date: datetime) -> List[Tuple[datetime, datetime]]:
        slots = []
        slot_start = date
        day_end = date + timedelta(hours=24) - timedelta(seconds=1)
        while slot_start < day_end:
            slot_end = slot_start + timedelta(hours=1)
            if self.is_available(slot_start, slot_end):
                slots.append((slot_start, slot_end))
            slot_start = slot_end
        return slots

    def get_upcoming_events(self, num_events: int) -> List[Event]:
        now = datetime.now()  # local time
        upcoming = []
        for ev in self.events:
            if ev.start_time >= now:
                upcoming.append(ev)
                if len(upcoming) == num_events:
                    break
        return upcoming

def time_from_timestamp(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp)