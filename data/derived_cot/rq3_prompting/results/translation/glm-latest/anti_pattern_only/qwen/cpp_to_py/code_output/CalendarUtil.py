from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Tuple


class CalendarUtil:
    @dataclass
    class Event:
        date: datetime
        start_time: datetime
        end_time: datetime
        description: str

    def __init__(self) -> None:
        self.events: List[Event] = []

    def add_event(self, event: Event) -> None:
        self.events.append(event)

    def remove_event(self, event: Event) -> None:
        try:
            self.events.remove(event)  # removes only the first match, like std::find + erase
        except ValueError:
            pass  # not found: no-op, matching the C++ guard

    def get_events(self, date: datetime) -> List[Event]:
        events_on_date = []
        target_date = date.date()
        for event in self.events:
            if event.date.date() == target_date:
                events_on_date.append(event)
        return events_on_date

    def is_available(self, start_time: datetime, end_time: datetime) -> bool:
        for event in self.events:
            if start_time < event.end_time and end_time > event.start_time:
                return False
        return True

    def get_available_slots(self, date: datetime) -> List[Tuple[datetime, datetime]]:
        available_slots = []
        start_time = date
        end_time = date + timedelta(hours=24) - timedelta(seconds=1)

        while start_time < end_time:
            slot_end_time = start_time + timedelta(hours=1)
            if self.is_available(start_time, slot_end_time):
                available_slots.append((start_time, slot_end_time))
            start_time = slot_end_time

        return available_slots

    def get_upcoming_events(self, num_events: int) -> List[Event]:
        now = datetime.now()
        upcoming_events = []
        for event in self.events:
            if event.start_time >= now:
                upcoming_events.append(event)
                if len(upcoming_events) == num_events:
                    break
        return upcoming_events


def time_from_timestamp(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp)