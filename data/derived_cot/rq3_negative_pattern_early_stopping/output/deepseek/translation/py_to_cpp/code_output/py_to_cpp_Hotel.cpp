#include <string>
#include <unordered_map>
#include <variant>
#include <stdexcept>

class Hotel {
public:
    std::string name;
    std::unordered_map<std::string, int> available_rooms;
    std::unordered_map<std::string, std::unordered_map<std::string, int>> booked_rooms;

    Hotel(const std::string& name, const std::unordered_map<std::string, int>& rooms)
        : name(name), available_rooms(rooms) {}

    std::variant<std::string, int, bool> book_room(const std::string& room_type, int room_number, const std::string& name) {
        if (available_rooms.find(room_type) == available_rooms.end()) {
            return false;
        }
        if (room_number <= available_rooms[room_type]) {
            if (booked_rooms.find(room_type) == booked_rooms.end()) {
                booked_rooms[room_type] = std::unordered_map<std::string, int>();
            }
            booked_rooms[room_type][name] = room_number;
            available_rooms[room_type] -= room_number;
            return std::string("Success!");
        } else if (available_rooms[room_type] != 0) {
            return available_rooms[room_type];
        } else {
            return false;
        }
    }

    bool check_in(const std::string& room_type, int room_number, const std::string& name) {
        if (booked_rooms.find(room_type) == booked_rooms.end()) {
            return false;
        }
        auto& type_rooms = booked_rooms[room_type];
        if (type_rooms.find(name) == type_rooms.end()) {
            return false;
        }
        if (room_number > type_rooms[name]) {
            return false;
        } else if (room_number == type_rooms[name]) {
            type_rooms.erase(name);
        } else {
            type_rooms[name] -= room_number;
        }
        return true;
    }

    void check_out(const std::string& room_type, int room_number) {
        if (available_rooms.find(room_type) != available_rooms.end()) {
            available_rooms[room_type] += room_number;
        } else {
            available_rooms[room_type] = room_number;
        }
    }

    int get_available_rooms(const std::string& room_type) {
        return available_rooms[room_type];
    }
};