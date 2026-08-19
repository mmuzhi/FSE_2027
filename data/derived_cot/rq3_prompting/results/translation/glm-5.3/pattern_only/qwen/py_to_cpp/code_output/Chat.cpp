#include <ctime>
#include <iomanip>
#include <map>
#include <sstream>
#include <string>
#include <vector>

// Message record equivalent to the Python dict with keys
// 'sender', 'receiver', 'message', 'timestamp'.
struct MessageInfo {
    std::string sender;
    std::string receiver;
    std::string message;
    std::string timestamp;
};

class Chat {
public:
    Chat() : users() {}

    // Add a new user to the Chat.
    // Returns false if the user already exists, otherwise true.
    bool add_user(const std::string& username) {
        if (users.find(username) != users.end()) {
            return false;
        } else {
            users[username] = std::vector<MessageInfo>();
            return true;
        }
    }

    // Remove a user from the Chat.
    // Returns true if the user existed, otherwise false.
    bool remove_user(const std::string& username) {
        if (users.find(username) != users.end()) {
            users.erase(username);
            return true;
        } else {
            return false;
        }
    }

    // Send a message from a user to another user.
    // Returns false if the sender or the receiver is not in the Chat,
    // otherwise true.
    bool send_message(const std::string& sender,
                      const std::string& receiver,
                      const std::string& message) {
        if (users.find(sender) == users.end() ||
            users.find(receiver) == users.end()) {
            return false;
        }

        // Equivalent of datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        std::time_t now = std::time(nullptr);
        std::tm local_tm = *std::localtime(&now);
        std::ostringstream oss;
        oss << std::put_time(&local_tm, "%Y-%m-%d %H:%M:%S");

        MessageInfo message_info;
        message_info.sender = sender;
        message_info.receiver = receiver;
        message_info.message = message;
        message_info.timestamp = oss.str();

        users[sender].push_back(message_info);
        users[receiver].push_back(message_info);
        return true;
    }

    // Get all the messages of a user from the Chat.
    // Returns an empty list if the user is not in the Chat.
    std::vector<MessageInfo> get_messages(const std::string& username) {
        std::map<std::string, std::vector<MessageInfo> >::const_iterator it =
            users.find(username);
        if (it == users.end()) {
            return std::vector<MessageInfo>();
        }
        return it->second;
    }

private:
    std::map<std::string, std::vector<MessageInfo> > users;
};