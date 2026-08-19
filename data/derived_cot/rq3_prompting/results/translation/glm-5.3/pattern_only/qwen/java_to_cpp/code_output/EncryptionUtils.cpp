#ifndef ORG_EXAMPLE_ENCRYPTIONUTILS_HPP
#define ORG_EXAMPLE_ENCRYPTIONUTILS_HPP

#include <cctype>
#include <string>
#include <utility>
#include <vector>

namespace org::example {

class EncryptionUtils {
private:
    std::string key;

public:
    explicit EncryptionUtils(std::string key)
        : key(std::move(key)) {}

    std::string caesarCipher(const std::string& plaintext, int shift) {
        std::string ciphertext;
        for (char c : plaintext) {
            if (std::isalpha(static_cast<unsigned char>(c))) {
                int asciiOffset = std::isupper(static_cast<unsigned char>(c)) ? 'A' : 'a';
                // Java % truncates toward zero; C++ % does too, so negative shifts match.
                char shiftedChar = static_cast<char>((c - asciiOffset + shift) % 26 + asciiOffset);
                ciphertext += shiftedChar;
            }
            else {
                ciphertext += c;
            }
        }
        return ciphertext;
    }

    std::string vigenereCipher(const std::string& plainText) {
        std::string encryptedText;
        std::size_t keyIndex = 0;
        for (char c : plainText) {
            if (std::isalpha(static_cast<unsigned char>(c))) {
                // Matches Java ArithmeticException on empty key only loosely
                // (C++ makes x % 0 UB); assume non-empty key as in Java usage.
                int shift = std::tolower(static_cast<unsigned char>(key.at(keyIndex % key.length()))) - 'a';
                char encryptedChar = static_cast<char>(
                    (std::tolower(static_cast<unsigned char>(c)) - 'a' + shift) % 26 + 'a');
                encryptedText += std::isupper(static_cast<unsigned char>(c))
                                     ? static_cast<char>(std::toupper(static_cast<unsigned char>(encryptedChar)))
                                     : encryptedChar;
                keyIndex++;
            }
            else {
                encryptedText += c;
            }
        }
        return encryptedText;
    }

    std::string railFenceCipher(const std::string& plainText, int rails) {
        // .at() preserves Java's ArrayIndexOutOfBoundsException on bad indices (e.g. rails == 1).
        std::vector<std::vector<char>> fence(
            static_cast<std::size_t>(rails),
            std::vector<char>(plainText.length(), '\n'));

        int direction = -1;
        std::size_t row = 0, col = 0;

        for (char c : plainText) {
            if (row == 0 || row == static_cast<std::size_t>(rails) - 1) {
                direction = -direction;
            }

            fence.at(row).at(col) = c;
            col++;
            row += static_cast<std::size_t>(direction);
        }

        std::string encryptedText;
        for (int i = 0; i < rails; i++) {
            for (std::size_t j = 0; j < plainText.length(); j++) {
                if (fence.at(static_cast<std::size_t>(i)).at(j) != '\n') {
                    encryptedText += fence.at(static_cast<std::size_t>(i)).at(j);
                }
            }
        }
        return encryptedText;
    }
};

} // namespace org::example

#endif // ORG_EXAMPLE_ENCRYPTIONUTILS_HPP