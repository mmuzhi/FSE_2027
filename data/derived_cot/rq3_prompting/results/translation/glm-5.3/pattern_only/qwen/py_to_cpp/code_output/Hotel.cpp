#include <string>
#include <map>
#include <variant>
#include <optional>
#include <utility>

class Hotel {
public:
    using GuestBookings = std::map<std::string, int>;

    Hotel(std::string name, std::map<std::string, int> rooms)
        : name_(std::move(name)), available_rooms_(std::move(rooms)) {
        // available_rooms = {room_type1: room_number1, room_type2: room_number2, ...}
        // e.g. {'single': 5, 'double': 3}
        // booked_rooms stays empty, mirroring Python's self.booked_rooms = {}
    }

    // Returns "Success!" (string), the remaining quantity (int), or false.
    // Note: std::string("Success!") is explicit to avoid const char* -> bool decay
    // inside std::variant.
    std::variant<std::string, int, bool> book_room(const std::string& room_type,
                                                   int room_number,
                                                   const std::string& name) {
        // Check if there are any rooms of the specified type available
        auto avail_it = available_rooms_.find(room_type);
        if (avail_it == available_rooms_.end()) {
            return false;
        }

        if (room_number <= avail_it->second) {
            // Book the room by adding it to the booked_rooms map
            // (mirrors Python: creates the inner dict if missing, overwrites the guest entry)
            booked_rooms_[room_type][name] = room_number;
            avail_it->second -= room_number;
            return std::string("Success!");
        } else if (avail_it->second != 0) {
            return avail_it->second;
        } else {
            return false;
        }
    }

    // Returns false on failed check-in; std::nullopt otherwise (Python's implicit None).
    std::optional<bool> check_in(const std::string& room_type,
                                 int room_number,
                                 const std::string& name) {
        // Check if the room of the specified type and number is booked
        auto type_it = booked_rooms_.find(room_type);
        if (type_it == booked_rooms_.end()) {
            return false;
        }
        auto guest_it = type_it->second.find(name);
        if (guest_it != type_it->second.end()) {
            if (room_number > guest_it->second) {
                return false;
            } else if (room_number == guest_it->second) {
                // Check in the room by removing it from the booked_rooms map
                type_it->second.erase(guest_it);
            } else {
                guest_it->second -= room_number;
            }
        }
        return std::nullopt;
    }

    void check_out(const std::string& room_type, int room_number) {
        auto it = available_rooms_.find(room_type);
        if (it != available_rooms_.end()) {
            it->second += room_number;
        } else {
            available_rooms_[room_type] = room_number;
        }
    }

    // Python dict indexing raises KeyError for a missing type;
    // .at() throwing std::out_of_range is the closest equivalent.
    int get_available_rooms(const std::string& room_type) const {
        return available_rooms_.at(room_type);
    }

    std::string name_;
    std::map<std::string, int> available_rooms_;
    std::map<std::string, GuestBookings> booked_rooms_;
};