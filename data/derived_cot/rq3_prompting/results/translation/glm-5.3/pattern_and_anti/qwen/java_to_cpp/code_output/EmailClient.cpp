#include <any>
#include <ctime>
#include <iomanip>
#include <map>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

class EmailClient {
private:
    std::string addr;
    double capacity;
    std::vector<std::map<std::string, std::any>> inbox;

    static std::string nowTimestamp() {
        std::time_t t = std::time(nullptr);
        std::tm tmv = *std::localtime(&t);
        std::ostringstream oss;
        oss << std::put_time(&tmv, "%Y-%m-%d %H:%M:%S");
        return oss.str();
    }

public:
    EmailClient(const std::string& addr, double capacity)
        : addr(addr), capacity(capacity), inbox() {}

    bool sendTo(EmailClient& recv, const std::string& content, double size) {
        if (!recv.isFullWithOneMoreEmail(size)) {
            std::string timestamp = nowTimestamp();
            std::map<std::string, std::any> email;
            email["sender"] = this->addr;
            email["receiver"] = recv.addr;
            email["content"] = content;
            email["size"] = size;
            email["time"] = timestamp;
            email["state"] = std::string("unread");
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
            if (it != email.end()) {
                if (const std::string* s = std::any_cast<std::string>(&it->second)) {
                    if (*s == "unread") {
                        email["state"] = std::string("read");
                        return &email;
                    }
                }
            }
        }
        return nullptr;
    }

    bool isFullWithOneMoreEmail(double size) {
        double occupiedSize = this->getOccupiedSize();
        return occupiedSize + size > this->capacity;
    }

    double getOccupiedSize() {
        double occupiedSize = 0;
        for (const auto& email : this->inbox) {
            auto it = email.find("size");
            if (it != email.end()) {
                if (const double* d = std::any_cast<double>(&it->second)) {
                    occupiedSize += *d;
                }
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
            auto emailIt = this->inbox.begin();
            std::map<std::string, std::any> email = *emailIt;
            this->inbox.erase(emailIt);
            auto it = email.find("size");
            if (it != email.end()) {
                if (const double* d = std::any_cast<double>(&it->second)) {
                    freedSpace += *d;
                }
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