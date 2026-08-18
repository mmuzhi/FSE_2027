#pragma once
#include <string>
#include <vector>
#include <unordered_map>

namespace org::example {

class SignInSystem {
private:
    std::unordered_map<std::string, bool> users;

public:
    SignInSystem() = default;

    bool addUser(const std::string& username) {
        if (users.count(username)) {
            return false;
        }
        users[username] = false;
        return true;
    }

    bool signIn(const std::string& username) {
        if (users.count(username) == 0) {
            return false;
        }
        users[username] = true;
        return true;
    }

    bool checkSignIn(const std::string& username) {
        auto it = users.find(username);
        if (it == users.end()) {
            return false;
        }
        return it->second;
    }

    bool allSignedIn() const {
        for (const auto& [key, signedIn] : users) {
            if (!signedIn) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::string> allNotSignedIn() const {
        std::vector<std::string> notSignedInUsers;
        for (const auto& [username, signedIn] : users) {
            if (!signedIn) {
                notSignedInUsers.push_back(username);
            }
        }
        return notSignedInUsers;
    }
};

} // namespace org::example