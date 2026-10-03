#include <vector>
#include <string>
#include <chrono>
#include <ctime>
#include <cstdio>

class EmailClient {
private:
    std::string addr;
    double capacity;
    std::vector<EmailClient::Email> inbox;

public:
    struct Email {
        std::string sender;
        std::string receiver;
        std::string content;
        double size;
        std::string time;
        std::string state;
    };

    EmailClient(const std::string& addr, double capacity) : addr(addr), capacity(capacity) {}

    bool send_to(EmailClient& recv, const std::string& content, double size) {
        if (recv.is_full_with_one_more_email(size)) {
            recv.clear_inbox(size);
        }

        Email email;
        email.sender = addr;
        email.receiver = recv.addr;
        email.content = content;
        email.size = size;
        email.state = "unread";

        std::time_t now = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
        std::tm buf;
        std::memset(&buf, 0, sizeof(buf));
        buf = *std::localtime(&now);
        char buffer[20];
        std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", &buf);
        email.time = buffer;

        recv.inbox.push_back(email);
        return true;
    }

    Email* fetch() {
        for (auto& email : inbox) {
            if (email.state == "unread") {
                email.state = "read";
                return &email;
            }
        }
        return nullptr;
    }

    bool is_full_with_one_more_email(double size) {
        double occupied_size = get_occupied_size();
        return (occupied_size + size > capacity);
    }

    double get_occupied_size() {
        double total = 0.0;
        for (const auto& email : inbox) {
            total += email.size;
        }
        return total;
    }

    void clear_inbox(double size) {
        if (addr.empty()) {
            return;
        }

        double freed_space = 0.0;
        while (freed_space < size && !inbox.empty()) {
            Email email = inbox[0];
            freed_space += email.size;
            inbox.erase(inbox.begin());
        }
    }
};