#include <cctype>
#include <initializer_list>
#include <optional>
#include <string>

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
    // If name is empty or exceeds 33 characters in length, result is "None" (nullopt).
    static std::optional<std::string> _validate_name(const std::string& name) {
        if (name.empty())
            return std::nullopt;
        if (name.length() > 33)
            return std::nullopt;
        return name;
    }

    // If sex is not "Man", "Woman", or "UGM", result is "None" (nullopt).
    static std::optional<std::string> _validate_sex(const std::string& sex) {
        for (const char* valid : {"Man", "Woman", "UGM"}) {
            if (sex == valid)
                return sex;
        }
        return std::nullopt;
    }

    // If phoneNumber is empty or not an 11 digit number, result is "None" (nullopt).
    static std::optional<std::string> _validate_phoneNumber(const std::string& phoneNumber) {
        if (phoneNumber.empty())
            return std::nullopt;
        if (phoneNumber.length() != 11 || !is_digits(phoneNumber))
            return std::nullopt;
        return phoneNumber;
    }

    static bool is_digits(const std::string& s) {
        for (unsigned char c : s) {
            if (!std::isdigit(c))
                return false;
        }
        return true;
    }
};