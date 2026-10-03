class Hotel:
    def __init__(self, name, rooms):
        self.name = name
        self.availableRooms = dict(rooms)
        self.bookedRooms = {}

    def bookRoom(self, roomType, roomNumber, name):
        if roomType not in self.availableRooms:
            return "False"
        available = self.availableRooms[roomType]
        if roomNumber <= available:
            if roomType not in self.bookedRooms:
                self.bookedRooms[roomType] = {}
            self.bookedRooms[roomType][name] = roomNumber
            self.availableRooms[roomType] = available - roomNumber
            return "Success!"
        else:
            return "False"

    def checkIn(self, roomType, roomNumber, name):
        if roomType not in self.bookedRooms or name not in self.bookedRooms[roomType]:
            return False
        booked = self.bookedRooms[roomType][name]
        if roomNumber > booked:
            return False
        elif roomNumber == booked:
            del self.bookedRooms[roomType][name]
        else:
            self.bookedRooms[roomType][name] = booked - roomNumber
        return True

    def checkOut(self, roomType, roomNumber):
        self.availableRooms[roomType] = self.availableRooms.get(roomType, 0) + roomNumber

    def getAvailableRooms(self, roomType):
        return self.availableRooms.get(roomType, 0)


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
    print(hotel.bookedRooms)
    print(hotel.checkIn("single", 3, "guest 1"))
    print(hotel.checkIn("double", 1, "guest 1"))
    hotel.checkIn("double", 1, "guest 2")
    print(hotel.bookedRooms)

    hotel.checkOut("single", 1)
    print(hotel.availableRooms)
    hotel.checkOut("triple", 2)
    print(hotel.availableRooms)

    print(hotel.getAvailableRooms("single"))