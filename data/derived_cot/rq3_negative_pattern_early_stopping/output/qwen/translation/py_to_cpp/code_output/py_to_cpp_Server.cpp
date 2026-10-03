#include <vector>
#include <map>
#include <string>
#include <optional>
#include <variant>
#include <algorithm>
#include <iostream>

class Server {
private:
    std::vector<int> white_list;
    std::map<std::string, std::string> send_struct;
    std::map<std::string, std::string> receive_struct;

public:
    // Add an address to the whitelist if not present, otherwise return std::nullopt
    std::optional<std::vector<int>> add_white_list(int addr) {
        auto it = std::find(white_list.begin(), white_list.end(), addr);
        if (it != white_list.end()) {
            return std::nullopt;
        }
        white_list.push_back(addr);
        return white_list;
    }

    // Remove an address from the whitelist if present, otherwise return std::nullopt
    std::optional<std::vector<int>> del_white_list(int addr) {
        auto it = std::find(white_list.begin(), white_list.end(), addr);
        if (it == white_list.end()) {
            return std::nullopt;
        }
        white_list.erase(it);
        return white_list;
    }

    // Receive a message, validate, check whitelist, and return content or error
    std::variant<int, bool, std::string> recv(const std::map<std::string, std::string>& info) {
        if (info.size() < 2 || info.find("addr") == info.end() || info.find("content") == info.end()) {
            return -1;
        }
        int addr = std::stoi(info.at("addr"));
        std::string content = info.at("content");
        if (std::find(white_list.begin(), white_list.end(), addr) == white_list.end()) {
            return false;
        }
        receive_struct = info;
        return content;
    }

    // Send a message, validate, and store it or return error
    std::optional<std::string> send(const std::map<std::string, std::string>& info) {
        if (info.size() < 2 || info.find("addr") == info.end() || info.find("content") == info.end()) {
            return "info structure is not correct";
        }
        send_struct = info;
        return std::nullopt;
    }

    // Show the requested structure or return std::nullopt if invalid
    std::optional<std::map<std::string, std::string>> show(const std::string& type) {
        if (type == "send") {
            return send_struct;
        } else if (type == "receive") {
            return receive_struct;
        }
        return std::nullopt;
    }
};