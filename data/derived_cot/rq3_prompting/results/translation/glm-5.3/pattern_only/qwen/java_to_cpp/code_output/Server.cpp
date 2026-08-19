#pragma once

#include <algorithm>
#include <map>
#include <optional>
#include <string>
#include <variant>
#include <vector>

namespace org {
namespace example {

// Java's Object narrowed to the types actually used: Integer, Boolean, String.
using Object = std::variant<int, bool, std::string>;
using Map = std::map<std::string, Object>;

class Server {
private:
    std::vector<int> whiteList;
    Map sendStruct;
    Map receiveStruct;

    static bool containsKey(const Map& m, const std::string& key) {
        return m.find(key) != m.end();
    }

    static bool contains(const std::vector<int>& v, int value) {
        return std::find(v.begin(), v.end(), value) != v.end();
    }

public:
    Server() = default;

    // Java: returns the live list, or null when addr is already present.
    std::vector<int>* addWhiteList(int addr) {
        if (contains(whiteList, addr)) {
            return nullptr;
        } else {
            whiteList.push_back(addr);
            return &whiteList;
        }
    }

    // Java: removes by value (Integer.valueOf), not by index; returns live list or null.
    std::vector<int>* delWhiteList(int addr) {
        if (!contains(whiteList, addr)) {
            return nullptr;
        } else {
            auto it = std::find(whiteList.begin(), whiteList.end(), addr);
            whiteList.erase(it);
            return &whiteList;
        }
    }

    // Java returns: Integer(-1), Boolean(false), or the stored content String.
    Object recv(const Map* info) {
        if (info == nullptr || !containsKey(*info, "addr") || !containsKey(*info, "content")) {
            return Object{-1};
        }
        int addr = std::get<int>(info->at("addr"));                 // throws on wrong type, like ClassCastException
        const std::string& content = std::get<std::string>(info->at("content"));
        if (!contains(whiteList, addr)) {
            return Object{false};
        } else {
            receiveStruct["addr"] = addr;
            receiveStruct["content"] = content;
            return receiveStruct["content"];
        }
    }

    // Java: returns null on success, error message otherwise (nullopt == null).
    std::optional<std::string> send(const Map* info) {
        if (info == nullptr || !containsKey(*info, "addr") || !containsKey(*info, "content")) {
            return std::string("info structure is not correct");
        }
        sendStruct["addr"] = info->at("addr");
        sendStruct["content"] = info->at("content");
        return std::nullopt;
    }

    // Java: returns the live map reference, or null for unknown type.
    Map* show(const std::string& type) {
        if (type == "send") {
            return &sendStruct;
        } else if (type == "receive") {
            return &receiveStruct;
        } else {
            return nullptr;
        }
    }
};

} // namespace example
} // namespace org