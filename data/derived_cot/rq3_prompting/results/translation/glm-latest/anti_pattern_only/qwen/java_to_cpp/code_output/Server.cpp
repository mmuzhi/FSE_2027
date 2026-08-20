#include <algorithm>
#include <any>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

// "Object" mirrors java.lang.Object: it can hold any value type (int, bool, std::string, ...).
using Object = std::any;
// Java Map<String, Object> (HashMap) -> std::unordered_map<std::string, std::any>.
using StructMap = std::unordered_map<std::string, Object>;

class Server {
private:
    std::vector<int> whiteList;
    StructMap sendStruct;
    StructMap receiveStruct;

public:
    Server() = default;

    // Returns nullptr if addr is already whitelisted (Java: null);
    // otherwise appends addr and returns the live whitelist (Java: the list itself).
    std::vector<int>* addWhiteList(int addr) {
        if (std::find(whiteList.begin(), whiteList.end(), addr) != whiteList.end()) {
            return nullptr;
        }
        whiteList.push_back(addr);
        return &whiteList;
    }

    // Returns nullptr if addr is not whitelisted (Java: null);
    // otherwise removes the first occurrence and returns the live whitelist.
    std::vector<int>* delWhiteList(int addr) {
        auto it = std::find(whiteList.begin(), whiteList.end(), addr);
        if (it == whiteList.end()) {
            return nullptr;
        }
        whiteList.erase(it);
        return &whiteList;
    }

    // Returns an Object holding:
    //   int(-1)              - info is null or missing "addr"/"content" (Java: Integer -1),
    //   bool(false)          - addr is not whitelisted (Java: Boolean false),
    //   std::string(content) - the received content on success.
    // std::any_cast throws std::bad_any_cast, mirroring Java's ClassCastException
    // for wrongly-typed values, before any state is mutated.
    Object recv(const StructMap* info) {
        if (info == nullptr || info->find("addr") == info->end() ||
            info->find("content") == info->end()) {
            return Object(-1);
        }
        int addr = std::any_cast<int>(info->at("addr"));
        std::string content = std::any_cast<std::string>(info->at("content"));
        if (std::find(whiteList.begin(), whiteList.end(), addr) == whiteList.end()) {
            return Object(false);
        }
        receiveStruct["addr"] = addr;
        receiveStruct["content"] = content;
        return receiveStruct["content"];
    }

    // Returns "info structure is not correct" when info is null or malformed;
    // returns std::nullopt on success (Java: null).
    std::optional<std::string> send(const StructMap* info) {
        if (info == nullptr || info->find("addr") == info->end() ||
            info->find("content") == info->end()) {
            return std::string("info structure is not correct");
        }
        sendStruct["addr"] = info->at("addr");
        sendStruct["content"] = info->at("content");
        return std::nullopt;
    }

    // Null-safe, mirroring "send".equals(type) / "receive".equals(type):
    // a null or unknown type yields nullptr.
    StructMap* show(const std::string* type) {
        if (type != nullptr && *type == "send") {
            return &sendStruct;
        } else if (type != nullptr && *type == "receive") {
            return &receiveStruct;
        } else {
            return nullptr;
        }
    }
};