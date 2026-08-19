#include <optional>
#include <regex>
#include <string>

class PersonRequest {
public:
    // Java's nullable String parameters map to std::optional<std::string>
    PersonRequest(const std::optional<std::string>& name,
                  const std::optional<std::string>& sex,
                  const std::optional<std::string>& phoneNumber)
        : name_(validateName(name)),
          sex_(validateSex(sex)),
          phoneNumber_(validatePhoneNumber(phoneNumber)) {}

    // Java getters may return null; optional preserves that contract
    std::optional<std::string> getName() const { return name_; }
    std::optional<std::string> getSex() const { return sex_; }
    std::optional<std::string> getPhoneNumber() const { return phoneNumber_; }

private:
    static std::optional<std::string> validateName(const std::optional<std::string>& name) {
        if (!name.has_value() || name->empty() || name->length() > 33) {
            return std::nullopt;
        }
        return name;
    }

    static std::optional<std::string> validateSex(const std::optional<std::string>& sex) {
        if (!sex.has_value() ||
            (*sex != "Man" && *sex != "Woman" && *sex != "UGM")) {
            return std::nullopt;
        }
        return sex;
    }

    static std::optional<std::string> validatePhoneNumber(const std::optional<std::string>& phoneNumber) {
        static const std::regex digits11("\\d{11}");
        if (!phoneNumber.has_value() || phoneNumber->empty() ||
            phoneNumber->length() != 11 ||
            !std::regex_match(*phoneNumber, digits11)) {
            return std::nullopt;
        }
        return phoneNumber;
    }

    std::optional<std::string> name_;
    std::optional<std::string> sex_;
    std::optional<std::string> phoneNumber_;
};