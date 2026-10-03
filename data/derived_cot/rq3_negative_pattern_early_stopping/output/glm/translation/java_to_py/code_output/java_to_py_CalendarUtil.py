from datetime import datetime, timedelta
from typing import List, Tuple
from itertools import islice


class Event:
    def __init__(self, date: datetime, start_time: datetime, end_time: datetime, description: str):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.description = description

    def __eq__(self, obj):
        if self is obj:
            return True
        if obj is None or type(self) is not type(obj):
            return False
        event = obj
        return (self.date == event.date and
                self.start_time == event.start_time and
                self.end_time == event.end_time and
                self.description == event.description)

    def __hash__(self):
        return hash((self.date, self.start_time, self.end_time, self.description))


class CalendarUtil:
    def __init__(self):
        self.events: List[Event] = []

    def add_event(self, event: Event):
        self.events.append(event)

    def remove_event(self, event: Event):
        try:
            self.events.remove(event)
        except ValueError:
            pass

    def get_events(self, date: datetime) -> List[Event]:
        return [event for event in self.events if event.date.date() == date.date()]

    def is_available(self, start_time: datetime, end_time: datetime) -> bool:
        return not any(start_time < event.end_time and end_time > event.start_time for event in self.events)

    def get_available_slots(self, date: datetime) -> List[Tuple[datetime, datetime]]:
        available_slots: List[Tuple[datetime, datetime]] = []
        
        start_time = date.replace(hour=0, minute=0)
        end_time = date.replace(hour=23, minute=59)

        while start_time < end_time:
            slot_end_time = start_time + timedelta(hours=1)
            if self.is_available(start_time, slot_end_time):
                available_slots.append((start_time, slot_end_time))
            start_time = slot_end_time

        return available_slots

    def get_upcoming_events(self, num_events: int) -> List[Event]:
        now = datetime.now()
        return list(islice((event for event in self.events if event.start_time > now), num_events))