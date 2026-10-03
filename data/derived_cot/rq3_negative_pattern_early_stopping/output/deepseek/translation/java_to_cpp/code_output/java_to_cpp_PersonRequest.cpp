#include <optional>
#include <string>
#include <regex>

class PersonRequest {
private:
    std::optional<std::string> name_;
    std::optional<std::string> sex_;
    std::optional<std::string> phoneNumber_;

    static std::optional<std::string> validateName(const std::optional<std::string>& name) {
        if (!name.has_value() || name->empty() || name->length() > 33) {
            return std::nullopt;
        }
        return name;
    }

    static std::optional<std::string> validateSex(const std::optional<std::string>& sex) {
        if (!sex.has_value() || (*sex != "Man" && *sex != "Woman" && *sex != "UGM")) {
            return std::nullopt;
        }
        return sex;
    }

    static std::optional<std::string> validatePhoneNumber(const std::optional<std::string>& phoneNumber) {
        if (!phoneNumber.has_value() || phoneNumber->empty() || phoneNumber->length() != 11 ||
            !std::regex_match(*phoneNumber, std::regex("\\d{11}"))) {
            return std::nullopt;
        }
        return phoneNumber;
    }

public:
    PersonRequest(const std::optional<std::string>& name,
                  const std::optional<std::string>& sex,
                  const std::optional<std::string>& phoneNumber)
        : name_(validateName(name)), sex_(validateSex(sex)), phoneNumber_(validatePhoneNumber(phoneNumber)) {}

    std::optional<std::string> getName() const { return name_; }
    std::optional<std::string> getSex() const { return sex_; }
    std::optional<std::string> getPhoneNumber() const { return phoneNumber_; }
};