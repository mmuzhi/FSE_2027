from datetime import datetime, timedelta


class Event:
    def __init__(self, date, start_time, end_time, description):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.description = description

    def __eq__(self, other):
        if self is other:
            return True
        if other is None or type(self) is not type(other):
            return False
        return (self.date == other.date and
                self.start_time == other.start_time and
                self.end_time == other.end_time and
                self.description == other.description)

    def __hash__(self):
        return hash((self.date, self.start_time, self.end_time, self.description))


class CalendarUtil:
    def __init__(self):
        self.events = []

    def addEvent(self, event):
        self.events.append(event)

    def removeEvent(self, event):
        if event in self.events:
            self.events.remove(event)

    def getEvents(self, date):
        return [event for event in self.events if event.date.date() == date.date()]

    def isAvailable(self, start_time, end_time):
        return not any(start_time < event.end_time and end_time > event.start_time
                       for event in self.events)

    def getAvailableSlots(self, date):
        available_slots = []
        start_time = date.replace(hour=0, minute=0)
        end_time = date.replace(hour=23, minute=59)

        while start_time < end_time:
            slot_end_time = start_time + timedelta(hours=1)
            if self.isAvailable(start_time, slot_end_time):
                available_slots.append((start_time, slot_end_time))
            start_time = slot_end_time

        return available_slots

    def getUpcomingEvents(self, num_events):
        if num_events < 0:
            raise ValueError("num_events must be non-negative")
        now = datetime.now()
        upcoming = [event for event in self.events if event.start_time > now]
        return upcoming[:num_events]