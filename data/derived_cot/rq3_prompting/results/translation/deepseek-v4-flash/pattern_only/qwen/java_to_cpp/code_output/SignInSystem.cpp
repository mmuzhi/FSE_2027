#include <string>
#include <unordered_map>
#include <vector>

class SignInSystem {
private:
    std::unordered_map<std::string, bool> users;

public:
    SignInSystem() {}

    bool addUser(const std::string& username) {
        if (users.find(username) != users.end()) {
            return false;
        }
        users[username] = false;
        return true;
    }

    bool signIn(const std::string& username) {
        auto it = users.find(username);
        if (it == users.end()) {
            return false;
        }
        it->second = true;
        return true;
    }

    bool checkSignIn(const std::string& username) const {
        auto it = users.find(username);
        if (it == users.end()) {
            return false;
        }
        return it->second;
    }

    bool allSignedIn() const {
        for (const auto& entry : users) {
            if (!entry.second) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::string> allNotSignedIn() const {
        std::vector<std::string> notSignedInUsers;
        for (const auto& entry : users) {
            if (!entry.second) {
                notSignedInUsers.push_back(entry.first);
            }
        }
        return notSignedInUsers;
    }
};