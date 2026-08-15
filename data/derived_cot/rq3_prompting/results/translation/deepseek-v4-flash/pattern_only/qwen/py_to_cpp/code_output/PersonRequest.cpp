#include <optional>
#include <string>
#include <cctype>

class PersonRequest {
public:
    std::optional<std::string> name;
    std::optional<std::string> sex;
    std::optional<std::string> phoneNumber;

    PersonRequest(const std::string& name, const std::string& sex, const std::string& phoneNumber)
        : name(validateName(name)), sex(validateSex(sex)), phoneNumber(validatePhoneNumber(phoneNumber)) {}

private:
    static std::size_t utf8Length(const std::string& s) {
        std::size_t count = 0;
        std::size_t i = 0;
        while (i < s.size()) {
            unsigned char c = static_cast<unsigned char>(s[i]);
            if (c < 0x80) {
                i += 1;
            } else if ((c & 0xE0) == 0xC0) {
                i += 2;
            } else if ((c & 0xF0) == 0xE0) {
                i += 3;
            } else if ((c & 0xF8) == 0xF0) {
                i += 4;
            } else {
                i += 1;
            }
            ++count;
        }
        return count;
    }

    static std::optional<std::string> validateName(const std::string& name) {
        if (name.empty()) return std::nullopt;
        if (utf8Length(name) > 33) return std::nullopt;
        return name;
    }

    static std::optional<std::string> validateSex(const std::string& sex) {
        if (sex != "Man" && sex != "Woman" && sex != "UGM") return std::nullopt;
        return sex;
    }

    static std::optional<std::string> validatePhoneNumber(const std::string& phoneNumber) {
        if (phoneNumber.empty()) return std::nullopt;
        if (utf8Length(phoneNumber) != 11) return std::nullopt;
        for (char c : phoneNumber) {
            if (!std::isdigit(static_cast<unsigned char>(c))) return std::nullopt;
        }
        return phoneNumber;
    }
};