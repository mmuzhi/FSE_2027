import datetime as dt
import time

class Event:
    __slots__ = ('date', 'start_time', 'end_time', 'description')
    
    def __init__(self, date, start_time, end_time, description):
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
        events_on_date = []
        for event in self.events:
            if event.date.date() == date.date():
                events_on_date.append(event)
        return events_on_date
    
    def is_available(self, start_time, end_time):
        for event in self.events:
            if start_time < event.end_time and end_time > event.start_time:
                return False
        return True
    
    def get_available_slots(self, date):
        start_time = dt.datetime.combine(date.date(), dt.time.min)
        end_time = start_time + dt.timedelta(days=1) - dt.timedelta(seconds=1)
        available_slots = []
        current = start_time
        
        while current < end_time:
            slot_end = current + dt.timedelta(hours=1)
            if self.is_available(current, slot_end):
                available_slots.append((current, slot_end))
            current = slot_end
        
        return available_slots
    
    def get_upcoming_events(self, num_events):
        now = dt.datetime.now()
        upcoming_events = []
        for event in self.events:
            if event.start_time >= now:
                upcoming_events.append(event)
                if len(upcoming_events) == num_events:
                    break
        return upcoming_events

def time_from_timestamp(timestamp):
    return dt.datetime.fromtimestamp(timestamp)