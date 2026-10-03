import datetime
from typing import List, Tuple


class CalendarUtil:
    class Event:
        def __init__(self, date: datetime.datetime, start_time: datetime.datetime,
                     end_time: datetime.datetime, description: str):
            self.date = date
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

        def __hash__(self):
            return hash((self.date, self.start_time, self.end_time, self.description))

    def __init__(self):
        self.events: List[CalendarUtil.Event] = []

    def add_event(self, event: 'CalendarUtil.Event') -> None:
        self.events.append(event)

    def remove_event(self, event: 'CalendarUtil.Event') -> None:
        try:
            self.events.remove(event)
        except ValueError:
            pass

    def get_events(self, date: datetime.datetime) -> List['CalendarUtil.Event']:
        events_on_date = []
        for event in self.events:
            if (date.year == event.date.year and
                    date.month == event.date.month and
                    date.day == event.date.day):
                events_on_date.append(event)
        return events_on_date

    def is_available(self, start_time: datetime.datetime,
                     end_time: datetime.datetime) -> bool:
        for event in self.events:
            if start_time < event.end_time and end_time > event.start_time:
                return False
        return True

    def get_available_slots(self, date: datetime.datetime) -> List[Tuple[datetime.datetime, datetime.datetime]]:
        available_slots = []
        start_time = date
        end_time = date + datetime.timedelta(hours=24) - datetime.timedelta(seconds=1)

        while start_time < end_time:
            slot_end_time = start_time + datetime.timedelta(hours=1)
            if self.is_available(start_time, slot_end_time):
                available_slots.append((start_time, slot_end_time))
            start_time = slot_end_time

        return available_slots

    def get_upcoming_events(self, num_events: int) -> List['CalendarUtil.Event']:
        now = datetime.datetime.now()
        upcoming_events = []
        for event in self.events:
            if event.start_time >= now:
                upcoming_events.append(event)
                if len(upcoming_events) == num_events:
                    break
        return upcoming_events


def time_from_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)