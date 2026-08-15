#include <map>
#include <string>
#include <variant>
#include <optional>
#include <exception>
#include <utility>

class KeyError : public std::exception {
public:
    explicit KeyError(const std::string& key)
        : message_("'" + key + "'") {}

    const char* what() const noexcept override {
        return message_.c_str();
    }

private:
    std::string message_;
};

class Hotel {
public:
    std::string name;
    std::map<std::string, int> available_rooms;
    std::map<std::string, std::map<std::string, int>> booked_rooms;

    Hotel(std::string name, std::map<std::string, int> rooms)
        : name(std::move(name)), available_rooms(std::move(rooms)) {}

    std::variant<std::string, int, bool> book_room(
        const std::string& room_type,
        int room_number,
        const std::string& name
    ) {
        auto it = available_rooms.find(room_type);
        if (it == available_rooms.end()) {
            return false;
        }

        if (room_number <= it->second) {
            auto booked_it = booked_rooms.find(room_type);
            if (booked_it == booked_rooms.end()) {
                booked_rooms[room_type] = {};
            }
            booked_rooms[room_type][name] = room_number;
            it->second -= room_number;
            return std::string("Success!");
        } else if (it->second != 0) {
            return it->second;
        } else {
            return false;
        }
    }

    std::optional<bool> check_in(
        const std::string& room_type,
        int room_number,
        const std::string& name
    ) {
        auto booked_it = booked_rooms.find(room_type);
        if (booked_it == booked_rooms.end()) {
            return false;
        }

        auto& guests = booked_it->second;
        auto guest_it = guests.find(name);
        if (guest_it == guests.end()) {
            return std::nullopt;
        }

        if (room_number > guest_it->second) {
            return false;
        } else if (room_number == guest_it->second) {
            guests.erase(guest_it);
        } else {
            guest_it->second -= room_number;
        }

        return std::nullopt;
    }

    void check_out(const std::string& room_type, int room_number) {
        auto it = available_rooms.find(room_type);
        if (it != available_rooms.end()) {
            it->second += room_number;
        } else {
            available_rooms[room_type] = room_number;
        }
    }

    int get_available_rooms(const std::string& room_type) const {
        auto it = available_rooms.find(room_type);
        if (it == available_rooms.end()) {
            throw KeyError(room_type);
        }
        return it->second;
    }
};