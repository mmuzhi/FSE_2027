#include <string>
#include <optional>

struct PersonRequest {
    std::optional<std::string> name;
    std::optional<std::string> sex;
    std::optional<std::string> phoneNumber;

    PersonRequest(std::string name, std::string sex, std::string phoneNumber) {
        name = validateName(name);
        sex = validateSex(sex);
        phoneNumber = validatePhoneNumber(phoneNumber);
    }

    static std::optional<std::string> validateName(std::string name) {
        if (name.empty() || name.length() > 33) {
            return std::nullopt;
        }
        return name;
    }

    static std::optional<std::string> validateSex(std::string sex) {
        if (sex.empty() || 
            sex != "Man" && sex != "Woman" && sex != "UGM") {
            return std::nullopt;
        }
        return sex;
    }

    static std::optional<std::string> validatePhoneNumber(std::string phoneNumber) {
        if (phoneNumber.empty() || phoneNumber.length() != 11 || 
            !std::regex_match(phoneNumber, std::regex("\\d{11}"))) {
            return std::nullopt;
        }
        return phoneNumber;
    }

    // Getters
    std::string getName() const {
        if (!name) {
            return ""; // In Java, it would be null, but in C++ we return empty string to mimic null behavior?
        }
        return *name;
    }

    std::string getSex() const {
        if (!sex) {
            return "";
        }
        return *sex;
    }

    std::string getPhoneNumber() const {
        if (!phoneNumber) {
            return "";
        }
        return *phoneNumber;
    }
};