#include <vector>
#include <string>
#include <map>
#include <variant>
#include <optional>
#include <algorithm>

class Server {
public:
    using InfoDict = std::map<std::string, std::variant<int, std::string>>;

private:
    std::vector<int> white_list;
    InfoDict send_struct;
    InfoDict receive_struct;

public:
    Server() = default;

    std::variant<bool, std::vector<int>> add_white_list(int addr) {
        if (std::find(white_list.begin(), white_list.end(), addr) != white_list.end()) {
            return false;
        }
        white_list.push_back(addr);
        return white_list;
    }

    std::variant<bool, std::vector<int>> del_white_list(int addr) {
        auto it = std::find(white_list.begin(), white_list.end(), addr);
        if (it == white_list.end()) {
            return false;
        }
        white_list.erase(it);
        return white_list;
    }

    std::variant<int, bool, std::string> recv(const InfoDict& info) {
        auto addr_it = info.find("addr");
        auto content_it = info.find("content");
        if (addr_it == info.end() || content_it == info.end()) {
            return -1;
        }
        int addr = std::get<int>(addr_it->second);
        std::string content = std::get<std::string>(content_it->second);
        if (std::find(white_list.begin(), white_list.end(), addr) == white_list.end()) {
            return false;
        }
        receive_struct = {{"addr", addr}, {"content", content}};
        return content;
    }

    std::optional<std::string> send(const InfoDict& info) {
        auto addr_it = info.find("addr");
        auto content_it = info.find("content");
        if (addr_it == info.end() || content_it == info.end()) {
            return std::string("info structure is not correct");
        }
        send_struct = {{"addr", std::get<int>(addr_it->second)}, {"content", std::get<std::string>(content_it->second)}};
        return std::nullopt;
    }

    std::variant<bool, InfoDict> show(const std::string& type) {
        if (type == "send") {
            return send_struct;
        } else if (type == "receive") {
            return receive_struct;
        }
        return false;
    }
};