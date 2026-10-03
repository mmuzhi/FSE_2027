#include <string>
#include <unordered_map>
#include <vector>
#include <memory>
#include <chrono>
#include <ctime>
#include <iomanip>
#include <sstream>

class Chat {
public:
    Chat() = default;

    /**
     * Add a new user to the chat.
     * @param username The user's name.
     * @return true if the user was added, false if the user already exists.
     */
    bool add_user(const std::string& username) {
        if (users.find(username) != users.end()) {
            return false;
        }
        users[username] = {};
        return true;
    }

    /**
     * Remove a user from the chat.
     * @param username The user's name.
     * @return true if the user was removed, false if the user did not exist.
     */
    bool remove_user(const std::string& username) {
        auto it = users.find(username);
        if (it == users.end()) {
            return false;
        }
        users.erase(it);
        return true;
    }

    /**
     * Send a message from one user to another.  The message is stored in both users' message lists.
     * @param sender   The sender's name.
     * @param receiver The receiver's name.
     * @param message  The message text.
     * @return true if the message was sent (both users exist), false otherwise.
     */
    bool send_message(const std::string& sender, const std::string& receiver, const std::string& message) {
        if (users.find(sender) == users.end() || users.find(receiver) == users.end()) {
            return false;
        }
        std::string timestamp = get_current_timestamp();
        auto msg = std::make_shared<Message>(Message{sender, receiver, message, timestamp});
        users[sender].push_back(msg);
        users[receiver].push_back(msg);
        return true;
    }

    /**
     * Retrieve all messages for a given user.
     * @param username The user's name.
     * @return A vector of shared pointers to the user's messages (empty if the user does not exist).
     */
    std::vector<std::shared_ptr<Message>> get_messages(const std::string& username) {
        auto it = users.find(username);
        if (it == users.end()) {
            return {};
        }
        return it->second;   // returns a copy (as does the Python version when a user is missing)
    }

private:
    struct Message {
        std::string sender;
        std::string receiver;
        std::string message;
        std::string timestamp;
    };

    std::unordered_map<std::string, std::vector<std::shared_ptr<Message>>> users;

    /**
     * Get the current local time as a formatted string: "YYYY-MM-DD HH:MM:SS".
     */
    static std::string get_current_timestamp() {
        auto now = std::chrono::system_clock::now();
        auto time_t_now = std::chrono::system_clock::to_time_t(now);
        std::tm tm_now;
#ifdef _MSC_VER
        localtime_s(&tm_now, &time_t_now);
#else
        localtime_r(&time_t_now, &tm_now);
#endif
        std::stringstream ss;
        ss << std::put_time(&tm_now, "%Y-%m-%d %H:%M:%S");
        return ss.str();
    }
};