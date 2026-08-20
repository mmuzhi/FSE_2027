#include <cstddef>
#include <ctime>
#include <functional>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace org {
namespace example {

class Chat {
public:
    class Message {
    public:
        Message(std::string sender, std::string receiver, std::string message, std::string timestamp)
            : sender(std::move(sender)),
              receiver(std::move(receiver)),
              message(std::move(message)),
              timestamp(std::move(timestamp)) {
        }

        const std::string& getSender() const { return sender; }
        const std::string& getReceiver() const { return receiver; }
        const std::string& getMessage() const { return message; }
        const std::string& getTimestamp() const { return timestamp; }

        bool operator==(const Message& other) const {
            return sender == other.sender
                && receiver == other.receiver
                && message == other.message
                && timestamp == other.timestamp;
        }

        bool operator!=(const Message& other) const {
            return !(*this == other);
        }

        // Mirrors java.util.Objects.hash(sender, receiver, message, timestamp).
        // Java int arithmetic wraps around; unsigned arithmetic reproduces that.
        int hashCode() const {
            unsigned int result = 1;
            result = 31u * result + static_cast<unsigned int>(stringHashCode(sender));
            result = 31u * result + static_cast<unsigned int>(stringHashCode(receiver));
            result = 31u * result + static_cast<unsigned int>(stringHashCode(message));
            result = 31u * result + static_cast<unsigned int>(stringHashCode(timestamp));
            return static_cast<int>(result);
        }

        // Mirrors String.format("Message{sender='%s', receiver='%s', message='%s', timestamp='%s'}", ...)
        std::string toString() const {
            return "Message{sender='" + sender
                 + "', receiver='" + receiver
                 + "', message='" + message
                 + "', timestamp='" + timestamp + "'}";
        }

    private:
        std::string sender;
        std::string receiver;
        std::string message;
        std::string timestamp;

        // Mirrors java.lang.String.hashCode()
        static int stringHashCode(const std::string& s) {
            unsigned int h = 0;
            for (unsigned char c : s) {
                h = 31u * h + static_cast<unsigned int>(c);
            }
            return static_cast<int>(h);
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
        return users.erase(username) > 0;
    }

    bool sendMessage(const std::string& sender, const std::string& receiver, const std::string& message) {
        auto senderEntry = users.find(sender);
        if (senderEntry == users.end()) {
            return false;
        }
        auto receiverEntry = users.find(receiver);
        if (receiverEntry == users.end()) {
            return false;
        }

        const std::string timestamp = currentTimestamp();

        const Message messageInfo(sender, receiver, message, timestamp);

        senderEntry->second.push_back(messageInfo);
        receiverEntry->second.push_back(messageInfo);
        return true;
    }

    // Returns a live reference to the user's message list (like the Java version,
    // where mutations through the returned list affect the Chat).
    // For an unknown user an empty list is returned (Java returns a fresh empty
    // ArrayList; here it is a shared list that the Chat itself never modifies).
    std::vector<Message>& getMessages(const std::string& username) {
        auto it = users.find(username);
        if (it == users.end()) {
            static std::vector<Message> empty;
            return empty;
        }
        return it->second;
    }

    const std::vector<Message>& getMessages(const std::string& username) const {
        auto it = users.find(username);
        if (it == users.end()) {
            static const std::vector<Message> empty;
            return empty;
        }
        return it->second;
    }

    std::unordered_map<std::string, std::vector<Message>>& getUsers() {
        return users;
    }

    const std::unordered_map<std::string, std::vector<Message>>& getUsers() const {
        return users;
    }

private:
    std::unordered_map<std::string, std::vector<Message>> users;

    // Mirrors new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date()):
    // current time formatted in the system's local time zone.
    static std::string currentTimestamp() {
        const std::time_t now = std::time(nullptr);
        std::tm localTime{};
#if defined(_MSC_VER)
        localtime_s(&localTime, &now);
#elif defined(_WIN32)
        if (const std::tm* tmp = std::localtime(&now)) {
            localTime = *tmp;
        }
#else
        localtime_r(&now, &localTime);
#endif
        char buffer[64];
        if (std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", &localTime) == 0) {
            return std::string();
        }
        return std::string(buffer);
    }
};

} // namespace example
} // namespace org

// Allows Message to be used as a key in unordered containers,
// mirroring the Java hashCode()/equals() contract.
namespace std {
template <>
struct hash<org::example::Chat::Message> {
    std::size_t operator()(const org::example::Chat::Message& message) const noexcept {
        return static_cast<std::size_t>(static_cast<unsigned int>(message.hashCode()));
    }
};
} // namespace std