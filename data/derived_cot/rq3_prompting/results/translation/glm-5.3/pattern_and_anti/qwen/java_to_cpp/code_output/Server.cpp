#include <map>
#include <variant>
#include <string>
#include <vector>
#include <optional>
#include <algorithm>

namespace org::example {

class Server {
public:
    // Stand-in for java.lang.Object for the value types actually stored:
    // int ("addr"), std::string ("content"), bool (recv failure result).
    using Object = std::variant<int, bool, std::string>;
    using MapType = std::map<std::string, Object>;

    Server() = default;

    // Java: returns the live list reference, or null if already present.
    std::vector<int>* addWhiteList(int addr) {
        if (std::find(whiteList.begin(), whiteList.end(), addr) != whiteList.end()) {
            return nullptr;
        }
        whiteList.push_back(addr);
        return &whiteList;
    }

    // Java: returns the live list reference, or null if not present.
    std::vector<int>* delWhiteList(int addr) {
        if (std::find(whiteList.begin(), whiteList.end(), addr) == whiteList.end()) {
            return nullptr;
        }
        // Java remove(Integer.valueOf(addr)) removes by value, not by index.
        whiteList.erase(std::remove(whiteList.begin(), whiteList.end(), addr),
                        whiteList.end());
        return &whiteList;
    }

    // Java: returns Integer(-1), Boolean(false), or the stored content String.
    Object recv(const MapType* info) {
        if (info == nullptr || info->count("addr") == 0 || info->count("content") == 0) {
            return -1;
        }
        // Java casts throw ClassCastException on wrong type; std::get throws
        // bad_variant_access analogously.
        int addr = std::get<int>(info->at("addr"));
        std::string content = std::get<std::string>(info->at("content"));
        if (std::find(whiteList.begin(), whiteList.end(), addr) == whiteList.end()) {
            return false;
        }
        receiveStruct["addr"] = addr;
        receiveStruct["content"] = std::move(content);
        return receiveStruct["content"];
    }

    // Java: returns an error String, or null on success -> optional nullopt.
    std::optional<std::string> send(const MapType* info) {
        if (info == nullptr || info->count("addr") == 0 || info->count("content") == 0) {
            return std::string("info structure is not correct");
        }
        sendStruct["addr"] = info->at("addr");
        sendStruct["content"] = info->at("content");
        return std::nullopt;
    }

    // Java: returns live map reference, or null for unknown type.
    MapType* show(const std::string& type) {
        if (type == "send") {
            return &sendStruct;
        } else if (type == "receive") {
            return &receiveStruct;
        } else {
            return nullptr;
        }
    }

private:
    std::vector<int> whiteList;
    MapType sendStruct;
    MapType receiveStruct;
};

} // namespace org::example