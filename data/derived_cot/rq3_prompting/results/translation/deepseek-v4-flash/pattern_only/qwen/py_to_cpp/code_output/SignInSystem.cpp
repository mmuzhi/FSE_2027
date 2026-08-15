#include <string>
#include <vector>
#include <utility>

class SignInSystem {
private:
    std::vector<std::pair<std::string, bool>> users;

public:
    SignInSystem() {}

    bool add_user(const std::string& username) {
        for (const auto& user : users) {
            if (user.first == username) {
                return false;
            }
        }
        users.push_back({username, false});
        return true;
    }

    bool sign_in(const std::string& username) {
        for (auto& user : users) {
            if (user.first == username) {
                user.second = true;
                return true;
            }
        }
        return false;
    }

    bool check_sign_in(const std::string& username) const {
        for (const auto& user : users) {
            if (user.first == username) {
                return user.second;
            }
        }
        return false;
    }

    bool all_signed_in() const {
        for (const auto& user : users) {
            if (!user.second) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::string> all_not_signed_in() const {
        std::vector<std::string> result;
        for (const auto& user : users) {
            if (!user.second) {
                result.push_back(user.first);
            }
        }
        return result;
    }
};