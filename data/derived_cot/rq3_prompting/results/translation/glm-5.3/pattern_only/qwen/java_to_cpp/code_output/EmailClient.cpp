#include <any>
#include <chrono>
#include <ctime>
#include <iomanip>
#include <map>
#include <sstream>
#include <string>
#include <typeinfo>
#include <utility>
#include <vector>

class EmailClient {
private:
    std::string addr;
    double capacity;
    std::vector<std::map<std::string, std::any>> inbox;

    static std::string currentTimestamp() {
        std::time_t t = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
        std::tm tmv{};
#ifdef _WIN32
        localtime_s(&tmv, &t);
#else
        localtime_r(&t, &tmv);
#endif
        std::ostringstream oss;
        oss << std::put_time(&tmv, "%Y-%m-%d %H:%M:%S");
        return oss.str();
    }

public:
    EmailClient(const std::string& addr, double capacity)
        : addr(addr), capacity(capacity), inbox() {}

    bool sendTo(EmailClient& recv, const std::string& content, double size) {
        if (!recv.isFullWithOneMoreEmail(size)) {
            std::string timestamp = currentTimestamp();
            std::map<std::string, std::any> email;
            email["sender"] = std::any(this->addr);
            email["receiver"] = std::any(recv.addr);
            email["content"] = std::any(content);
            email["size"] = std::any(size);
            email["time"] = std::any(timestamp);
            email["state"] = std::any(std::string("unread"));
            recv.inbox.push_back(std::move(email));
            return true;
        }
        else {
            this->clearInbox(size);
            if (recv.isFullWithOneMoreEmail(size)) {
                return false;
            }
            return sendTo(recv, content, size); // Retry sending after clearing
        }
    }

    std::map<std::string, std::any>* fetch() {
        if (this->inbox.empty()) {
            return nullptr;
        }
        for (auto& email : this->inbox) {
            auto it = email.find("state");
            if (it != email.end() && it->second.type() == typeid(std::string) &&
                std::any_cast<const std::string&>(it->second) == "unread") {
                email["state"] = std::any(std::string("read"));
                return &email;
            }
        }
        return nullptr;
    }

    bool isFullWithOneMoreEmail(double size) const {
        double occupiedSize = this->getOccupiedSize();
        return occupiedSize + size > this.capacity;
    }

    double getOccupiedSize() const {
        double occupiedSize = 0;
        for (const auto& email : this->inbox) {
            auto it = email.find("size");
            if (it != email.end() && it->second.type() == typeid(double)) {
                occupiedSize += std::any_cast<double>(it->second);
            }
        }
        return occupiedSize;
    }

    void clearInbox(double size) {
        if (this->addr.empty()) {
            return;
        }
        double freedSpace = 0;
        while (freedSpace < size && !this->inbox.empty()) {
            std::map<std::string, std::any> email = this->inbox.front();
            this->inbox.erase(this->inbox.begin());
            auto it = email.find("size");
            if (it != email.end() && it->second.type() == typeid(double)) {
                freedSpace += std::any_cast<double>(it->second);
            }
        }
    }

    std::vector<std::map<std::string, std::any>>& getInbox() {
        return this->inbox;
    }

    void setInbox(std::vector<std::map<std::string, std::any>> inbox) {
        this->inbox = std::move(inbox);
    }
};