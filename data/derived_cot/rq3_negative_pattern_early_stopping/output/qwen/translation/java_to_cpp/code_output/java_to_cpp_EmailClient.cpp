#include <vector>
#include <unordered_map>
#include <string>
#include <any>
#include <iostream>
#include <ctime>
#include <chrono>

class EmailClient {
private:
    std::string addr;
    double capacity;
    std::vector<std::unordered_map<std::string, std::any>> inbox;

    double getOccupiedSize() {
        double occupiedSize = 0;
        for (const auto& email : inbox) {
            try {
                double size = std::any_cast<double>(email.at("size"));
                occupiedSize += size;
            } catch (...) {
                // Ignore non-double values
            }
        }
        return occupiedSize;
    }

public:
    EmailClient(const std::string& addr, double capacity) : addr(addr), capacity(capacity) {}

    bool sendTo(EmailClient& recv, const std::string& content, double size) {
        if (!recv.isFullWithOneMoreEmail(size)) {
            auto timestamp = getCurrentTimestamp();
            std::unordered_map<std::string, std::any> email;
            email["sender"] = addr;
            email["receiver"] = recv.addr;
            email["content"] = content;
            email["size"] = size;
            email["time"] = timestamp;
            email["state"] = "unread";
            recv.inbox.push_back(email);
            return true;
        } else {
            clearInbox(size);
            if (recv.isFullWithOneMoreEmail(size)) {
                return false;
            }
            return sendTo(recv, content, size);
        }
    }

    std::unordered_map<std::string, std::any> fetch() {
        if (inbox.empty()) {
            return {};
        }
        for (auto& email : inbox) {
            if (email.at("state").cast<std::string>() == "unread") {
                email["state"] = "read";
                return email;
            }
        }
        return {};
    }

    bool isFullWithOneMoreEmail(double size) {
        double occupiedSize = getOccupiedSize();
        return occupiedSize + size > capacity;
    }

    void clearInbox(double size) {
        if (addr.empty()) {
            return;
        }
        double freedSpace = 0;
        while (freedSpace < size && !inbox.empty()) {
            auto email = inbox[0];
            inbox.erase(inbox.begin());
            try {
                double emailSize = std::any_cast<double>(email.at("size"));
                freedSpace += emailSize;
            } catch (...) {
                // Ignore non-double values
            }
        }
    }

    std::vector<std::unordered_map<std::string, std::any>> getInbox() {
        return inbox;
    }

    void setInbox(const std::vector<std::unordered_map<std::string, std::any>>& inbox) {
        this->inbox = inbox;
    }

private:
    std::string getCurrentTimestamp() {
        auto now = std::chrono::system_clock::now();
        std::time_t tt = std::chrono::system_clock::to_time_t(now);
        std::tm tm = *std::localtime(&tt);
        char buffer[20];
        std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", &tm);
        return std::string(buffer);
    }
};