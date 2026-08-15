#include <vector>
#include <string>
#include <memory>
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
    std::vector<std::shared_ptr<Email>> inbox;

    EmailClient(const std::string& addr, double capacity)
        : addr(addr), capacity(capacity) {}

    bool send_to(EmailClient& recv, const std::string& content, double size) {
        if (!recv.is_full_with_one_more_email(size)) {
            auto email = std::make_shared<Email>();
            email->sender = this->addr;
            email->receiver = recv.addr;
            email->content = content;
            email->size = size;
            email->time = current_time();
            email->state = "unread";
            recv.inbox.push_back(email);
            return true;
        } else {
            this->clear_inbox(size);
            return false;
        }
    }

    std::shared_ptr<Email> fetch() {
        if (inbox.empty()) {
            return nullptr;
        }
        for (auto& email : inbox) {
            if (email->state == "unread") {
                email->state = "read";
                return email;
            }
        }
        return nullptr;
    }

    bool is_full_with_one_more_email(double size) const {
        double occupied_size = get_occupied_size();
        return occupied_size + size > capacity;
    }

    double get_occupied_size() const {
        double occupied_size = 0;
        for (const auto& email : inbox) {
            occupied_size += email->size;
        }
        return occupied_size;
    }

    void clear_inbox(double size) {
        if (addr.empty()) {
            return;
        }
        double freed_space = 0;
        while (freed_space < size && !inbox.empty()) {
            freed_space += inbox.front()->size;
            inbox.erase(inbox.begin());
        }
    }

private:
    static std::string current_time() {
        std::time_t t = std::time(nullptr);
        std::tm* tm = std::localtime(&t);
        char buffer[20];
        std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", tm);
        return std::string(buffer);
    }
};