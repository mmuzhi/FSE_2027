#include <string>
#include <optional>
#include <cctype>

class PersonRequest {
public:
    std::optional<std::string> name;
    std::optional<std::string> sex;
    std::optional<std::string> phoneNumber;

    PersonRequest(const std::string& name, const std::string& sex, const std::string& phoneNumber)
        : name(_validate_name(name)),
          sex(_validate_sex(sex)),
          phoneNumber(_validate_phoneNumber(phoneNumber)) {}

private:
    // If name is empty or exceeds 33 characters in length, set to nullopt.
    static std::optional<std::string> _validate_name(const std::string& name) {
        if (name.empty()) {
            return std::nullopt;
        }
        if (name.size() > 33) {
            return std::nullopt;
        }
        return name;
    }

    // If sex is not Man, Woman, or UGM, set to nullopt.
    static std::optional<std::string> _validate_sex(const std::string& sex) {
        if (sex != "Man" && sex != "Woman" && sex != "UGM") {
            return std::nullopt;
        }
        return sex;
    }

    // If phoneNumber is empty or not an 11 digit number, set to nullopt.
    static std::optional<std::string> _validate_phoneNumber(const std::string& phoneNumber) {
        if (phoneNumber.empty()) {
            return std::nullopt;
        }
        if (phoneNumber.size() != 11) {
            return std::nullopt;
        }
        for (char c : phoneNumber) {
            if (!std::isdigit(static_cast<unsigned char>(c))) {
                return std::nullopt;
            }
        }
        return phoneNumber;
    }
};