#include <string>
#include <vector>
#include <cctype>
#include <algorithm>
#include <cmath>

class EncryptionUtils {
private:
    std::string key;

public:
    EncryptionUtils(const std::string& key) : key(key) {}

    std::string caesarCipher(const std::string& plaintext, int shift) {
        std::string ciphertext;
        for (char c : plaintext) {
            if (std::isalpha(c)) {
                int asciiOffset = std::isupper(c) ? 'A' : 'a';
                char shiftedChar = static_cast<char>((c - asciiOffset + shift % 26 + 26) % 26 + asciiOffset);
                ciphertext += shiftedChar;
            } else {
                ciphertext += c;
            }
        }
        return ciphertext;
    }

    std::string vigenereCipher(const std::string& plainText) {
        std::string encryptedText;
        int keyIndex = 0;
        for (char c : plainText) {
            if (std::isalpha(c)) {
                char keyChar = key[keyIndex % key.length()];
                int shift = std::tolower(keyChar) - 'a';
                char lowerC = std::tolower(c);
                char encryptedChar = static_cast<char>((lowerC - 'a' + shift) % 26 + 'a');
                encryptedChar = std::isupper(c) ? std::toupper(encryptedChar) : encryptedChar;
                encryptedText += encryptedChar;
                keyIndex++;
            } else {
                encryptedText += c;
            }
        }
        return encryptedText;
    }

    std::string railFenceCipher(const std::string& plainText, int rails) {
        if (rails <= 0 || plainText.empty()) {
            return plainText;
        }

        // Create a 2D vector (fence) with rails rows and plainText.length() columns, initialize with '\n'
        std::vector<std::vector<char>> fence(rails, std::vector<char>(plainText.length(), '\n'));

        int direction = -1;
        int row = 0, col = 0;

        for (char c : plainText) {
            if (row == 0 || row == rails - 1) {
                direction = -direction;
            }

            fence[row][col] = c;
            col++;
            row += direction;
        }

        std::string encryptedText;
        for (int i = 0; i < rails; i++) {
            for (int j = 0; j < plainText.length(); j++) {
                if (fence[i][j] != '\n') {
                    encryptedText += fence[i][j];
                }
            }
        }

        return encryptedText;
    }
};