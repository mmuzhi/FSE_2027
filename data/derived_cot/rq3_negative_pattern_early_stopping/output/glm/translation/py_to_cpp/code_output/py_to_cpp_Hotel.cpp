#include <string>
#include <map>
#include <variant>

class Hotel {
public:
    std::string name;
    std::map<std::string, int> available_rooms;
    std::map<std::string, std::map<std::string, int>> booked_rooms;

    Hotel(std::string name, std::map<std::string, int> rooms)
        : name(std::move(name)), available_rooms(std::move(rooms)) {}

    using BookRoomResult = std::variant<bool, int, std::string>;

    BookRoomResult book_room(const std::string& room_type, int room_number, const std::string& name) {
        if (available_rooms.find(room_type) == available_rooms.end()) {
            return false;
        }

        if (room_number <= available_rooms[room_type]) {
            if (booked_rooms.find(room_type) == booked_rooms.end()) {
                booked_rooms[room_type] = {};
            }
            booked_rooms[room_type][name] = room_number;
            available_rooms[room_type] -= room_number;
            return "Success!";
        } else if (available_rooms[room_type] != 0) {
            return available_rooms[room_type];
        } else {
            return false;
        }
    }

    using CheckInResult = std::variant<bool, std::monostate>;

    CheckInResult check_in(const std::string& room_type, int room_number, const std::string& name) {
        if (booked_rooms.find(room_type) == booked_rooms.end()) {
            return false;
        }
        if (booked_rooms[room_type].find(name) != booked_rooms[room_type].end()) {
            if (room_number > booked_rooms[room_type][name]) {
                return false;
            } else if (room_number == booked_rooms[room_type][name]) {
                booked_rooms[room_type].erase(name);
            } else {
                booked_rooms[room_type][name] -= room_number;
            }
        }
        return std::monostate{};
    }

    void check_out(const std::string& room_type, int room_number) {
        if (available_rooms.find(room_type) != available_rooms.end()) {
            available_rooms[room_type] += room_number;
        } else {
            available_rooms[room_type] = room_number;
        }
    }

    int get_available_rooms(const std::string& room_type) {
        return available_rooms.at(room_type);
    }
};