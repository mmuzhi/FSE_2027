#include <ctime>
#include <string>
#include <vector>

/**
 * # This is a class that serves as an email client, implementing functions
 * # such as checking emails, determining whether there is sufficient space,
 * # and cleaning up space
 */
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
    std::string addr;
    double capacity;
    std::vector<Email> inbox;

    /**
     * Initializes the EmailClient class with the email address and the
     * capacity of the email box.
     * :param addr: The email address, str.
     * :param capacity: The capacity of the email box, float.
     */
    EmailClient(const std::string& addr, double capacity)
        : addr(addr), capacity(capacity) {}

    /**
     * Sends an email to the given email address.
     * :param recv: The email address of the receiver, str.
     * :param content: The content of the email, str.
     * :param size: The size of the email, float.
     * :return: True if the email is sent successfully, False if the
     *          receiver's email box is full.
     */
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

    /**
     * Retrieves the first unread email in the email box and marks it as read.
     * :return: Pointer to the first unread email in the email box, or
     *          nullptr if none exists.
     */
    Email* fetch() {
        if (inbox.empty()) {
            return nullptr;
        }
        for (std::size_t i = 0; i < inbox.size(); ++i) {
            if (inbox[i].state == "unread") {
                inbox[i].state = "read";
                return &inbox[i];
            }
        }
        return nullptr;
    }

    /**
     * Determines whether the email box is full after adding an email of the
     * given size.
     * :param size: The size of the email, float.
     * :return: True if the email box is full, False otherwise.
     */
    bool is_full_with_one_more_email(double size) const {
        double occupied_size = get_occupied_size();
        return occupied_size + size > capacity;
    }

    /**
     * Gets the total size of the emails in the email box.
     * :return: The total size of the emails in the email box, float.
     */
    double get_occupied_size() const {
        double occupied_size = 0;
        for (const Email& email : inbox) {
            occupied_size += email.size;
        }
        return occupied_size;
    }

    /**
     * Clears the email box by deleting the oldest emails until the email box
     * has enough space to accommodate the given size.
     * :param size: The size of the email, float.
     */
    void clear_inbox(double size) {
        if (addr.empty()) {
            return;
        }
        double freed_space = 0;
        while (freed_space < size && !inbox.empty()) {
            Email email = inbox.front();
            freed_space += email.size;
            inbox.erase(inbox.begin());
        }
    }

private:
    static std::string current_timestamp() {
        std::time_t now = std::time(nullptr);
        std::tm* tm_info = std::localtime(&now);
        char buf[20];
        std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", tm_info);
        return std::string(buf);
    }
};