class Hotel:
    def __init__(self, name: str, rooms: dict):
        self.name = name
        self.available_rooms = rooms.copy()  # keep a copy to avoid external mutation
        self.booked_rooms = {}  # room_type -> {name: room_number}

    def book_room(self, room_type: str, room_number: int, name: str) -> str:
        if room_type not in self.available_rooms:
            return "False."

        available = self.available_rooms[room_type]
        if room_number <= available:
            if room_type not in self.booked_rooms:
                self.booked_rooms[room_type] = {}
            self.booked_rooms[room_type][name] = room_number
            self.available_rooms[room_type] -= room_number
            return "Success!"
        elif available != 0:
            return str(available)
        else:
            return "False."

    def check_in(self, room_type: str, room_number: int, name: str) -> bool:
        if room_type not in self.booked_rooms:
            return False

        if name in self.booked_rooms[room_type]:
            booked = self.booked_rooms[room_type][name]
            if room_number > booked:
                return False
            elif room_number == booked:
                del self.booked_rooms[room_type][name]
                if not self.booked_rooms[room_type]:
                    del self.booked_rooms[room_type]
            else:
                self.booked_rooms[room_type][name] -= room_number
            return True
        return False

    def check_out(self, room_type: str, room_number: int) -> None:
        if room_type in self.available_rooms:
            self.available_rooms[room_type] += room_number
        else:
            self.available_rooms[room_type] = room_number

    def get_available_rooms(self, room_type: str) -> int:
        return self.available_rooms.get(room_type, 0)