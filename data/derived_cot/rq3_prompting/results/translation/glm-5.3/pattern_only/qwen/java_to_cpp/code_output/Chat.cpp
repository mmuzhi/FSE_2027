#pragma once

#include <ctime>
#include <functional>
#include <iomanip>
#include <sstream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

class Chat {
public:
    class Message {
    private:
        std::string sender;
        std::string receiver;
        std::string message;
        std::string timestamp;

    public:
        Message(std::string sender, std::string receiver, std::string message, std::string timestamp)
            : sender(std::move(sender)),
              receiver(std::move(receiver)),
              message(std::move(message)),
              timestamp(std::move(timestamp)) {}

        const std::string& getSender() const { return sender; }
        const std::string& getReceiver() const { return receiver; }
        const std::string& getMessage() const { return message; }
        const std::string& getTimestamp() const { return timestamp; }

        bool operator==(const Message& other) const {
            return sender == other.sender &&
                   receiver == other.receiver &&
                   message == other.message &&
                   timestamp == other.timestamp;
        }

        int hashCode() const {
            // Mirrors java.util.Objects.hash / String.hashCode combination
            std::size_t h = 0;
            for (const std::string* s : {&sender, &receiver, &message, &timestamp}) {
                std::size_t hs = 0;
                for (char c : *s) {
                    hs = 31 * hs + static_cast<unsigned char>(c);
                }
                h = 31 * h + hs;
            }
            return static_cast<int>(static_cast<unsigned int>(h));
        }

        std::string toString() const {
            std::ostringstream oss;
            oss << "Message{sender='" << sender << "', receiver='" << receiver
                << "', message='" << message << "', timestamp='" << timestamp << "'}";
            return oss.str();
        }
    };

    Chat() = default;

    bool addUser(const std::string& username) {
        if (users.find(username) != users.end()) {
            return false;
        }
        users.emplace(username, std::vector<Message>());
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

        std::string timestamp = currentTimestamp();

        Message messageInfo(sender, receiver, message, timestamp);

        users[sender].push_back(messageInfo);
        users[receiver].push_back(messageInfo);
        return true;
    }

    // Java returns a reference to the live list (or a fresh empty list for unknown users).
    std::vector<Message>& getMessages(const std::string& username) {
        if (users.find(username) == users.end()) {
            static std::vector<Message> empty;
            empty.clear();  // fresh empty list each call, like `new ArrayList<>()`
            return empty;
        }
        return users[username];
    }

    std::unordered_map<std::string, std::vector<Message>>& getUsers() {
        return users;
    }

private:
    std::unordered_map<std::string, std::vector<Message>> users;

    static std::string currentTimestamp() {
        std::time_t now = std::time(nullptr);
        std::tm localTm{};
#ifdef _WIN32
        localtime_s(&localTm, &now);
#else
        localtime_r(&now, &localTm);
#endif
        std::ostringstream oss;
        oss << std::put_time(&localTm, "%Y-%m-%d %H:%M:%S");
        return oss.str();
    }
};