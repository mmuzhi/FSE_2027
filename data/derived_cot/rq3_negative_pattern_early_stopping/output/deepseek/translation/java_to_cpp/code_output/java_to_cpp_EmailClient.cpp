#include <vector>
#include <map>
#include <string>
#include <any>
#include <ctime>
#include <stdexcept>
#include <cstring>

class EmailClient {
private:
    std::string addr;
    double capacity;
    std::vector<std::map<std::string, std::any>> inbox;

    // Helper: get numeric value from std::any (handles double and int)
    static double toDouble(const std::any& val) {
        if (val.type() == typeid(double)) {
            return std::any_cast<double>(val);
        } else if (val.type() == typeid(int)) {
            return static_cast<double>(std::any_cast<int>(val));
        } else if (val.type() == typeid(float)) {
            return static_cast<double>(std::any_cast<float>(val));
        } else if (val.type() == typeid(long)) {
            return static_cast<double>(std::any_cast<long>(val));
        } else {
            throw std::bad_any_cast();
        }
    }

    // Helper: format current time as "yyyy-MM-dd HH:mm:ss"
    static std::string currentTimestamp() {
        std::time_t t = std::time(nullptr);
        std::tm tm = *std::localtime(&t);
        char buf[20];
        std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", &tm);
        return std::string(buf);
    }

public:
    EmailClient(const std::string& addr, double capacity)
        : addr(addr), capacity(capacity) {}

    bool sendTo(EmailClient& recv, const std::string& content, double size) {
        if (!recv.isFullWithOneMoreEmail(size)) {
            std::map<std::string, std::any> email;
            email["sender"] = this->addr;
            email["receiver"] = recv.addr;
            email["content"] = content;
            email["size"] = size;
            email["time"] = currentTimestamp();
            email["state"] = std::string("unread");
            recv.inbox.push_back(std::move(email));
            return true;
        } else {
            this->clearInbox(size);
            if (recv.isFullWithOneMoreEmail(size)) {
                return false;
            }
            return sendTo(recv, content, size); // Retry after clearing
        }
    }

    // Returns pointer to the email map, or nullptr if none
    std::map<std::string, std::any>* fetch() {
        if (inbox.empty()) {
            return nullptr;
        }
        for (auto& email : inbox) {
            auto it = email.find("state");
            if (it != email.end() && it->second.type() == typeid(std::string)) {
                if (std::any_cast<std::string>(it->second) == "unread") {
                    it->second = std::string("read");
                    return &email;
                }
            }
        }
        return nullptr;
    }

    bool isFullWithOneMoreEmail(double size) const {
        double occupied = getOccupiedSize();
        return occupied + size > capacity;
    }

    double getOccupiedSize() const {
        double total = 0.0;
        for (const auto& email : inbox) {
            auto it = email.find("size");
            if (it != email.end()) {
                try {
                    total += toDouble(it->second);
                } catch (const std::bad_any_cast&) {
                    // ignore non-numeric
                }
            }
        }
        return total;
    }

    void clearInbox(double size) {
        if (addr.empty()) {
            return;
        }
        double freed = 0.0;
        while (freed < size && !inbox.empty()) {
            auto& email = inbox.front();
            auto it = email.find("size");
            if (it != email.end()) {
                try {
                    freed += toDouble(it->second);
                } catch (const std::bad_any_cast&) {
                    // ignore non-numeric
                }
            }
            inbox.erase(inbox.begin());
        }
    }

    // Getter and setter for inbox
    std::vector<std::map<std::string, std::any>>& getInbox() {
        return inbox;
    }

    const std::vector<std::map<std::string, std::any>>& getInbox() const {
        return inbox;
    }

    void setInbox(const std::vector<std::map<std::string, std::any>>& newInbox) {
        inbox = newInbox;
    }
};