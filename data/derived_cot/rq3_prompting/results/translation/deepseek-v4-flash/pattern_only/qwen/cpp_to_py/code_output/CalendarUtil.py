from datetime import datetime, timezone, timedelta
import copy

class CalendarUtil:
    class Event:
        def __init__(self, date, start_time, end_time, description):
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

    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(copy.copy(event))

    def remove_event(self, event):
        try:
            self.events.remove(event)
        except ValueError:
            pass

    def get_events(self, date):
        events_on_date = []
        date_local = date.astimezone()
        for event in self.events:
            event_date_local = event.date.astimezone()
            if (date_local.year == event_date_local.year and
                date_local.month == event_date_local.month and
                date_local.day == event_date_local.day):
                events_on_date.append(copy.copy(event))
        return events_on_date

    def is_available(self, start_time, end_time):
        for event in self.events:
            if start_time < event.end_time and end_time > event.start_time:
                return False
        return True

    def get_available_slots(self, date):
        available_slots = []
        start_time = date
        end_time = date + timedelta(hours=24) - timedelta(seconds=1)
        while start_time < end_time:
            slot_end_time = start_time + timedelta(hours=1)
            if self.is_available(start_time, slot_end_time):
                available_slots.append((start_time, slot_end_time))
            start_time = slot_end_time
        return available_slots

    def get_upcoming_events(self, num_events):
        num_events = int(num_events)
        now = datetime.now(timezone.utc)
        upcoming_events = []
        for event in self.events:
            if event.start_time >= now:
                upcoming_events.append(copy.copy(event))
                if len(upcoming_events) == num_events:
                    break
        return upcoming_events

def time_from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)