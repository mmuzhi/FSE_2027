#include <string>
#include <optional>
#include <cctype>
#include <algorithm>

class PersonRequest {
public:
    std::optional<std::string> name;
    std::optional<std::string> sex;
    std::optional<std::string> phoneNumber;

    PersonRequest(const std::string& name, const std::string& sex, const std::string& phoneNumber)
        : name(validate_name(name)),
          sex(validate_sex(sex)),
          phoneNumber(validate_phoneNumber(phoneNumber))
    {}

private:
    static std::optional<std::string> validate_name(const std::string& name) {
        if (name.empty() || name.length() > 33) {
            return std::nullopt;
        }
        return name;
    }

    static std::optional<std::string> validate_sex(const std::string& sex) {
        if (sex != "Man" && sex != "Woman" && sex != "UGM") {
            return std::nullopt;
        }
        return sex;
    }

    static std::optional<std::string> validate_phoneNumber(const std::string& phoneNumber) {
        if (phoneNumber.empty() || phoneNumber.length() != 11) {
            return std::nullopt;
        }
        if (!std::all_of(phoneNumber.begin(), phoneNumber.end(), ::isdigit)) {
            return std::nullopt;
        }
        return phoneNumber;
    }
};