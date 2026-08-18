#include <string>
#include <map>
#include <variant>
#include <optional>
#include <utility>

class Hotel {
public:
    using RoomCounts = std::map<std::string, int>;
    using Bookings   = std::map<std::string, RoomCounts>;
    // Mirrors Python's mixed return: str 'Success!' | int remaining | False
    using BookResult = std::variant<bool, int, std::string>;
    // Mirrors Python's None (implicit) | False
    using CheckInResult = std::optional<bool>;

    Hotel(std::string name, RoomCounts rooms)
        : name(std::move(name)), available_rooms(std::move(rooms)) {
        // booked_rooms starts empty, like `self.booked_rooms = {}`
    }

    BookResult book_room(const std::string& room_type, int room_number, const std::string& guest_name) {
        // Check if there are any rooms of the specified type available
        auto avail_it = available_rooms.find(room_type);
        if (avail_it == available_rooms.end()) {
            return false;
        }

        if (room_number <= avail_it->second) {
            // Book the room by adding it to the booked_rooms dictionary
            booked_rooms[room_type][guest_name] = room_number;
            avail_it->second -= room_number;
            return std::string("Success!");  // explicit: avoids const char* -> bool variant trap
        } else if (avail_it->second != 0) {
            return avail_it->second;
        } else {
            return false;
        }
    }

    CheckInResult check_in(const std::string& room_type, int room_number, const std::string& guest_name) {
        // Check if the room of the specified type and number is booked
        auto booked_it = booked_rooms.find(room_type);
        if (booked_it == booked_rooms.end()) {
            return false;
        }
        auto guest_it = booked_it->second.find(guest_name);
        if (guest_it != booked_it->second.end()) {
            if (room_number > guest_it->second) {
                return false;
            } else if (room_number == guest_it->second) {
                // Check in the room by removing it from the booked_rooms dictionary
                booked_it->second.erase(guest_it);
            } else {
                guest_it->second -= room_number;
            }
        }
        return std::nullopt;  // Python implicit None
    }

    void check_out(const std::string& room_type, int room_number) {
        auto it = available_rooms.find(room_type);
        if (it != available_rooms.end()) {
            it->second += room_number;
        } else {
            available_rooms[room_type] = room_number;
        }
    }

    int get_available_rooms(const std::string& room_type) {
        // .at() throws std::out_of_range for a missing key, matching Python's KeyError
        return available_rooms.at(room_type);
    }

    std::string name;
    RoomCounts available_rooms;
    Bookings booked_rooms;
};