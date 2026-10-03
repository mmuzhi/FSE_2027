#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>
#include <ctime>
#include <memory>
#include <stdexcept>

class Chat {
    class Message {
    private:
        std::string sender;
        std::string receiver;
        std::string message;
        std::string timestamp;

    public:
        Message(const std::string& sender, const std::string& receiver, const std::string& message, const std::string& timestamp)
            : sender(sender), receiver(receiver), message(message), timestamp(timestamp) {}

        std::string getSender() const { return sender; }
        std::string getReceiver() const { return receiver; }
        std::string getMessage() const { return message; }
        std::string getTimestamp() const { return timestamp; }

        bool equals(const Message& other) const {
            return sender == other.sender && 
                   receiver == other.receiver && 
                   message == other.message && 
                   timestamp == other.timestamp;
        }

        bool operator==(const Message& other) const {
            return sender == other.sender && 
                   receiver == other.receiver && 
                   message == other.message && 
                   timestamp == other.timestamp;
        }

        std::string toString() const {
            return "Message{sender='" + sender + "', receiver='" + receiver + "', message='" + message + "', timestamp='" + timestamp + "'}";
        }
    };

    std::unordered_map<std::string, std::vector<Message>> users;

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
        if (users.find(username) != users.end()) {
            users.erase(username);
            return true;
        }
        return false;
    }

    bool sendMessage(const std::string& sender, const std::string& receiver, const std::string& message) {
        if (users.find(sender) == users.end() || users.find(receiver) == users.end()) {
            return false;
        }

        // Format current time
        std::time_t now = std::time(nullptr);
        std::tm* currentTime = std::localtime(&now);

        char buffer[20];
        std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", currentTime);
        std::string timestamp(buffer);

        Message messageInfo(sender, receiver, message, timestamp);

        users[sender].push_back(messageInfo);
        users[receiver].push_back(messageInfo);
        return true;
    }

    std::vector<Message> getMessages(const std::string& username) {
        if (users.find(username) == users.end()) {
            return std::vector<Message>();
        }
        return users[username];
    }

    std::unordered_map<std::string, std::vector<Message>>& getUsers() {
        return users;
    }
};