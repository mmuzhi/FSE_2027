#include <string>
#include <vector>
#include <map>
#include <variant>
#include <optional>
#include <algorithm>

// Server: manages a whitelist, message sending/receiving, and display.
//
// Value mirrors a Python dict value (int / bool / str); Info mirrors a Python dict.
// Note: when building an Info, wrap string literals in std::string(...) so they
// bind to the std::string alternative rather than converting to bool:
//   Server::Info{{"addr", 88}, {"content", std::string("abc")}}

class Server {
public:
    using Value = std::variant<int, bool, std::string>;
    using Info = std::map<std::string, Value>;

    std::vector<int> white_list;
    Info send_struct;
    Info receive_struct;

    Server() = default;

    // Add an address to the whitelist; returns nullopt (False) if it already
    // exists, otherwise the updated whitelist.
    std::optional<std::vector<int>> add_white_list(int addr) {
        if (std::find(white_list.begin(), white_list.end(), addr) != white_list.end())
            return std::nullopt;                       // False
        white_list.push_back(addr);
        return white_list;
    }

    // Remove an address from the whitelist; returns nullopt (False) if it is
    // absent, otherwise the updated whitelist.
    std::optional<std::vector<int>> del_white_list(int addr) {
        auto it = std::find(white_list.begin(), white_list.end(), addr);
        if (it == white_list.end())
            return std::nullopt;                       // False
        white_list.erase(it);
        return white_list;
    }

    // Receive info {"addr": .., "content": ..}.
    // Returns -1 if info is malformed (missing keys), false if the address is
    // not whitelisted, otherwise the received content.
    std::variant<int, bool, std::string> recv(const Info& info) {
        auto addr_it = info.find("addr");
        auto content_it = info.find("content");
        if (addr_it == info.end() || content_it == info.end())
            return -1;
        int addr;
        if (auto p = std::get_if<int>(&addr_it->second))
            addr = *p;
        else if (auto p = std::get_if<bool>(&addr_it->second))
            addr = *p ? 1 : 0;                         // True == 1 in Python
        else
            return false;                              // non-int addr can never match the whitelist
        if (std::find(white_list.begin(), white_list.end(), addr) == white_list.end())
            return false;
        receive_struct.clear();
        receive_struct["addr"] = addr_it->second;
        receive_struct["content"] = content_it->second;
        return receive_struct["content"];
    }

    // Send info {"addr": .., "content": ..}.
    // Returns nullopt (None) on success, or an error message if malformed.
    std::optional<std::string> send(const Info& info) {
        if (info.find("addr") == info.end() || info.find("content") == info.end())
            return std::string("info structure is not correct");
        send_struct.clear();
        send_struct["addr"] = info.at("addr");
        send_struct["content"] = info.at("content");
        return std::nullopt;                           // None
    }

    // Returns a pointer to the live struct of the requested type, or nullptr
    // (False) if `type` is neither "send" nor "receive".
    const Info* show(const std::string& type) {
        if (type == "send") return &send_struct;
        if (type == "receive") return &receive_struct;
        return nullptr;                                // False
    }
};