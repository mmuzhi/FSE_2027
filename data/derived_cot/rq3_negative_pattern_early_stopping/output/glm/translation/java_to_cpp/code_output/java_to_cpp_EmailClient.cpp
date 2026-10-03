#include <string>
#include <vector>
#include <unordered_map>
#include <any>
#include <chrono>
#include <iomanip>
#include <sstream>

namespace org {
namespace example {

class EmailClient {
private:
    std::string addr;
    double capacity;
    std::vector<std::unordered_map<std::string, std::any>> inbox;

public:
    EmailClient(const std::string& addr, double capacity) {
        this->addr = addr;
        this->capacity = capacity;
    }

    bool sendTo(EmailClient& recv, const std::string& content, double size) {
        if (!recv.isFullWithOneMoreEmail(size)) {
            auto now = std::chrono::system_clock::now();
            auto in_time_t = std::chrono::system_clock::to_time_t(now);
            std::stringstream ss;
            ss << std::put_time(std::localtime(&in_time_t), "%Y-%m-%d %H:%M:%S");
            std::string timestamp = ss.str();

            std::unordered_map<std::string, std::any> email;
            email["sender"] = this->addr;
            email["receiver"] = recv.addr;
            email["content"] = content;
            email["size"] = size;
            email["time"] = timestamp;
            email["state"] = std::string("unread");
            recv.inbox.push_back(email);
            return true;
        } else {
            this->clearInbox(size);
            if (recv.isFullWithOneMoreEmail(size)) {
                return false;
            }
            return sendTo(recv, content, size);
        }
    }

    std::unordered_map<std::string, std::any>* fetch() {
        if (this->inbox.empty()) {
            return nullptr;
        }
        for (auto& email : this->inbox) {
            auto it = email.find("state");
            if (it != email.end()) {
                const std::string* state_ptr = std::any_cast<std::string>(&it->second);
                if (state_ptr && *state_ptr == "unread") {
                    email["state"] = std::string("read");
                    return &email;
                }
            }
        }
        return nullptr;
    }

    bool isFullWithOneMoreEmail(double size) const {
        double occupiedSize = this->getOccupiedSize();
        return occupiedSize + size > this->capacity;
    }

    double getOccupiedSize() const {
        double occupiedSize = 0;
        for (const auto& email : this->inbox) {
            auto it = email.find("size");
            if (it != email.end()) {
                const std::any& sizeObj = it->second;
                if (const double* d = std::any_cast<double>(&sizeObj)) {
                    occupiedSize += *d;
                } else if (const int* i = std::any_cast<int>(&sizeObj)) {
                    occupiedSize += *i;
                } else if (const float* f = std::any_cast<float>(&sizeObj)) {
                    occupiedSize += *f;
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
            auto it = this->inbox.begin();
            auto email = std::move(*it);
            this->inbox.erase(it);
            
            auto sizeIt = email.find("size");
            if (sizeIt != email.end()) {
                const std::any& sizeObj = sizeIt->second;
                if (const double* d = std::any_cast<double>(&sizeObj)) {
                    freedSpace += *d;
                } else if (const int* i = std::any_cast<int>(&sizeObj)) {
                    freedSpace += *i;
                } else if (const float* f = std::any_cast<float>(&sizeObj)) {
                    freedSpace += *f;
                }
            }
        }
    }

    std::vector<std::unordered_map<std::string, std::any>>& getInbox() {
        return this->inbox;
    }

    void setInbox(const std::vector<std::unordered_map<std::string, std::any>>& inbox) {
        this->inbox = inbox;
    }
};

}
}