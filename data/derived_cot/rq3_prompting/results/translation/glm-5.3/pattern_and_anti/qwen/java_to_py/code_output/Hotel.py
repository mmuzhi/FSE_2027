class Hotel:
    def __init__(self, name, rooms):
        self.name = name
        self.available_rooms = dict(rooms)  # defensive copy, like new HashMap<>(rooms)
        self.booked_rooms = {}

    def book_room(self, room_type, room_number, name):
        if room_type not in self.available_rooms:
            return "False"

        available = self.available_rooms[room_type]
        if room_number <= available:
            self.booked_rooms.setdefault(room_type, {})  # putIfAbsent equivalent
            self.booked_rooms[room_type][name] = room_number
            self.available_rooms[room_type] = available - room_number
            return "Success!"
        else:
            return "False"

    def check_in(self, room_type, room_number, name):
        if room_type not in self.booked_rooms or name not in self.booked_rooms[room_type]:
            return False

        booked = self.booked_rooms[room_type][name]
        if room_number > booked:
            return False
        elif room_number == booked:
            del self.booked_rooms[room_type][name]
        else:
            self.booked_rooms[room_type][name] = booked - room_number
        return True

    def check_out(self, room_type, room_number):
        self.available_rooms[room_type] = self.available_rooms.get(room_type, 0) + room_number

    def get_available_rooms(self, room_type):
        return self.available_rooms.get(room_type, 0)


def main():
    rooms = {"single": 3, "double": 2}
    hotel = Hotel("Test Hotel", rooms)

    print(hotel.book_room("single", 2, "guest 1"))
    print(hotel.book_room("triple", 2, "guest 1"))
    print(hotel.book_room("single", 2, "guest 2"))
    print(hotel.book_room("single", 1, "guest 2"))
    print(hotel.book_room("single", 3, "guest 1"))
    print(hotel.book_room("single", 100, "guest 1"))

    hotel.check_in("single", 1, "guest 1")
    print(hotel.booked_rooms)
    print(hotel.check_in("single", 3, "guest 1"))
    print(hotel.check_in("double", 1, "guest 1"))
    hotel.check_in("double", 1, "guest 2")
    print(hotel.booked_rooms)

    hotel.check_out("single", 1)
    print(hotel.available_rooms)
    hotel.check_out("triple", 2)
    print(hotel.available_rooms)

    print(hotel.get_available_rooms("single"))


if __name__ == "__main__":
    main()