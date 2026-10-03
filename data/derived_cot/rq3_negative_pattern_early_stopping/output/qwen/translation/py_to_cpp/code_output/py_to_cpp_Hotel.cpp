#include <unordered_map>
#include <string>
#include <variant>

using namespace std;

class Hotel {
private:
    string name;
    unordered_map<string, int> available_rooms;
    unordered_map<string, unordered_map<string, int>> booked_rooms;

public:
    Hotel(string name, unordered_map<string, int> rooms) : name(name), available_rooms(rooms) {}

    variant<string, int, bool> book_room(string room_type, int room_number, string name) {
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

    bool check_in(string room_type, int room_number, string name) {
        if (booked_rooms.find(room_type) == booked_rooms.end() || 
            booked_rooms[room_type].find(name) == booked_rooms[room_type].end()) {
            return false;
        }

        if (room_number > booked_rooms[room_type][name]) {
            return false;
        }

        if (room_number == booked_rooms[room_type][name]) {
            booked_rooms[room_type].erase(name);
        } else {
            booked_rooms[room_type][name] -= room_number;
        }

        return true;
    }

    void check_out(string room_type, int room_number) {
        if (available_rooms.find(room_type) != available_rooms.end()) {
            available_rooms[room_type] += room_number;
        } else {
            available_rooms[room_type] = room_number;
        }
    }

    int get_available_rooms(string room_type) {
        return available_rooms[room_type];
    }
};