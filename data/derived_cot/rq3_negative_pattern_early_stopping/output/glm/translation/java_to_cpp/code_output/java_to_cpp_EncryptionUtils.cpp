#include <string>
#include <vector>
#include <cctype>

class EncryptionUtils {
private:
    std::string key;

public:
    EncryptionUtils(const std::string& key) : key(key) {}

    std::string caesarCipher(const std::string& plaintext, int shift) {
        std::string ciphertext;
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

    std::string vigenereCipher(const std::string& plainText) {
        std::string encryptedText;
        int keyIndex = 0;
        for (char c : plainText) {
            if (std::isalpha(static_cast<unsigned char>(c))) {
                int shift = std::tolower(static_cast<unsigned char>(key[keyIndex % key.length()])) - 'a';
                char encryptedChar = static_cast<char>((std::tolower(static_cast<unsigned char>(c)) - 'a' + shift) % 26 + 'a');
                encryptedText += std::isupper(static_cast<unsigned char>(c)) ? std::toupper(static_cast<unsigned char>(encryptedChar)) : encryptedChar;
                keyIndex++;
            } else {
                encryptedText += c;
            }
        }
        return encryptedText;
    }

    std::string railFenceCipher(const std::string& plainText, int rails) {
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
            for (int j = 0; j < static_cast<int>(plainText.length()); j++) {
                if (fence[i][j] != '\n') {
                    encryptedText += fence[i][j];
                }
            }
        }
        return encryptedText;
    }
};