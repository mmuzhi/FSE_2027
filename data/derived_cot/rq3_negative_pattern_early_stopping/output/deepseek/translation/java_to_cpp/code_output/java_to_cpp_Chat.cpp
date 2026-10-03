#include <unordered_map>
#include <vector>
#include <string>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <chrono>
#include <algorithm>

class Chat {
public:
    Chat() = default;

    bool addUser(const std::string& username) {
        if (users.find(username) != users.end()) {
            return false;
        }
        users[username] = std::vector<Message>();
        return true;
    }

    bool removeUser(const std::string& username) {
        auto it = users.find(username);
        if (it != users.end()) {
            users.erase(it);
            return true;
        }
        return false;
    }

    bool sendMessage(const std::string& sender, const std::string& receiver, const std::string& message) {
        if (users.find(sender) == users.end() || users.find(receiver) == users.end()) {
            return false;
        }
        std::string timestamp = getCurrentTimestamp();
        Message msg(sender, receiver, message, timestamp);
        users[sender].push_back(msg);
        users[receiver].push_back(msg);
        return true;
    }

    std::vector<Message> getMessages(const std::string& username) const {
        auto it = users.find(username);
        if (it == users.end()) {
            return std::vector<Message>();
        }
        return it->second;
    }

    std::unordered_map<std::string, std::vector<Message>>& getUsers() {
        return users;
    }

    struct Message {
        std::string sender;
        std::string receiver;
        std::string message;
        std::string timestamp;

        Message() = default;
        Message(const std::string& s, const std::string& r, const std::string& m, const std::string& t)
            : sender(s), receiver(r), message(m), timestamp(t) {}

        bool operator==(const Message& other) const {
            return sender == other.sender &&
                   receiver == other.receiver &&
                   message == other.message &&
                   timestamp == other.timestamp;
        }

        std::string toString() const {
            std::ostringstream oss;
            oss << "Message{sender='" << sender << "', receiver='" << receiver
                << "', message='" << message << "', timestamp='" << timestamp << "'}";
            return oss.str();
        }
    };

private:
    std::unordered_map<std::string, std::vector<Message>> users;

    static std::string getCurrentTimestamp() {
        auto now = std::chrono::system_clock::now();
        std::time_t t = std::chrono::system_clock::to_time_t(now);
        std::tm* tm = std::localtime(&t);
        std::ostringstream ss;
        ss << std::put_time(tm, "%Y-%m-%d %H:%M:%S");
        return ss.str();
    }
};

// Specialize std::hash for Message if needed for unordered containers (optional)
namespace std {
    template<>
    struct hash<Chat::Message> {
        std::size_t operator()(const Chat::Message& msg) const {
            std::size_t h1 = std::hash<std::string>()(msg.sender);
            std::size_t h2 = std::hash<std::string>()(msg.receiver);
            std::size_t h3 = std::hash<std::string>()(msg.message);
            std::size_t h4 = std::hash<std::string>()(msg.timestamp);
            // Combine hashes (similar to Java's Objects.hash)
            return h1 ^ (h2 << 1) ^ (h3 << 2) ^ (h4 << 3);
        }
    };
}