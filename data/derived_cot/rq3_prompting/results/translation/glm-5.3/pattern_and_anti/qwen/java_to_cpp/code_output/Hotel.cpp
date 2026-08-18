#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>

class Hotel {
private:
    std::string name;

public:
    std::unordered_map<std::string, int> availableRooms;
    std::unordered_map<std::string, std::unordered_map<std::string, int>> bookedRooms;

    Hotel(const std::string& name, const std::unordered_map<std::string, int>& rooms)
        : name(name), availableRooms(rooms), bookedRooms() {}

    std::string bookRoom(const std::string& roomType, int roomNumber, const std::string& guestName) {
        auto it = availableRooms.find(roomType);
        if (it == availableRooms.end()) {
            return "False";
        }

        int available = it->second;
        if (roomNumber <= available) {
            // putIfAbsent(roomType, ...) + put(name, roomNumber): insert outer map if
            // missing, then insert/overwrite the inner entry for this guest.
            bookedRooms[roomType][guestName] = roomNumber;
            it->second = available - roomNumber;
            return "Success!";
        } else {
            return "False";
        }
    }

    bool checkIn(const std::string& roomType, int roomNumber, const std::string& guestName) {
        auto outer = bookedRooms.find(roomType);
        if (outer == bookedRooms.end()) {
            return false;
        }
        auto& inner = outer->second;
        auto entry = inner.find(guestName);
        if (entry == inner.end()) {
            return false;
        }

        int booked = entry->second;
        if (roomNumber > booked) {
            return false;
        } else if (roomNumber == booked) {
            inner.erase(entry);
        } else {
            entry->second = booked - roomNumber;
        }
        return true;
    }

    void checkOut(const std::string& roomType, int roomNumber) {
        // getOrDefault(roomType, 0) + roomNumber, then put
        availableRooms[roomType] += roomNumber;
    }

    int getAvailableRooms(const std::string& roomType) const {
        auto it = availableRooms.find(roomType);
        return it == availableRooms.end() ? 0 : it->second;
    }
};

// Java-style Map printing: {k=v, k=v} (nested maps rendered the same way).
static std::string mapToString(const std::unordered_map<std::string, int>& m) {
    std::ostringstream oss;
    oss << "{";
    bool first = true;
    for (const auto& kv : m) {
        if (!first) oss << ", ";
        first = false;
        oss << kv.first << "=" << kv.second;
    }
    oss << "}";
    return oss.str();
}

static std::string mapToString(const std::unordered_map<std::string, std::unordered_map<std::string, int>>& m) {
    std::ostringstream oss;
    oss << "{";
    bool first = true;
    for (const auto& kv : m) {
        if (!first) oss << ", ";
        first = false;
        oss << kv.first << "=" << mapToString(kv.second);
    }
    oss << "}";
    return oss.str();
}

static std::string boolToString(bool b) {
    return b ? "true" : "false";
}

int main() {
    std::unordered_map<std::string, int> rooms;
    rooms["single"] = 3;
    rooms["double"] = 2;
    Hotel hotel("Test Hotel", rooms);

    std::cout << hotel.bookRoom("single", 2, "guest 1") << "\n";
    std::cout << hotel.bookRoom("triple", 2, "guest 1") << "\n";
    std::cout << hotel.bookRoom("single", 2, "guest 2") << "\n";
    std::cout << hotel.bookRoom("single", 1, "guest 2") << "\n";
    std::cout << hotel.bookRoom("single", 3, "guest 1") << "\n";
    std::cout << hotel.bookRoom("single", 100, "guest 1") << "\n";

    hotel.checkIn("single", 1, "guest 1");
    std::cout << mapToString(hotel.bookedRooms) << "\n";
    std::cout << boolToString(hotel.checkIn("single", 3, "guest 1")) << "\n";
    std::cout << boolToString(hotel.checkIn("double", 1, "guest 1")) << "\n";
    hotel.checkIn("double", 1, "guest 2");
    std::cout << mapToString(hotel.bookedRooms) << "\n";

    hotel.checkOut("single", 1);
    std::cout << mapToString(hotel.availableRooms) << "\n";
    hotel.checkOut("triple", 2);
    std::cout << mapToString(hotel.availableRooms) << "\n";

    std::cout << hotel.getAvailableRooms("single") << "\n";
    return 0;
}