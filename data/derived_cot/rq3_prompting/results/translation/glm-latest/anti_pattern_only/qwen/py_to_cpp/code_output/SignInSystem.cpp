#include <algorithm>
#include <string>
#include <utility>
#include <vector>

class SignInSystem {
public:
    SignInSystem() = default;

    // Add a user to the sign-in system if the user wasn't already present.
    // The initial state is false.
    // Returns true if the user is added successfully, false if the user already exists.
    bool add_user(const std::string& username) {
        if (find_user(username) != users.end()) {
            return false;
        }
        users.emplace_back(username, false);
        return true;
    }

    // Sign in a user if the user exists, changing the state to true.
    // Returns true if the user is signed in successfully, false if the user does not exist.
    bool sign_in(const std::string& username) {
        auto it = find_user(username);
        if (it == users.end()) {
            return false;
        }
        it->second = true;
        return true;
    }

    // Check if a user is signed in.
    // Returns true if the user is signed in, false if the user does not exist or is not signed in.
    bool check_sign_in(const std::string& username) const {
        auto it = find_user(username);
        if (it == users.end()) {
            return false;
        }
        return it->second;
    }

    // Check if all users are signed in.
    // Returns true if all users are signed in (and true when there are no users,
    // matching Python's all() over an empty collection).
    bool all_signed_in() const {
        return std::all_of(users.begin(), users.end(),
                           [](const std::pair<std::string, bool>& entry) {
                               return entry.second;
                           });
    }

    // Get a list of usernames (in insertion order, matching Python dict semantics)
    // that are not signed in.
    std::vector<std::string> all_not_signed_in() const {
        std::vector<std::string> not_signed_in_users;
        for (const auto& entry : users) {
            if (!entry.second) {
                not_signed_in_users.push_back(entry.first);
            }
        }
        return not_signed_in_users;
    }

private:
    // Preserves insertion order, matching Python 3.7+ dict iteration order.
    std::vector<std::pair<std::string, bool>> users;

    std::vector<std::pair<std::string, bool>>::iterator find_user(const std::string& username) {
        return std::find_if(users.begin(), users.end(),
                            [&username](const std::pair<std::string, bool>& entry) {
                                return entry.first == username;
                            });
    }

    std::vector<std::pair<std::string, bool>>::const_iterator find_user(const std::string& username) const {
        return std::find_if(users.begin(), users.end(),
                            [&username](const std::pair<std::string, bool>& entry) {
                                return entry.first == username;
                            });
    }
};