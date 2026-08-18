#include <string>
#include <vector>
#include <optional>
#include <variant>
#include <algorithm>

// A class acting as a server, handling a whitelist, message
// sending/receiving, and information display.
class Server {
public:
    // Information dictionary equivalent: optional "addr" and "content" keys.
    // A missing key is represented by a disengaged optional.
    struct Info {
        std::optional<int> addr;
        std::optional<std::string> content;
    };

    // Initialize the whitelist as an empty list, and initialize the
    // sending and receiving information as empty dicts.
    Server() = default;

    // Add an address to the whitelist; do nothing if it already exists.
    // Returns the new whitelist, or "False" (nullopt) if it already exists.
    std::optional<std::vector<int>> add_white_list(int addr) {
        if (std::find(white_list.begin(), white_list.end(), addr) != white_list.end()) {
            return std::nullopt; // False
        }
        white_list.push_back(addr);
        return white_list;
    }

    // Remove an address from the whitelist; do nothing if it does not exist.
    // Returns the new whitelist, or "False" (nullopt) if it does not exist.
    std::optional<std::vector<int>> del_white_list(int addr) {
        auto it = std::find(white_list.begin(), white_list.end(), addr);
        if (it == white_list.end()) {
            return std::nullopt; // False
        }
        white_list.erase(it);
        return white_list;
    }

    // Receive information containing address and content. If the address is
    // on the whitelist, receive the content; otherwise, do not receive it.
    // Returns: -1 if the info structure is not correct; false if the address
    // is not whitelisted; otherwise the received content.
    std::variant<int, bool, std::string> recv(const Info& info) {
        if (!info.addr.has_value() || !info.content.has_value()) {
            return -1;
        }
        int addr = *info.addr;
        const std::string& content = *info.content;
        if (std::find(white_list.begin(), white_list.end(), addr) == white_list.end()) {
            return false;
        }
        receive_struct = Info{addr, content};
        return *receive_struct.content;
    }

    // Send information containing address and content.
    // Returns nothing (nullopt = None) on success; otherwise an error string.
    std::optional<std::string> send(const Info& info) {
        if (!info.addr.has_value() || !info.content.has_value()) {
            return std::string("info structure is not correct");
        }
        send_struct = Info{*info.addr, *info.content};
        return std::nullopt; // None (implicit return)
    }

    // Returns the struct of the specified type ("send" or "receive"),
    // or "False" (nullopt) otherwise.
    std::optional<Info> show(const std::string& type) {
        if (type == "send") {
            return send_struct;
        } else if (type == "receive") {
            return receive_struct;
        }
        return std::nullopt; // False
    }

private:
    std::vector<int> white_list;
    Info send_struct;      // initially "empty dict"
    Info receive_struct;   // initially "empty dict"
};