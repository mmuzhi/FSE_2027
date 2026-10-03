#include <string>
#include <vector>
#include <ctime>

struct Email {
    std::string sender;
    std::string receiver;
    std::string content;
    double size;
    std::string time;
    std::string state;
};

class EmailClient {
public:
    std::string addr;
    double capacity;
    std::vector<Email> inbox;

    EmailClient(std::string addr, double capacity) 
        : addr(std::move(addr)), capacity(capacity) {}

    bool send_to(EmailClient& recv, const std::string& content, double size) {
        if (!recv.is_full_with_one_more_email(size)) {
            auto now = std::time(nullptr);
            auto tm = *std::localtime(&now);
            char buf[20];
            std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", &tm);
            
            Email email;
            email.sender = addr;
            email.receiver = recv.addr;
            email.content = content;
            email.size = size;
            email.time = std::string(buf);
            email.state = "unread";
            
            recv.inbox.push_back(email);
            return true;
        } else {
            clear_inbox(size);
            return false;
        }
    }

    Email* fetch() {
        if (inbox.empty()) {
            return nullptr;
        }
        for (size_t i = 0; i < inbox.size(); ++i) {
            if (inbox[i].state == "unread") {
                inbox[i].state = "read";
                return &inbox[i];
            }
        }
        return nullptr;
    }

    bool is_full_with_one_more_email(double size) const {
        double occupied_size = get_occupied_size();
        return occupied_size + size > capacity;
    }

    double get_occupied_size() const {
        double occupied_size = 0.0;
        for (const auto& email : inbox) {
            occupied_size += email.size;
        }
        return occupied_size;
    }

    void clear_inbox(double size) {
        if (addr.empty()) {
            return;
        }
        double freed_space = 0.0;
        while (freed_space < size && !inbox.empty()) {
            freed_space += inbox.front().size;
            inbox.erase(inbox.begin());
        }
    }
};