#include <string>
#include <unordered_map>
#include <vector>

class SignInSystem {
private:
    std::unordered_map<std::string, bool> users;

public:
    SignInSystem() = default;

    bool addUser(const std::string& username) {
        if (users.count(username)) {
            return false;
        } else {
            users[username] = false;
            return true;
        }
    }

    bool signIn(const std::string& username) {
        if (!users.count(username)) {
            return false;
        } else {
            users[username] = true;
            return true;
        }
    }

    bool checkSignIn(const std::string& username) {
        auto it = users.find(username);
        if (it == users.end()) {
            return false;
        } else {
            return it->second;
        }
    }

    bool allSignedIn() {
        for (const auto& pair : users) {
            if (!pair.second) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::string> allNotSignedIn() {
        std::vector<std::string> notSignedInUsers;
        for (const auto& entry : users) {
            if (!entry.second) {
                notSignedInUsers.push_back(entry.first);
            }
        }
        return notSignedInUsers;
    }
};