from datetime import datetime, timezone, timedelta
import copy


def _to_utc(dt):
    return dt.astimezone(timezone.utc)


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
            return (
                _to_utc(self.date) == _to_utc(other.date)
                and _to_utc(self.start_time) == _to_utc(other.start_time)
                and _to_utc(self.end_time) == _to_utc(other.end_time)
                and self.description == other.description
            )

        def __repr__(self):
            return (
                f"Event(date={self.date!r}, start_time={self.start_time!r}, "
                f"end_time={self.end_time!r}, description={self.description!r})"
            )

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
        date_utc = _to_utc(date)
        local_date = date_utc.astimezone()

        for event in self.events:
            event_date_utc = _to_utc(event.date)
            event_local = event_date_utc.astimezone()
            if (
                local_date.year == event_local.year
                and local_date.month == event_local.month
                and local_date.day == event_local.day
            ):
                events_on_date.append(copy.copy(event))

        return events_on_date

    def is_available(self, start_time, end_time):
        start_utc = _to_utc(start_time)
        end_utc = _to_utc(end_time)

        for event in self.events:
            event_start_utc = _to_utc(event.start_time)
            event_end_utc = _to_utc(event.end_time)
            if start_utc < event_end_utc and end_utc > event_start_utc:
                return False

        return True

    def get_available_slots(self, date):
        available_slots = []
        start_time = _to_utc(date)
        end_time = start_time + timedelta(hours=24) - timedelta(seconds=1)

        while start_time < end_time:
            slot_end_time = start_time + timedelta(hours=1)
            if self.is_available(start_time, slot_end_time):
                available_slots.append((start_time, slot_end_time))
            start_time = slot_end_time

        return available_slots

    def get_upcoming_events(self, num_events):
        now = datetime.now(timezone.utc)
        upcoming_events = []

        for event in self.events:
            event_start_utc = _to_utc(event.start_time)
            if event_start_utc >= now:
                upcoming_events.append(copy.copy(event))
                if len(upcoming_events) == num_events:
                    break

        return upcoming_events


def time_from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)