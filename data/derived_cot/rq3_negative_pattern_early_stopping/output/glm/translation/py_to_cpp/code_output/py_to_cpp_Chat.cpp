#include <string>
#include <unordered_map>
#include <vector>
#include <chrono>
#include <iomanip>
#include <sstream>
#include <ctime>

struct MessageInfo {
    std::string sender;
    std::string receiver;
    std::string message;
    std::string timestamp;
};

class Chat {
private:
    std::unordered_map<std::string, std::vector<MessageInfo>> users;

    std::string get_current_timestamp() const {
        auto now = std::chrono::system_clock::now();
        auto in_time_t = std::chrono::system_clock::to_time_t(now);
        std::stringstream ss;
        ss << std::put_time(std::localtime(&in_time_t), "%Y-%m-%d %H:%M:%S");
        return ss.str();
    }

public:
    Chat() = default;

    bool add_user(const std::string& username) {
        if (users.count(username)) {
            return false;
        }
        users[username] = std::vector<MessageInfo>();
        return true;
    }

    bool remove_user(const std::string& username) {
        return users.erase(username) > 0;
    }

    bool send_message(const std::string& sender, const std::string& receiver, const std::string& message) {
        if (!users.count(sender) || !users.count(receiver)) {
            return false;
        }

        MessageInfo message_info;
        message_info.sender = sender;
        message_info.receiver = receiver;
        message_info.message = message;
        message_info.timestamp = get_current_timestamp();

        users[sender].push_back(message_info);
        users[receiver].push_back(message_info);
        return true;
    }

    std::vector<MessageInfo> get_messages(const std::string& username) const {
        auto it = users.find(username);
        if (it == users.end()) {
            return {};
        }
        return it->second;
    }
};