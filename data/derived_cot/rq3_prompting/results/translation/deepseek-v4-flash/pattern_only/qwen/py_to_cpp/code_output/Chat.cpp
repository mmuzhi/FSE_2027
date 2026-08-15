#include <string>
#include <unordered_map>
#include <vector>
#include <memory>
#include <ctime>
#include <chrono>

class Chat {
public:
    using Message = std::unordered_map<std::string, std::string>;
    using MessagePtr = std::shared_ptr<Message>;
    using MessageList = std::vector<MessagePtr>;

    Chat() = default;

    bool add_user(const std::string& username) {
        if (users.find(username) != users.end()) {
            return false;
        }
        users[username] = std::make_shared<MessageList>();
        return true;
    }

    bool remove_user(const std::string& username) {
        auto it = users.find(username);
        if (it == users.end()) {
            return false;
        }
        users.erase(it);
        return true;
    }

    bool send_message(const std::string& sender, const std::string& receiver, const std::string& message) {
        auto sit = users.find(sender);
        auto rit = users.find(receiver);
        if (sit == users.end() || rit == users.end()) {
            return false;
        }

        auto now = std::chrono::system_clock::now();
        std::time_t t = std::chrono::system_clock::to_time_t(now);
        char buf[20];
        std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", std::localtime(&t));

        auto msg = std::make_shared<Message>();
        (*msg)["sender"] = sender;
        (*msg)["receiver"] = receiver;
        (*msg)["message"] = message;
        (*msg)["timestamp"] = std::string(buf);

        sit->second->push_back(msg);
        rit->second->push_back(msg);
        return true;
    }

    std::shared_ptr<MessageList> get_messages(const std::string& username) {
        auto it = users.find(username);
        if (it == users.end()) {
            return std::make_shared<MessageList>();
        }
        return it->second;
    }

    std::unordered_map<std::string, std::shared_ptr<MessageList>> users;
};