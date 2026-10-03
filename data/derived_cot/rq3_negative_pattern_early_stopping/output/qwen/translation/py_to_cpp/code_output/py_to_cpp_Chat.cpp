#include <unordered_map>
#include <vector>
#include <string>
#include <ctime>
#include <iomanip>
#include <sstream>

struct Message {
    std::string sender;
    std::string receiver;
    std::string message;
    std::string timestamp;
};

class Chat {
private:
    std::unordered_map<std::string, std::vector<Message>> users;

public:
    // Add a new user
    bool add_user(const std::string& username) {
        if (users.find(username) != users.end()) {
            return false;
        }
        users[username] = std::vector<Message>();
        return true;
    }

    // Remove a user
    bool remove_user(const std::string& username) {
        if (users.find(username) != users.end()) {
            users.erase(username);
            return true;
        }
        return false;
    }

    // Send a message
    bool send_message(const std::string& sender, const std::string& receiver, const std::string& message) {
        // Check if both sender and receiver exist
        if (users.find(sender) == users.end() || users.find(receiver) == users.end()) {
            return false;
        }

        // Create timestamp
        std::time_t now = std::time(nullptr);
        std::tm* utc_time = std::gmtime(&now);
        char buffer[20];
        std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", utc_time);
        std::string timestamp(buffer);

        Message msg;
        msg.sender = sender;
        msg.receiver = receiver;
        msg.message = message;
        msg.timestamp = timestamp;

        // Add to sender's messages
        users[sender].push_back(msg);
        // Add to receiver's messages
        users[receiver].push_back(msg);

        return true;
    }

    // Get all messages for a user
    std::vector<Message> get_messages(const std::string& username) {
        if (users.find(username) == users.end()) {
            return std::vector<Message>();
        }
        return users[username];
    }
};