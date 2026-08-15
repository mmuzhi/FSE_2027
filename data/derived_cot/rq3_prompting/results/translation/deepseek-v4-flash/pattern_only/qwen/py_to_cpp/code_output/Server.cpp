#include <vector>
#include <map>
#include <string>
#include <variant>
#include <optional>
#include <algorithm>

using InfoDict = std::map<std::string, std::variant<bool, int, std::string>>;
using StructDict = InfoDict;

class Server {
private:
    std::vector<int> white_list;
    StructDict send_struct;
    StructDict receive_struct;

public:
    Server() : white_list(), send_struct(), receive_struct() {}

    std::variant<bool, std::vector<int>> add_white_list(int addr) {
        if (std::find(white_list.begin(), white_list.end(), addr) != white_list.end()) {
            return false;
        } else {
            white_list.push_back(addr);
            return white_list;
        }
    }

    std::variant<bool, std::vector<int>> del_white_list(int addr) {
        auto it = std::find(white_list.begin(), white_list.end(), addr);
        if (it == white_list.end()) {
            return false;
        } else {
            white_list.erase(it);
            return white_list;
        }
    }

    std::variant<bool, int, std::string> recv(const InfoDict& info) {
        auto addr_it = info.find("addr");
        auto content_it = info.find("content");
        if (addr_it == info.end() || content_it == info.end()) {
            return -1;
        }

        const auto& addr_v = addr_it->second;
        const auto& content_v = content_it->second;

        int addr;
        if (auto p = std::get_if<int>(&addr_v)) {
            addr = *p;
        } else if (auto p = std::get_if<bool>(&addr_v)) {
            addr = *p ? 1 : 0;
        } else {
            return false;
        }

        if (std::find(white_list.begin(), white_list.end(), addr) == white_list.end()) {
            return false;
        }

        receive_struct["addr"] = addr_v;
        receive_struct["content"] = content_v;

        return std::visit([](auto&& value) -> std::variant<bool, int, std::string> {
            return value;
        }, content_v);
    }

    std::optional<std::string> send(const InfoDict& info) {
        auto addr_it = info.find("addr");
        auto content_it = info.find("content");
        if (addr_it == info.end() || content_it == info.end()) {
            return std::string("info structure is not correct");
        }

        send_struct["addr"] = addr_it->second;
        send_struct["content"] = content_it->second;

        return std::nullopt;
    }

    std::variant<StructDict, bool> show(const std::string& type) const {
        if (type == "send") {
            return send_struct;
        } else if (type == "receive") {
            return receive_struct;
        } else {
            return false;
        }
    }
};