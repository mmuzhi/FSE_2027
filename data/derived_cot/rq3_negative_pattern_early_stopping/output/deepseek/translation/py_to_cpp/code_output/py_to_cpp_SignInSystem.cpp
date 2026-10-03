#include <unordered_map>
#include <string>
#include <vector>
#include <algorithm>

class SignInSystem {
private:
    std::unordered_map<std::string, bool> users;

public:
    bool add_user(const std::string& username) {
        if (users.find(username) != users.end()) {
            return false;
        }
        users[username] = false;
        return true;
    }

    bool sign_in(const std::string& username) {
        auto it = users.find(username);
        if (it == users.end()) {
            return false;
        }
        it->second = true;
        return true;
    }

    bool check_sign_in(const std::string& username) {
        auto it = users.find(username);
        if (it == users.end()) {
            return false;
        }
        return it->second;
    }

    bool all_signed_in() {
        return std::all_of(users.begin(), users.end(),
            [](const auto& pair) { return pair.second; });
    }

    std::vector<std::string> all_not_signed_in() {
        std::vector<std::string> result;
        for (const auto& pair : users) {
            if (!pair.second) {
                result.push_back(pair.first);
            }
        }
        return result;
    }
};