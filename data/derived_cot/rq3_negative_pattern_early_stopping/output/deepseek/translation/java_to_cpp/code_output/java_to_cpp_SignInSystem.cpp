#include <string>
#include <unordered_map>
#include <vector>

class SignInSystem {
private:
    std::unordered_map<std::string, bool> users;

public:
    SignInSystem() : users() {}

    bool addUser(const std::string& username) {
        if (users.find(username) != users.end()) {
            return false;
        } else {
            users[username] = false;
            return true;
        }
    }

    bool signIn(const std::string& username) {
        auto it = users.find(username);
        if (it == users.end()) {
            return false;
        } else {
            it->second = true;
            return true;
        }
    }

    bool checkSignIn(const std::string& username) const {
        auto it = users.find(username);
        if (it == users.end()) {
            return false;
        } else {
            return it->second;
        }
    }

    bool allSignedIn() const {
        for (const auto& pair : users) {
            if (!pair.second) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::string> allNotSignedIn() const {
        std::vector<std::string> result;
        for (const auto& pair : users) {
            if (!pair.second) {
                result.push_back(pair.first);
            }
        }
        return result;
    }
};