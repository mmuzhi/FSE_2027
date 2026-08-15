#include <vector>
#include <unordered_map>
#include <string>
#include <any>
#include <algorithm>
#include <optional>
#include <stdexcept>

class Server {
public:
    Server() = default;

    std::vector<int>* addWhiteList(int addr) {
        if (std::find(whiteList.begin(), whiteList.end(), addr) != whiteList.end()) {
            return nullptr;
        }
        whiteList.push_back(addr);
        return &whiteList;
    }

    std::vector<int>* delWhiteList(int addr) {
        auto it = std::find(whiteList.begin(), whiteList.end(), addr);
        if (it == whiteList.end()) {
            return nullptr;
        }
        whiteList.erase(it);
        return &whiteList;
    }

    std::any recv(const std::unordered_map<std::string, std::any>* info) {
        if (info == nullptr || info->find("addr") == info->end() || info->find("content") == info->end()) {
            return -1;
        }
        const std::any& addrAny = info->at("addr");
        if (!addrAny.has_value()) {
            throw std::runtime_error("NullPointerException");
        }
        int addr = std::any_cast<int>(addrAny);

        const std::any& contentAny = info->at("content");
        if (!contentAny.has_value()) {
            throw std::runtime_error("NullPointerException");
        }
        std::string content = std::any_cast<std::string>(contentAny);

        if (std::find(whiteList.begin(), whiteList.end(), addr) == whiteList.end()) {
            return false;
        }
        receiveStruct["addr"] = addr;
        receiveStruct["content"] = content;
        return receiveStruct["content"];
    }

    std::optional<std::string> send(const std::unordered_map<std::string, std::any>* info) {
        if (info == nullptr || info->find("addr") == info->end() || info->find("content") == info->end()) {
            return std::string("info structure is not correct");
        }
        sendStruct["addr"] = info->at("addr");
        sendStruct["content"] = info->at("content");
        return std::nullopt;
    }

    std::unordered_map<std::string, std::any>* show(const std::optional<std::string>& type) {
        if (type && *type == "send") {
            return &sendStruct;
        } else if (type && *type == "receive") {
            return &receiveStruct;
        } else {
            return nullptr;
        }
    }

private:
    std::vector<int> whiteList;
    std::unordered_map<std::string, std::any> sendStruct;
    std::unordered_map<std::string, std::any> receiveStruct;
};