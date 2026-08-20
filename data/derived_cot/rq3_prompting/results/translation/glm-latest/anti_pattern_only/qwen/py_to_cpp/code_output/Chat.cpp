#include <ctime>
#include <map>
#include <string>
#include <vector>

// A chat class with the functions of adding users, removing users,
// sending messages, and obtaining messages.

class Chat {
public:
    // One message; equivalent to the Python dict with keys
    // 'sender', 'receiver', 'message', 'timestamp'.
    struct Message {
        std::string sender;
        std::string receiver;
        std::string message;
        std::string timestamp;
    };

    // Equivalent of the Python attribute self.users.
    std::map<std::string, std::vector<Message>> users;

    // Initialize the Chat with an attribute users, which is an empty map.
    Chat() = default;

    // Add a new user to the Chat.
    // Returns false if the user is already in the Chat, otherwise true.
    bool add_user(const std::string& username) {
        // emplace() inserts only when the key is absent; .second reports insertion.
        return users.emplace(username, std::vector<Message>()).second;
    }

    // Remove a user from the Chat.
    // Returns true if the user was in the Chat, otherwise false.
    bool remove_user(const std::string& username) {
        // erase(key) returns the number of elements removed (0 or 1).
        return users.erase(username) > 0;
    }

    // Send a message from a user to another user.
    // Returns false if the sender or the receiver is not in the Chat,
    // otherwise true.
    bool send_message(const std::string& sender, const std::string& receiver,
                      const std::string& message) {
        if (users.find(sender) == users.end() ||
            users.find(receiver) == users.end()) {
            return false;
        }

        // timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        const std::string timestamp = current_timestamp();
        const Message message_info = {sender, receiver, message, timestamp};

        // If sender == receiver, the message is appended twice to that user,
        // exactly as in the Python original.
        users[sender].push_back(message_info);
        users[receiver].push_back(message_info);
        return true;
    }

    // Get all the messages of a user from the Chat.
    // Returns an empty list if the user is not in the Chat.
    const std::vector<Message>& get_messages(const std::string& username) const {
        static const std::vector<Message> empty;
        auto it = users.find(username);
        return (it != users.end()) ? it->second : empty;
    }

private:
    // datetime.now().strftime("%Y-%m-%d %H:%M:%S"): current local time string.
    static std::string current_timestamp() {
        const std::time_t now = std::time(nullptr);
        const std::tm* local_tm = std::localtime(&now);
        char buffer[20];  // "YYYY-MM-DD HH:MM:SS" (19 chars) + '\0'
        if (local_tm != nullptr &&
            std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", local_tm) != 0) {
            return std::string(buffer);
        }
        return std::string();
    }
};