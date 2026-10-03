#include <string>
#include <unordered_map>
#include <vector>

class SignInSystem {
private:
    std::unordered_map<std::string, bool> users;

public:
    SignInSystem() : users() {}

    bool add_user(const std::string& username) {
        if (users.find(username) != users.end()) {
            return false;
        } else {
            users[username] = false;
            return true;
        }
    }

    bool sign_in(const std::string& username) {
        auto it = users.find(username);
        if (it == users.end()) {
            return false;
        } else {
            it->second = true;
            return true;
        }
    }

    bool check_sign_in(const std::string& username) {
        auto it = users.find(username);
        if (it == users.end()) {
            return false;
        } else {
            if (it->second) {
                return true;
            } else {
                return false;
            }
        }
    }

    bool all_signed_in() {
        // Python's all([]) returns True, so empty map returns True
        for (const auto& pair : users) {
            if (!pair.second) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::string> all_not_signed_in() {
        std::vector<std::string> not_signed_in_users;
        for (const auto& pair : users) {
            if (!pair.second) {
                not_signed_in_users.push_back(pair.first);
            }
        }
        return not_signed_in_users;
    }
};