import datetime
from typing import List, Tuple


class Event:
    def __init__(self, date: datetime.datetime, start_time: datetime.datetime,
                 end_time: datetime.datetime, description: str):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.description = description

    def __eq__(self, other):
        if not isinstance(other, Event):
            return NotImplemented
        return (self.date == other.date and
                self.start_time == other.start_time and
                self.end_time == other.end_time and
                self.description == other.description)

    def __hash__(self):
        return hash((self.date, self.start_time, self.end_time, self.description))


class CalendarUtil:
    def __init__(self):
        self.events: List[Event] = []

    def addEvent(self, event: Event) -> None:
        self.events.append(event)

    def removeEvent(self, event: Event) -> None:
        self.events.remove(event)

    def getEvents(self, date: datetime.datetime) -> List[Event]:
        return [e for e in self.events if e.date.date() == date.date()]

    def isAvailable(self, start_time: datetime.datetime, end_time: datetime.datetime) -> bool:
        return not any(
            start_time < e.end_time and end_time > e.start_time
            for e in self.events
        )

    def getAvailableSlots(self, date: datetime.datetime) -> List[Tuple[datetime.datetime, datetime.datetime]]:
        slots = []
        start_time = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = date.replace(hour=23, minute=59, second=0, microsecond=0)
        while start_time < end_time:
            slot_end = start_time + datetime.timedelta(hours=1)
            if self.isAvailable(start_time, slot_end):
                slots.append((start_time, slot_end))
            start_time = slot_end
        return slots

    def getUpcomingEvents(self, num_events: int) -> List[Event]:
        now = datetime.datetime.now()
        return [e for e in self.events if e.start_time > now][:num_events]