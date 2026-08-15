#include <unordered_map>
#include <vector>
#include <string>
#include <sstream>
#include <iomanip>
#include <ctime>
#include <chrono>
#include <memory>
#include <functional>
#include <utility>

class Chat {
public:
    class Message {
    public:
        Message(std::string sender, std::string receiver, std::string message, std::string timestamp)
            : sender_(std::move(sender)), receiver_(std::move(receiver)), message_(std::move(message)), timestamp_(std::move(timestamp)) {}

        const std::string& getSender() const { return sender_; }
        const std::string& getReceiver() const { return receiver_; }
        const std::string& getMessage() const { return message_; }
        const std::string& getTimestamp() const { return timestamp_; }

        bool operator==(const Message& other) const {
            return sender_ == other.sender_ &&
                   receiver_ == other.receiver_ &&
                   message_ == other.message_ &&
                   timestamp_ == other.timestamp_;
        }

        bool operator!=(const Message& other) const {
            return !(*this == other);
        }

        std::string toString() const {
            std::ostringstream oss;
            oss << "Message{sender='" << sender_ << "', receiver='" << receiver_ << "', message='" << message_ << "', timestamp='" << timestamp_ << "'}";
            return oss.str();
        }

        size_t hash() const {
            size_t h1 = std::hash<std::string>{}(sender_);
            size_t h2 = std::hash<std::string>{}(receiver_);
            size_t h3 = std::hash<std::string>{}(message_);
            size_t h4 = std::hash<std::string>{}(timestamp_);
            size_t result = h1;
            result = result * 31 + h2;
            result = result * 31 + h3;
            result = result * 31 + h4;
            return result;
        }

    private:
        std::string sender_;
        std::string receiver_;
        std::string message_;
        std::string timestamp_;
    };

    Chat() = default;

    Chat(const Chat&) = delete;
    Chat& operator=(const Chat&) = delete;

    bool addUser(const std::string& username) {
        if (users_.find(username) != users_.end()) {
            return false;
        }
        users_.emplace(username, std::make_shared<std::vector<Message>>());
        return true;
    }

    bool removeUser(const std::string& username) {
        auto it = users_.find(username);
        if (it == users_.end()) {
            return false;
        }
        users_.erase(it);
        return true;
    }

    bool sendMessage(const std::string& sender, const std::string& receiver, const std::string& message) {
        auto senderIt = users_.find(sender);
        auto receiverIt = users_.find(receiver);
        if (senderIt == users_.end() || receiverIt == users_.end()) {
            return false;
        }

        std::string timestamp = currentTimestamp();
        Message msg(sender, receiver, message, timestamp);

        senderIt->second->push_back(msg);
        receiverIt->second->push_back(msg);
        return true;
    }

    std::shared_ptr<std::vector<Message>> getMessages(const std::string& username) {
        auto it = users_.find(username);
        if (it == users_.end()) {
            return std::make_shared<std::vector<Message>>();
        }
        return it->second;
    }

    std::shared_ptr<const std::vector<Message>> getMessages(const std::string& username) const {
        auto it = users_.find(username);
        if (it == users_.end()) {
            return std::make_shared<const std::vector<Message>>();
        }
        return it->second;
    }

    std::unordered_map<std::string, std::shared_ptr<std::vector<Message>>>& getUsers() {
        return users_;
    }

    const std::unordered_map<std::string, std::shared_ptr<std::vector<Message>>>& getUsers() const {
        return users_;
    }

private:
    std::string currentTimestamp() const {
        auto now = std::chrono::system_clock::now();
        std::time_t t = std::chrono::system_clock::to_time_t(now);
        std::tm* tm = std::localtime(&t);
        std::ostringstream oss;
        oss << std::put_time(tm, "%Y-%m-%d %H:%M:%S");
        return oss.str();
    }

    std::unordered_map<std::string, std::shared_ptr<std::vector<Message>>> users_;
};

namespace std {
    template<>
    struct hash<Chat::Message> {
        size_t operator()(const Chat::Message& m) const {
            return m.hash();
        }
    };
}