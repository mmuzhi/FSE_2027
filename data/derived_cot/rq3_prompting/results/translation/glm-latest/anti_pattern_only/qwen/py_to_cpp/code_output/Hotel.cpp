#include <map>
#include <optional>
#include <string>
#include <utility>
#include <variant>

// Hotel management system: booking, check-in, check-out and availability
// of rooms in a hotel with different room types.
class Hotel {
public:
    std::string name;                                              // hotel name
    // available_rooms = {'single': 5, 'double': 3, ...}
    std::map<std::string, int> available_rooms;
    // booked_rooms = {'single': {'guest 1': 2, 'guest 2': 1}, 'double': {}, ...}
    std::map<std::string, std::map<std::string, int>> booked_rooms;

    Hotel(std::string hotel_name, std::map<std::string, int> rooms)
        : name(std::move(hotel_name)), available_rooms(std::move(rooms)) {}

    // Returns:
    //   std::string("Success!")  if room_number does not exceed the remaining rooms
    //   int                      if it exceeds but the remaining quantity is not zero
    //   false                    if it exceeds and the quantity is zero, or the
    //                            room_type is not present in available_rooms
    std::variant<std::string, int, bool> book_room(const std::string& room_type,
                                                   int room_number,
                                                   const std::string& guest_name) {
        // Check if there are any rooms of the specified type available
        auto avail = available_rooms.find(room_type);
        if (avail == available_rooms.end()) {
            return false;
        }

        if (room_number <= avail->second) {
            // Book the room by recording it in booked_rooms
            // (creates the room type / guest entry when absent, overwrites otherwise)
            booked_rooms[room_type][guest_name] = room_number;
            avail->second -= room_number;
            return std::string("Success!");
        } else if (avail->second != 0) {
            return avail->second;
        } else {
            return false;
        }
    }

    // Returns:
    //   false           if room_type is not in booked_rooms, or room_number is
    //                    higher than the guest's booked quantity
    //   std::nullopt    otherwise (Python implicitly returns None)
    std::optional<bool> check_in(const std::string& room_type,
                                 int room_number,
                                 const std::string& guest_name) {
        // Check if the room of the specified type and number is booked
        auto type_it = booked_rooms.find(room_type);
        if (type_it == booked_rooms.end()) {
            return false;
        }

        auto& guests = type_it->second;
        auto guest_it = guests.find(guest_name);
        if (guest_it != guests.end()) {
            if (room_number > guest_it->second) {
                return false;
            } else if (room_number == guest_it->second) {
                // Full check-in: remove the guest's booking
                guests.erase(guest_it);
            } else {
                // Partial check-in: booked quantity minus actual quantity remains
                guest_it->second -= room_number;
            }
        }
        return std::nullopt;
    }

    void check_out(const std::string& room_type, int room_number) {
        auto it = available_rooms.find(room_type);
        if (it != available_rooms.end()) {
            it->second += room_number;
        } else {
            // New room type: add it to available_rooms
            available_rooms.emplace(room_type, room_number);
        }
    }

    // Throws std::out_of_range for an unknown room_type (analogous to Python's KeyError)
    int get_available_rooms(const std::string& room_type) const {
        return available_rooms.at(room_type);
    }
};