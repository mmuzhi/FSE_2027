#pragma once

#include <cctype>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class DecryptionUtils {
private:
    std::string key;

public:
    explicit DecryptionUtils(std::string key) : key(std::move(key)) {}

    std::string caesarDecipher(const std::string& ciphertext, int shift) const {
        std::string plaintext;
        shift = shift % 26;
        for (char ch : ciphertext) {
            if (std::isalpha(static_cast<unsigned char>(ch))) {
                int asciiOffset = std::isupper(static_cast<unsigned char>(ch)) ? 'A' : 'a';
                char shiftedChar = static_cast<char>((ch - asciiOffset - shift + 26) % 26 + asciiOffset);
                plaintext.push_back(shiftedChar);
            }
            else {
                plaintext.push_back(ch);
            }
        }
        return plaintext;
    }

    std::string vigenereDecipher(const std::string& ciphertext) const {
        std::string decryptedText;
        int keyIndex = 0;
        for (char ch : ciphertext) {
            if (std::isalpha(static_cast<unsigned char>(ch))) {
                if (key.empty()) {
                    // Java: ArithmeticException on `keyIndex % key.length()` with an empty key
                    throw std::runtime_error("/ by zero");
                }
                int shift = std::tolower(static_cast<unsigned char>(key.at(keyIndex % key.length()))) - 'a';
                char base = std::isupper(static_cast<unsigned char>(ch)) ? 'A' : 'a';
                char decryptedChar = static_cast<char>((ch - base - shift + 26) % 26 + base);
                decryptedText.push_back(decryptedChar);
                keyIndex++;
            }
            else {
                decryptedText.push_back(ch);
            }
        }
        return decryptedText;
    }

    std::string railFenceDecipher(const std::string& encryptedText, int rails) const {
        if (rails < 0) {
            // Java: NegativeArraySizeException from `new char[rails][...]`
            throw std::length_error("rails < 0");
        }
        const std::size_t len = encryptedText.length();
        std::vector<std::vector<char>> fence(rails, std::vector<char>(len, '\0'));

        int direction = -1;
        int row = 0, col = 0;

        for (std::size_t i = 0; i < len; i++) {
            if (row == 0 || row == rails - 1) {
                direction = -direction;
            }
            fence.at(row).at(col++) = '*';
            row += direction;
        }

        int index = 0;
        for (int i = 0; i < rails; i++) {
            for (std::size_t j = 0; j < len; j++) {
                if (fence.at(i).at(j) == '*') {
                    fence.at(i).at(j) = encryptedText.at(index++);
                }
            }
        }

        std::string plainText;
        direction = -1;
        row = 0;
        col = 0;

        for (std::size_t i = 0; i < len; i++) {
            if (row == 0 || row == rails - 1) {
                direction = -direction;
            }
            plainText.push_back(fence.at(row).at(col++));
            row += direction;
        }

        return plainText;
    }
};