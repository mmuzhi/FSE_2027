// Requires C++17 (std::any, nested namespace definitions)
#include <any>
#include <chrono>
#include <ctime>
#include <iomanip>
#include <memory>
#include <sstream>
#include <string>
#include <typeinfo>
#include <unordered_map>
#include <utility>
#include <vector>

namespace org::example {

// Analogue of Map<String, Object> for a single email.
using Email = std::unordered_map<std::string, std::any>;
// Java object references (to emails and to the inbox list) are modeled with shared_ptr,
// so mutations stay visible through every reference, as in Java.
using EmailRef = std::shared_ptr<Email>;
using Inbox = std::vector<EmailRef>;
using InboxRef = std::shared_ptr<Inbox>;

class EmailClient {
private:
    std::string addr;
    double capacity;
    InboxRef inbox;

    // LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"))
    static std::string nowTimestamp() {
        const std::time_t now =
            std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
        std::tm tmBuf{};
        if (const std::tm* local = std::localtime(&now)) {
            tmBuf = *local;
        }
        std::ostringstream oss;
        oss << std::put_time(&tmBuf, "%Y-%m-%d %H:%M:%S");
        return oss.str();
    }

    // Equivalent of (obj instanceof Number) followed by ((Number) obj).doubleValue().
    static bool tryAsNumber(const std::any& value, double& out) {
        if (!value.has_value()) {
            return false;
        }
        const std::type_info& type = value.type();
        if (type == typeid(double))    { out = std::any_cast<double>(value); return true; }
        if (type == typeid(float))     { out = std::any_cast<float>(value); return true; }
        if (type == typeid(int))       { out = std::any_cast<int>(value); return true; }
        if (type == typeid(long))      { out = static_cast<double>(std::any_cast<long>(value)); return true; }
        if (type == typeid(long long)) { out = static_cast<double>(std::any_cast<long long>(value)); return true; }
        if (type == typeid(short))     { out = std::any_cast<short>(value); return true; }
        return false;
    }

    static bool tryGetSize(const Email& email, double& out) {
        const auto it = email.find("size");
        if (it == email.end()) {
            return false;
        }
        return tryAsNumber(it->second, out);
    }

public:
    EmailClient(std::string addr, double capacity)
        : addr(std::move(addr)), capacity(capacity), inbox(std::make_shared<Inbox>()) {}

    bool sendTo(EmailClient& recv, const std::string& content, double size) {
        if (!recv.isFullWithOneMoreEmail(size)) {
            const std::string timestamp = nowTimestamp();
            Email email;
            email["sender"] = this->addr;
            email["receiver"] = recv.addr;
            email["content"] = content;
            email["size"] = size;
            email["time"] = timestamp;
            email["state"] = std::string("unread");
            recv.inbox->push_back(std::make_shared<Email>(std::move(email)));
            return true;
        } else {
            this->clearInbox(size);
            if (recv.isFullWithOneMoreEmail(size)) {
                return false;
            }
            return sendTo(recv, content, size); // Retry sending after clearing
        }
    }

    // Returns nullptr where the Java version returns null.
    EmailRef fetch() {
        if (this->inbox->empty()) {
            return nullptr;
        }
        for (const EmailRef& email : *this->inbox) {
            const auto it = email->find("state");
            if (it == email->end()) {
                continue;
            }
            const std::string* state = std::any_cast<std::string>(&it->second);
            if (state != nullptr && *state == "unread") {
                (*email)["state"] = std::string("read");
                return email;
            }
        }
        return nullptr;
    }

    bool isFullWithOneMoreEmail(double size) const {
        const double occupiedSize = this->getOccupiedSize();
        return occupiedSize + size > this->capacity;
    }

    double getOccupiedSize() const {
        double occupiedSize = 0;
        double size = 0;
        for (const EmailRef& email : *this->inbox) {
            if (tryGetSize(*email, size)) {
                occupiedSize += size;
            }
        }
        return occupiedSize;
    }

    void clearInbox(double size) {
        if (this->addr.empty()) {
            return;
        }
        double freedSpace = 0;
        double emailSize = 0;
        while (freedSpace < size && !this->inbox->empty()) {
            const EmailRef email = this->inbox->front();
            this->inbox->erase(this->inbox->begin());
            if (tryGetSize(*email, emailSize)) {
                freedSpace += emailSize;
            }
        }
    }

    InboxRef getInbox() const {
        return this->inbox;
    }

    void setInbox(InboxRef inbox) {
        this->inbox = std::move(inbox);
    }
};

} // namespace org::example