#include <cstddef>
#include <ctime>
#include <string>
#include <vector>

// This is a class that serves as an email client, implementing functions
// such as checking emails, determining whether there is sufficient space,
// and cleaning up space.

// Represents an email (the dict entries used by the Python implementation).
struct Email {
    std::string sender;
    std::string receiver;
    std::string content;
    double size = 0.0;
    std::string time;
    std::string state;
};

class EmailClient {
public:
    std::string addr;          // The email address.
    double capacity;           // The capacity of the email box.
    std::vector<Email> inbox;

    // Initializes the EmailClient class with the email address and the
    // capacity of the email box.
    EmailClient(const std::string& addr, double capacity)
        : addr(addr), capacity(capacity) {}

    // Sends an email to the given email client.
    // Returns true if the email is sent successfully, false if the
    // receiver's email box is full (in which case the sender's own inbox
    // is cleared, mirroring the original behavior).
    bool send_to(EmailClient& recv, const std::string& content, double size) {
        if (!recv.is_full_with_one_more_email(size)) {
            std::string timestamp = current_timestamp();
            Email email;
            email.sender = this->addr;
            email.receiver = recv.addr;
            email.content = content;
            email.size = size;
            email.time = timestamp;
            email.state = "unread";
            recv.inbox.push_back(email);
            return true;
        } else {
            this->clear_inbox(size);
            return false;
        }
    }

    // Retrieves the first unread email in the email box and marks it as read.
    // Returns nullptr (Python's None) if the inbox is empty or no unread
    // email exists. The result points at the email stored inside the inbox,
    // mirroring the Python behavior of returning the dict itself.
    Email* fetch() {
        if (inbox.empty()) {
            return nullptr;
        }
        for (Email& email : inbox) {
            if (email.state == "unread") {
                email.state = "read";
                return &email;
            }
        }
        return nullptr;
    }

    // Determines whether the email box is full after adding an email of the
    // given size.
    bool is_full_with_one_more_email(double size) const {
        double occupied_size = get_occupied_size();
        return occupied_size + size > capacity;
    }

    // Gets the total size of the emails in the email box.
    double get_occupied_size() const {
        double occupied_size = 0.0;
        for (const Email& email : inbox) {
            occupied_size += email.size;
        }
        return occupied_size;
    }

    // Clears the email box by deleting the oldest emails until enough space
    // has been freed for the given size (or the inbox becomes empty).
    // Note: does nothing when this client's address is empty, matching the
    // original implementation's early return.
    void clear_inbox(double size) {
        if (addr.empty()) {
            return;
        }
        double freed_space = 0.0;
        while (freed_space < size && !inbox.empty()) {
            freed_space += inbox.front().size;
            inbox.erase(inbox.begin());  // del self.inbox[0]
        }
    }

private:
    // Equivalent of datetime.now().strftime("%Y-%m-%d %H:%M:%S") (local time).
    static std::string current_timestamp() {
        std::time_t now = std::time(nullptr);
        std::tm* tm_buf = std::localtime(&now);
        char buffer[32];
        if (tm_buf != nullptr &&
            std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", tm_buf) != 0) {
            return std::string(buffer);
        }
        return std::string();
    }
};