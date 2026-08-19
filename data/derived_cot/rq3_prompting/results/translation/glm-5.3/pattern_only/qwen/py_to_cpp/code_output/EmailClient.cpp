#include <ctime>
#include <iomanip>
#include <map>
#include <sstream>
#include <string>
#include <variant>
#include <vector>

// An email is represented as a dict-like map with string or numeric values.
using Email = std::map<std::string, std::variant<std::string, double>>;

class EmailClient {
public:
    std::string addr;
    double capacity;
    std::vector<Email> inbox;

    // Initializes the EmailClient with the email address and the capacity of the email box.
    EmailClient(const std::string& addr, double capacity)
        : addr(addr), capacity(capacity), inbox() {}

    // Sends an email to the given EmailClient.
    // Returns true if sent, false if the receiver's email box is full
    // (in which case the *sender's* own inbox is cleared, mirroring the original logic).
    bool send_to(EmailClient& recv, const std::string& content, double size) {
        if (!recv.is_full_with_one_more_email(size)) {
            std::string timestamp = now_timestamp();
            Email email;
            email["sender"] = addr;
            email["receiver"] = recv.addr;
            email["content"] = content;
            email["size"] = size;
            email["time"] = timestamp;
            email["state"] = std::string("unread");
            recv.inbox.push_back(std::move(email));
            return true;
        } else {
            this->clear_inbox(size);
            return false;
        }
    }

    // Retrieves the first unread email in the email box and marks it as read.
    // Returns a pointer to the email (reference semantics like Python),
    // or nullptr if there is none.
    Email* fetch() {
        if (inbox.empty()) {
            return nullptr;
        }
        for (std::size_t i = 0; i < inbox.size(); ++i) {
            if (std::get<std::string>(inbox[i]["state"]) == "unread") {
                inbox[i]["state"] = std::string("read");
                return &inbox[i];
            }
        }
        return nullptr;
    }

    // Determines whether the email box is full after adding an email of the given size.
    bool is_full_with_one_more_email(double size) {
        double occupied_size = get_occupied_size();
        return occupied_size + size > capacity ? true : false;
    }

    // Gets the total size of the emails in the email box.
    double get_occupied_size() {
        double occupied_size = 0;
        for (const Email& email : inbox) {
            occupied_size += std::get<double>(email.at("size"));
        }
        return occupied_size;
    }

    // Clears the email box by deleting the oldest emails until enough space
    // for the given size is freed (no-op if addr is empty).
    void clear_inbox(double size) {
        if (addr.empty()) {
            return;
        }
        double freed_space = 0;
        while (freed_space < size && !inbox.empty()) {
            freed_space += std::get<double>(inbox[0].at("size"));
            inbox.erase(inbox.begin());
        }
    }

private:
    // Equivalent of datetime.now().strftime("%Y-%m-%d %H:%M:%S") (local time).
    static std::string now_timestamp() {
        std::time_t now = std::time(nullptr);
        std::tm tm_buf{};
#ifdef _MSC_VER
        localtime_s(&tm_buf, &now);
        std::tm* tm_ptr = &tm_buf;
#else
        std::tm* tm_ptr = localtime_r(&now, &tm_buf);
#endif
        std::ostringstream oss;
        oss << std::put_time(tm_ptr, "%Y-%m-%d %H:%M:%S");
        return oss.str();
    }
};