#include <string>
#include <vector>
#include <utility>
#include <algorithm>

class SignInSystem {
private:
    // Preserves Python dict insertion order (relevant for all_not_signed_in output order)
    std::vector<std::pair<std::string, bool>> users;

    std::vector<std::pair<std::string, bool>>::iterator find_user(const std::string& username) {
        return std::find_if(users.begin(), users.end(),
                            [&username](const std::pair<std::string, bool>& p) {
                                return p.first == username;
                            });
    }

public:
    SignInSystem() = default;

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
        // std::all_of over an empty range returns true, matching Python's all([])
        return std::all_of(users.begin(), users.end(),
                           [](const std::pair<std::string, bool>& p) {
                               return p.second;
                           });
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