#include <iostream>
#include <string>
#include <unordered_map>

class Hotel {
private:
    std::string name;
    std::unordered_map<std::string, int> availableRooms;
    std::unordered_map<std::string, std::unordered_map<std::string, int>> bookedRooms;

public:
    Hotel(const std::string& name, const std::unordered_map<std::string, int>& rooms)
        : name(name), availableRooms(rooms) {}

    std::string bookRoom(const std::string& roomType, int roomNumber, const std::string& guestName) {
        auto it = availableRooms.find(roomType);
        if (it == availableRooms.end()) {
            return "False";
        }
        int available = it->second;
        if (roomNumber <= available) {
            // Ensure inner map exists
            auto& inner = bookedRooms[roomType]; // inserts if absent
            inner[guestName] = roomNumber;
            availableRooms[roomType] = available - roomNumber;
            return "Success!";
        } else {
            return "False";
        }
    }

    bool checkIn(const std::string& roomType, int roomNumber, const std::string& guestName) {
        auto outerIt = bookedRooms.find(roomType);
        if (outerIt == bookedRooms.end()) {
            return false;
        }
        auto& inner = outerIt->second;
        auto innerIt = inner.find(guestName);
        if (innerIt == inner.end()) {
            return false;
        }
        int booked = innerIt->second;
        if (roomNumber > booked) {
            return false;
        } else if (roomNumber == booked) {
            inner.erase(innerIt);
        } else {
            inner[guestName] = booked - roomNumber;
        }
        return true;
    }

    void checkOut(const std::string& roomType, int roomNumber) {
        availableRooms[roomType] += roomNumber;
    }

    int getAvailableRooms(const std::string& roomType) {
        auto it = availableRooms.find(roomType);
        if (it == availableRooms.end()) {
            return 0;
        }
        return it->second;
    }

    // Helper for printing map (used in main)
    static void printMap(const std::unordered_map<std::string, int>& m) {
        std::cout << "{";
        bool first = true;
        for (const auto& p : m) {
            if (!first) std::cout << ", ";
            first = false;
            std::cout << p.first << "=" << p.second;
        }
        std::cout << "}";
    }

    static void printBookedRooms(const std::unordered_map<std::string, std::unordered_map<std::string, int>>& booked) {
        std::cout << "{";
        bool first = true;
        for (const auto& p : booked) {
            if (!first) std::cout << ", ";
            first = false;
            std::cout << p.first << "={";
            bool innerFirst = true;
            for (const auto& inner : p.second) {
                if (!innerFirst) std::cout << ", ";
                innerFirst = false;
                std::cout << inner.first << "=" << inner.second;
            }
            std::cout << "}";
        }
        std::cout << "}";
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
    Hotel::printBookedRooms(hotel.bookedRooms);
    std::cout << std::endl;
    std::cout << (hotel.checkIn("single", 3, "guest 1") ? "1" : "0") << std::endl;
    std::cout << (hotel.checkIn("double", 1, "guest 1") ? "1" : "0") << std::endl;
    hotel.checkIn("double", 1, "guest 2");
    Hotel::printBookedRooms(hotel.bookedRooms);
    std::cout << std::endl;

    hotel.checkOut("single", 1);
    Hotel::printMap(hotel.availableRooms);
    std::cout << std::endl;
    hotel.checkOut("triple", 2);
    Hotel::printMap(hotel.availableRooms);
    std::cout << std::endl;

    std::cout << hotel.getAvailableRooms("single") << std::endl;

    return 0;
}