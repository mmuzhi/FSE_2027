#ifndef PERSON_REQUEST_H
#define PERSON_REQUEST_H

#include <string>
#include <optional>
#include <algorithm>
#include <cctype>

class PersonRequest {
private:
    std::optional<std::string> name;
    std::optional<std::string> sex;
    std::optional<std::string> phoneNumber;

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
            !std::all_of(phoneNumber->begin(), phoneNumber->end(),
                         [](unsigned char c) { return std::isdigit(c); })) {
            return std::nullopt;
        }
        return phoneNumber;
    }

public:
    PersonRequest(const std::optional<std::string>& name,
                  const std::optional<std::string>& sex,
                  const std::optional<std::string>& phoneNumber)
        : name(validateName(name)),
          sex(validateSex(sex)),
          phoneNumber(validatePhoneNumber(phoneNumber)) {}

    const std::optional<std::string>& getName() const {
        return name;
    }

    const std::optional<std::string>& getSex() const {
        return sex;
    }

    const std::optional<std::string>& getPhoneNumber() const {
        return phoneNumber;
    }
};

#endif