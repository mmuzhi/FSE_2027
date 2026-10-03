#include <string>
#include <vector>
#include <cctype>
#include <stdexcept>
#include <algorithm>

class EncryptionUtils {
private:
    std::string key;

public:
    EncryptionUtils(const std::string& key) : key(key) {}

    std::string caesarCipher(const std::string& plaintext, int shift) const {
        std::string ciphertext;
        ciphertext.reserve(plaintext.size());
        for (char c : plaintext) {
            if (std::isalpha(static_cast<unsigned char>(c))) {
                int asciiOffset = std::isupper(static_cast<unsigned char>(c)) ? 'A' : 'a';
                char shiftedChar = static_cast<char>((c - asciiOffset + shift) % 26 + asciiOffset);
                ciphertext += shiftedChar;
            } else {
                ciphertext += c;
            }
        }
        return ciphertext;
    }

    std::string vigenereCipher(const std::string& plainText) const {
        if (key.empty()) {
            throw std::invalid_argument("Key must not be empty (division by zero)");
        }
        std::string encryptedText;
        encryptedText.reserve(plainText.size());
        int keyIndex = 0;
        for (char c : plainText) {
            if (std::isalpha(static_cast<unsigned char>(c))) {
                int shift = std::tolower(static_cast<unsigned char>(key[keyIndex % key.size()])) - 'a';
                char encryptedChar = static_cast<char>((std::tolower(static_cast<unsigned char>(c)) - 'a' + shift) % 26 + 'a');
                if (std::isupper(static_cast<unsigned char>(c))) {
                    encryptedText += static_cast<char>(std::toupper(static_cast<unsigned char>(encryptedChar)));
                } else {
                    encryptedText += encryptedChar;
                }
                keyIndex++;
            } else {
                encryptedText += c;
            }
        }
        return encryptedText;
    }

    std::string railFenceCipher(const std::string& plainText, int rails) const {
        // Use .at() for bounds checking to replicate Java's ArrayIndexOutOfBoundsException
        std::vector<std::vector<char>> fence(rails, std::vector<char>(plainText.length(), '\n'));

        int direction = -1;
        int row = 0, col = 0;

        for (char c : plainText) {
            if (row == 0 || row == rails - 1) {
                direction = -direction;
            }
            fence.at(row).at(col) = c;
            col++;
            row += direction;
        }

        std::string encryptedText;
        encryptedText.reserve(plainText.size());
        for (int i = 0; i < rails; ++i) {
            for (int j = 0; j < static_cast<int>(plainText.length()); ++j) {
                if (fence.at(i).at(j) != '\n') {
                    encryptedText += fence.at(i).at(j);
                }
            }
        }
        return encryptedText;
    }
};