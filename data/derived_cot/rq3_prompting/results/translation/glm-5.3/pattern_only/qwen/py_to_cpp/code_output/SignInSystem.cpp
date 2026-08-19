#include <string>
#include <vector>
#include <utility>
#include <algorithm>

class SignInSystem {
private:
    // Preserves insertion order like a Python dict (matters for all_not_signed_in)
    std::vector<std::pair<std::string, bool>> users;

    std::vector<std::pair<std::string, bool>>::iterator find_user(const std::string& username) {
        for (auto it = users.begin(); it != users.end(); ++it) {
            if (it->first == username) {
                return it;
            }
        }
        return users.end();
    }

public:
    bool add_user(const std::string& username) {
        if (find_user(username) != users.end()) {
            return false;
        } else {
            users.emplace_back(username, false);
            return true;
        }
    }

    bool sign_in(const std::string& username) {
        auto it = find_user(username);
        if (it == users.end()) {
            return false;
        } else {
            it->second = true;
            return true;
        }
    }

    bool check_sign_in(const std::string& username) {
        auto it = find_user(username);
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
        // std::all_of returns true for empty range, matching Python's all() on empty dict
        return std::all_of(users.begin(), users.end(),
                           [](const std::pair<std::string, bool>& p) { return p.second; });
    }

    std::vector<std::string> all_not_signed_in() {
        std::vector<std::string> not_signed_in_users;
        for (const auto& entry : users) {
            if (!entry.second) {
                not_signed_in_users.push_back(entry.first);
            }
        }
        return not_signed_in_users;
    }
};