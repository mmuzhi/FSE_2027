#include <optional>
#include <string>
#include <cctype>
#include <algorithm>

namespace org {
namespace example {

class PersonRequest {
private:
    std::optional<std::string> name;
    std::optional<std::string> sex;
    std::optional<std::string> phoneNumber;

    static std::optional<std::string> validateName(const std::optional<std::string>& name) {
        if (!name.has_value()) {
            return std::nullopt;
        }
        const std::string& s = *name;
        if (s.empty() || s.length() > 33) {
            return std::nullopt;
        }
        return s;
    }

    static std::optional<std::string> validateSex(const std::optional<std::string>& sex) {
        if (!sex.has_value()) {
            return std::nullopt;
        }
        const std::string& s = *sex;
        if (s != "Man" && s != "Woman" && s != "UGM") {
            return std::nullopt;
        }
        return s;
    }

    static std::optional<std::string> validatePhoneNumber(const std::optional<std::string>& phoneNumber) {
        if (!phoneNumber.has_value()) {
            return std::nullopt;
        }
        const std::string& s = *phoneNumber;
        if (s.empty() || s.length() != 11 ||
            !std::all_of(s.begin(), s.end(), [](unsigned char c) { return std::isdigit(c); })) {
            return std::nullopt;
        }
        return s;
    }

public:
    PersonRequest(std::optional<std::string> name,
                  std::optional<std::string> sex,
                  std::optional<std::string> phoneNumber) {
        this->name = validateName(name);
        this->sex = validateSex(sex);
        this->phoneNumber = validatePhoneNumber(phoneNumber);
    }

    std::optional<std::string> getName() const { return name; }
    std::optional<std::string> getSex() const { return sex; }
    std::optional<std::string> getPhoneNumber() const { return phoneNumber; }
};

} // namespace example
} // namespace org