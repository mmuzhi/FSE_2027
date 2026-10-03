#include <iostream>
#include <unordered_map>
#include <string>

class Hotel {
private:
    std::string name;
    std::unordered_map<std::string, int> availableRooms;
    std::unordered_map<std::string, std::unordered_map<std::string, int>> bookedRooms;

public:
    Hotel(const std::string& name, const std::unordered_map<std::string, int>& rooms)
        : name(name), availableRooms(rooms) {
        // Initialize bookedRooms with empty maps for each room type if needed
        for (const auto& entry : availableRooms) {
            bookedRooms[entry.first]; // Force creation of an empty map for each room type
        }
    }

    std::string bookRoom(const std::string& roomType, int roomNumber, const std::string& name) {
        if (!availableRooms.count(roomType)) {
            return "False";
        }

        int available = availableRooms.at(roomType);
        if (roomNumber <= available) {
            bookedRooms[roomType][name] = roomNumber;
            availableRooms[roomType] = available - roomNumber;
            return "Success!";
        } else {
            return "False";
        }
    }

    bool checkIn(const std::string& roomType, int roomNumber, const std::string& name) {
        auto& bookingMap = bookedRooms[roomType];
        auto it = bookingMap.find(name);
        if (it == bookingMap.end()) {
            return false;
        }

        int booked = it->second;
        if (roomNumber > booked) {
            return false;
        } else if (roomNumber == booked) {
            bookingMap.erase(it);
        } else {
            bookingMap[name] = booked - roomNumber;
        }
        return true;
    }

    void checkOut(const std::string& roomType, int roomNumber) {
        availableRooms[roomType] += roomNumber;
    }

    int getAvailableRooms(const std::string& roomType) const {
        auto it = availableRooms.find(roomType);
        return it != availableRooms.end() ? it->second : 0;
    }
};

int main() {
    std::unordered_map<std::string, int> rooms;
    rooms["single"] = 3;
    rooms["double"] = 2;
    Hotel hotel("Test Hotel", rooms);

    std::cout << hotel.bookRoom("single", 2, "guest 1") << std::endl;
    std::cout << hotel.bookRoom("triple", 2, "guest 1") << std::endl;
    std::cout << hotel.bookRoom("single", 2, "guest 2") << std::endl;
    std::cout << hotel.bookRoom("single", 1, "guest 2") << std::endl;
    std::cout << hotel.bookRoom("single", 3, "guest 1") << std::endl;
    std::cout << hotel.bookRoom("single", 100, "guest 1") << std::endl;

    hotel.checkIn("single", 1, "guest 1");
    std::cout << "Booked Rooms: ";
    for (const auto& entry : hotel.bookedRooms["single"]) {
        std::cout << entry.first << ": " << entry.second << " ";
    }
    std::cout << std::endl;

    std::cout << hotel.checkIn("single", 3, "guest 1") << std::endl;
    std::cout << hotel.checkIn("double", 1, "guest 1") << std::endl;
    hotel.checkIn("double", 1, "guest 2");
    std::cout << "Booked Rooms: ";
    for (const auto& entry : hotel.bookedRooms["double"]) {
        std::cout << entry.first << ": " << entry.second << " ";
    }
    std::cout << std::endl;

    hotel.checkOut("single", 1);
    std::cout << "Available Rooms: single=" << hotel.getAvailableRooms("single") << std::endl;
    hotel.checkOut("triple", 2);
    std::cout << "Available Rooms: triple=" << hotel.getAvailableRooms("triple") << std::endl;

    std::cout << "Available single rooms: " << hotel.getAvailableRooms("single") << std::endl;

    return 0;
}