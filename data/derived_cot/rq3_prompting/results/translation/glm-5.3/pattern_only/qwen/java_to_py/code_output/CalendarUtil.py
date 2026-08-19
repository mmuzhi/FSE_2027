from datetime import datetime, timedelta
from itertools import islice


class Event:
    def __init__(self, date, start_time, end_time, description):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.description = description

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, Event):
            return False
        return (self.date == other.date
                and self.start_time == other.start_time
                and self.end_time == other.end_time
                and self.description == other.description)

    def __hash__(self):
        return hash((self.date, self.start_time, self.end_time, self.description))


class CalendarUtil:
    def __init__(self):
        self.events = []

    def addEvent(self, event):
        self.events.append(event)

    def removeEvent(self, event):
        # Java's List.remove(Object) is a no-op when absent; suppress Python's ValueError.
        try:
            self.events.remove(event)
        except ValueError:
            pass

    def getEvents(self, date):
        return [event for event in self.events if event.date.date() == date.date()]

    def isAvailable(self, start_time, end_time):
        return not any(start_time < event.end_time and end_time > event.start_time
                       for event in self.events)

    def getAvailableSlots(self, date):
        available_slots = []
        # replace() keeps second/microsecond, matching Java withHour().withMinute().
        start_time = date.replace(hour=0, minute=0)
        end_time = date.replace(hour=23, minute=59)

        while start_time < end_time:
            slot_end_time = start_time + timedelta(hours=1)
            if self.isAvailable(start_time, slot_end_time):
                available_slots.append((start_time, slot_end_time))
            start_time = slot_end_time

        return available_slots

    def getUpcomingEvents(self, num_events):
        now = datetime.now()
        # islice mirrors stream.limit(): caps at num_events, raises on negative input.
        return list(islice((event for event in self.events if event.start_time > now), num_events))