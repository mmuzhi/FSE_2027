#include <string>
#include <vector>
#include <unordered_map>
#include <ctime>

// This is a chat class with the functions of adding users, removing users,
// sending messages, and obtaining messages.

struct Message {
    std::string sender;
    std::string receiver;
    std::string message;
    std::string timestamp;
};

class Chat {
public:
    std::unordered_map<std::string, std::vector<Message>> users;

    Chat() = default;

    // Add a new user to the Chat.
    // Returns false if the user is already in the Chat, otherwise true.
    bool add_user(const std::string& username) {
        if (users.count(username)) {
            return false;
        }
        users[username] = {};
        return true;
    }

    // Remove a user from the Chat.
    // Returns true if the user is already in the Chat, otherwise false.
    bool remove_user(const std::string& username) {
        auto it = users.find(username);
        if (it != users.end()) {
            users.erase(it);
            return true;
        }
        return false;
    }

    // Send a message from a user to another user.
    // Returns false if the sender or the receiver is not in the Chat, otherwise true.
    bool send_message(const std::string& sender, const std::string& receiver, const std::string& message) {
        if (users.find(sender) == users.end() || users.find(receiver) == users.end()) {
            return false;
        }

        Message message_info;
        message_info.sender = sender;
        message_info.receiver = receiver;
        message_info.message = message;
        message_info.timestamp = now_timestamp();

        users[sender].push_back(message_info);
        users[receiver].push_back(message_info);
        return true;
    }

    // Get all the messages of a user from the Chat.
    // Returns an empty list if the user is not in the Chat.
    std::vector<Message> get_messages(const std::string& username) const {
        auto it = users.find(username);
        if (it == users.end()) {
            return {};
        }
        return it->second;
    }

private:
    static std::string now_timestamp() {
        std::time_t now = std::time(nullptr);
        std::tm tm_buf;
#ifdef _WIN32
        localtime_s(&tm_buf, &now);
#else
        localtime_r(&now, &tm_buf);
#endif
        char buf[20];
        std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", &tm_buf);
        return std::string(buf);
    }
};