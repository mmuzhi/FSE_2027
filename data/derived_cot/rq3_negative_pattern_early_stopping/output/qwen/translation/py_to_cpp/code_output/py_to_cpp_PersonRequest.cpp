#include <string>
#include <set>
#include <cctype>

class PersonRequest {
private:
    std::string validateName(const std::string& name) const {
        if (name.empty() || name.size() > 33) {
            return "";
        }
        return name;
    }

    std::string validateSex(const std::string& sex) const {
        static const std::set<std::string> validSexes = {"Man", "Woman", "UGM"};
        if (validSexes.find(sex) == validSexes.end()) {
            return "";
        }
        return sex;
    }

    std::string validatePhoneNumber(const std::string& phoneNumber) const {
        if (phoneNumber.empty() || phoneNumber.size() != 11) {
            return "";
        }
        for (char c : phoneNumber) {
            if (!std::isdigit(static_cast<unsigned char>(c))) {
                return "";
            }
        }
        return phoneNumber;
    }

public:
    PersonRequest(const std::string& name, const std::string& sex, const std::string& phoneNumber) {
        name_ = validateName(name);
        sex_ = validateSex(sex);
        phoneNumber_ = validatePhoneNumber(phoneNumber);
    }

    // Public getters to mimic Python property access
    std::string getName() const { return name_; }
    std::string getSex() const { return sex_; }
    std::string getPhoneNumber() const { return phoneNumber_; }

private:
    std::string name_;
    std::string sex_;
    std::string phoneNumber_;
};