from datetime import datetime, time, timedelta
from typing import List, Tuple, Optional

class Event:
    def __init__(self, date: datetime, start_time: datetime, end_time: datetime, description: str):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.description = description

    def __eq__(self, other):
        if not isinstance(other, Event):
            return False
        return (self.date == other.date and
                self.start_time == other.start_time and
                self.end_time == other.end_time and
                self.description == other.description)

    def __hash__(self):
        return hash((self.date, self.start_time, self.end_time, self.description))

class CalendarUtil:
    def __init__(self):
        self.events: List[Event] = []

    def add_event(self, event: Event) -> None:
        self.events.append(event)

    def remove_event(self, event: Event) -> None:
        self.events.remove(event)

    def get_events(self, date: datetime) -> List[Event]:
        return [event for event in self.events if event.date.date() == date.date()]

    def is_available(self, start_time: datetime, end_time: datetime) -> bool:
        for event in self.events:
            # Check if the event overlaps with the given time slot
            if start_time < event.end_time and end_time > event.start_time:
                return False
        return True

    def get_available_slots(self, date: datetime) -> List[Tuple[datetime, datetime]]:
        available_slots = []
        start_time = datetime.combine(date.date(), time.min)
        end_time = datetime.combine(date.date(), time.max)

        # We'll iterate by one hour slots
        current_time = start_time
        while current_time < end_time:
            slot_end_time = current_time + timedelta(hours=1)
            if self.is_available(current_time, slot_end_time):
                available_slots.append((current_time, slot_end_time))
            current_time = slot_end_time

        return available_slots

    def get_upcoming_events(self, num_events: int) -> List[Event]:
        now = datetime.now()
        return [event for event in self.events if event.start_time > now][:num_events]