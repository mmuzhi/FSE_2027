class Hotel:
    def __init__(self, name, rooms):
        self.name = name
        self.available_rooms = dict(rooms)
        self.booked_rooms = {}

    def bookRoom(self, room_type, room_number, name):
        if room_type not in self.available_rooms:
            return "False"
        available = self.available_rooms[room_type]
        if room_number <= available:
            self.booked_rooms.setdefault(room_type, {})[name] = room_number
            self.available_rooms[room_type] = available - room_number
            return "Success!"
        else:
            return "False"

    def checkIn(self, room_type, room_number, name):
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

    def checkOut(self, room_type, room_number):
        self.available_rooms[room_type] = self.available_rooms.get(room_type, 0) + room_number

    def getAvailableRooms(self, room_type):
        return self.available_rooms.get(room_type, 0)

if __name__ == "__main__":
    rooms = {"single": 3, "double": 2}
    hotel = Hotel("Test Hotel", rooms)

    print(hotel.bookRoom("single", 2, "guest 1"))
    print(hotel.bookRoom("triple", 2, "guest 1"))
    print(hotel.bookRoom("single", 2, "guest 2"))
    print(hotel.bookRoom("single", 1, "guest 2"))
    print(hotel.bookRoom("single", 3, "guest 1"))
    print(hotel.bookRoom("single", 100, "guest 1"))

    hotel.checkIn("single", 1, "guest 1")
    print(hotel.booked_rooms)
    print(hotel.checkIn("single", 3, "guest 1"))
    print(hotel.checkIn("double", 1, "guest 1"))
    hotel.checkIn("double", 1, "guest 2")
    print(hotel.booked_rooms)

    hotel.checkOut("single", 1)
    print(hotel.available_rooms)
    hotel.checkOut("triple", 2)
    print(hotel.available_rooms)

    print(hotel.getAvailableRooms("single"))