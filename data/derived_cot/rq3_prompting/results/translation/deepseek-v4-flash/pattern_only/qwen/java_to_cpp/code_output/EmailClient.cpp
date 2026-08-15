#include <string>
#include <vector>
#include <unordered_map>
#include <any>
#include <memory>
#include <ctime>
#include <sstream>
#include <iomanip>
#include <stdexcept>

using Email = std::unordered_map<std::string, std::any>;
using EmailPtr = std::shared_ptr<Email>;
using Inbox = std::vector<EmailPtr>;

class EmailClient {
private:
    std::string addr;
    double capacity;
    std::shared_ptr<Inbox> inbox;

    Inbox& inboxRef() {
        if (!inbox) throw std::runtime_error("NullPointerException");
        return *inbox;
    }

    const Inbox& inboxRef() const {
        if (!inbox) throw std::runtime_error("NullPointerException");
        return *inbox;
    }

    static std::string currentTimestamp() {
        std::time_t t = std::time(nullptr);
        std::tm tm = *std::localtime(&t);
        std::ostringstream oss;
        oss << std::put_time(&tm, "%Y-%m-%d %H:%M:%S");
        return oss.str();
    }

    static bool getNumberValue(const std::any& val, double& out) {
        if (auto p = std::any_cast<double>(&val)) { out = *p; return true; }
        if (auto p = std::any_cast<float>(&val)) { out = *p; return true; }
        if (auto p = std::any_cast<int>(&val)) { out = *p; return true; }
        if (auto p = std::any_cast<long>(&val)) { out = *p; return true; }
        if (auto p = std::any_cast<long long>(&val)) { out = *p; return true; }
        if (auto p = std::any_cast<short>(&val)) { out = *p; return true; }
        if (auto p = std::any_cast<signed char>(&val)) { out = *p; return true; }
        if (auto p = std::any_cast<unsigned int>(&val)) { out = *p; return true; }
        if (auto p = std::any_cast<unsigned long>(&val)) { out = *p; return true; }
        if (auto p = std::any_cast<unsigned long long>(&val)) { out = *p; return true; }
        if (auto p = std::any_cast<unsigned short>(&val)) { out = *p; return true; }
        if (auto p = std::any_cast<unsigned char>(&val)) { out = *p; return true; }
        return false;
    }

    static bool isUnread(const Email& email) {
        auto it = email.find("state");
        if (it == email.end()) return false;
        const std::any& val = it->second;
        if (auto p = std::any_cast<std::string>(&val)) return *p == "unread";
        if (auto p = std::any_cast<const char*>(&val)) return std::string(*p) == "unread";
        if (auto p = std::any_cast<char*>(&val)) return std::string(*p) == "unread";
        return false;
    }

public:
    EmailClient(const std::string& addr, double capacity)
        : addr(addr), capacity(capacity), inbox(std::make_shared<Inbox>()) {}

    bool sendTo(EmailClient& recv, const std::string& content, double size) {
        if (!recv.isFullWithOneMoreEmail(size)) {
            std::string timestamp = currentTimestamp();
            auto email = std::make_shared<Email>();
            (*email)["sender"] = this->addr;
            (*email)["receiver"] = recv.addr;
            (*email)["content"] = content;
            (*email)["size"] = size;
            (*email)["time"] = timestamp;
            (*email)["state"] = std::string("unread");
            recv.inboxRef().push_back(email);
            return true;
        } else {
            this->clearInbox(size);
            if (recv.isFullWithOneMoreEmail(size)) {
                return false;
            }
            return sendTo(recv, content, size);
        }
    }

    std::shared_ptr<Email> fetch() {
        auto& inb = inboxRef();
        if (inb.empty()) {
            return nullptr;
        }
        for (auto& emailPtr : inb) {
            if (!emailPtr) throw std::runtime_error("NullPointerException");
            if (isUnread(*emailPtr)) {
                (*emailPtr)["state"] = std::string("read");
                return emailPtr;
            }
        }
        return nullptr;
    }

    bool isFullWithOneMoreEmail(double size) const {
        double occupiedSize = this->getOccupiedSize();
        return occupiedSize + size > this->capacity;
    }

    double getOccupiedSize() const {
        const auto& inb = inboxRef();
        double occupiedSize = 0;
        for (const auto& emailPtr : inb) {
            if (!emailPtr) throw std::runtime_error("NullPointerException");
            auto it = emailPtr->find("size");
            if (it != emailPtr->end()) {
                double sz = 0;
                if (getNumberValue(it->second, sz)) {
                    occupiedSize += sz;
                }
            }
        }
        return occupiedSize;
    }

    void clearInbox(double size) {
        if (this->addr.empty()) {
            return;
        }
        auto& inb = inboxRef();
        double freedSpace = 0;
        while (freedSpace < size && !inb.empty()) {
            auto& emailPtr = inb.front();
            if (!emailPtr) throw std::runtime_error("NullPointerException");
            auto it = emailPtr->find("size");
            if (it != emailPtr->end()) {
                double sz = 0;
                if (getNumberValue(it->second, sz)) {
                    freedSpace += sz;
                }
            }
            inb.erase(inb.begin());
        }
    }

    std::shared_ptr<Inbox> getInbox() {
        return inbox;
    }

    std::shared_ptr<const Inbox> getInbox() const {
        return inbox;
    }

    void setInbox(const std::shared_ptr<Inbox>& newInbox) {
        this->inbox = newInbox;
    }
};