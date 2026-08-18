#include <chrono>
#include <cstdint>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>
#include <initializer_list>

class Chat {
public:
    class Message {
    private:
        std::string sender;
        std::string receiver;
        std::string message;
        std::string timestamp;

        // Mirrors java.lang.String.hashCode()
        static std::int32_t stringHashCode(const std::string& s) {
            std::uint32_t h = 0;
            for (unsigned char c : s) {
                h = 31u * h + static_cast<std::uint32_t>(c);
            }
            return static_cast<std::int32_t>(h);
        }

    public:
        Message() = default;

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

        bool operator!=(const Message& other) const {
            return !(*this == other);
        }

        // Mirrors Objects.hash(sender, receiver, message, timestamp)
        std::int32_t hashCode() const {
            std::uint32_t result = 1;
            for (std::int32_t h : {stringHashCode(sender), stringHashCode(receiver),
                                   stringHashCode(message), stringHashCode(timestamp)}) {
                result = 31u * result + static_cast<std::uint32_t>(h);
            }
            return static_cast<std::int32_t>(result);
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
        users.emplace(username, std::vector<Message>{});
        return true;
    }

    bool removeUser(const std::string& username) {
        auto it = users.find(username);
        if (it != users.end()) {
            users.erase(it);
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

    std::vector<Message>& getMessages(const std::string& username) {
        static std::vector<Message> empty;
        auto it = users.find(username);
        if (it == users.end()) {
            empty.clear(); // keep the shared empty list pristine, like a fresh ArrayList per call
            return empty;
        }
        return it->second;
    }

    std::unordered_map<std::string, std::vector<Message>>& getUsers() {
        return users;
    }

private:
    std::unordered_map<std::string, std::vector<Message>> users;

    // Equivalent of new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date())
    static std::string currentTimestamp() {
        const std::time_t now =
            std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
        std::tm tmv{};
#ifdef _WIN32
        localtime_s(&tmv, &now);
#else
        localtime_r(&now, &tmv);
#endif
        std::ostringstream oss;
        oss << std::put_time(&tmv, "%Y-%m-%d %H:%M:%S");
        return oss.str();
    }
};