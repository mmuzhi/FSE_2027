#include <string>
#include <optional>
#include <algorithm>
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
    std::optional<std::string> _validate_name(const std::string& name) {
        if (name.empty()) {
            return std::nullopt;
        }
        if (name.length() > 33) {
            return std::nullopt;
        }
        return name;
    }

    std::optional<std::string> _validate_sex(const std::string& sex) {
        if (sex != "Man" && sex != "Woman" && sex != "UGM") {
            return std::nullopt;
        }
        return sex;
    }

    std::optional<std::string> _validate_phoneNumber(const std::string& phoneNumber) {
        if (phoneNumber.empty()) {
            return std::nullopt;
        }
        if (phoneNumber.length() != 11 || 
            !std::all_of(phoneNumber.begin(), phoneNumber.end(), 
                         [](unsigned char c) { return std::isdigit(c); })) {
            return std::nullopt;
        }
        return phoneNumber;
    }
};