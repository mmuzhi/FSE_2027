#include <string>
#include <vector>
#include <cctype>

class EncryptionUtils {
public:
    explicit EncryptionUtils(const std::string& key) : key(key) {}

    std::string caesarCipher(const std::string& plaintext, int shift) {
        std::string ciphertext;
        for (char ch : plaintext) {
            if (std::isalpha(ch)) {
                int asciiOffset = std::isupper(ch) ? 'A' : 'a';
                char shiftedChar = static_cast<char>(
                    (static_cast<int>(ch) - asciiOffset + shift % 26 + 26) % 26 + asciiOffset);
                ciphertext += shiftedChar;
            } else {
                ciphertext += ch;
            }
        }
        return ciphertext;
    }

    std::string vigenereCipher(const std::string& plaintext) {
        std::string encryptedText;
        int keyIndex = 0;
        for (char ch : plaintext) {
            if (std::isalpha(ch)) {
                char keyChar = std::tolower(key[key[keyIndex % key.size()]]); // Ensure lowercase for shift calculation
                int shift = keyChar - 'a';
                char base = std::isupper(ch) ? 'A' : 'a';
                char shiftedChar = static_cast<char>(
                    (static_cast<int>(ch) - base + shift + 26) % 26 + base);
                encryptedText += shiftedChar;
                keyIndex++;
            } else {
                encryptedText += ch;
            }
        }
        return encryptedText;
    }

    std::string railFenceCipher(const std::string& plaintext, int rails) {
        if (rails <= 1 || plaintext.empty()) {
            return plaintext;
        }
        std::vector<std::vector<char>> fence(rails, std::vector<char>(plaintext.size(), '\0'));
        int direction = -1;
        int row = 0, col = 0;

        for (char ch : plaintext) {
            fence[row][col] = ch;
            col++;
            if (row == 0 || row == rails - 1) {
                direction *= -1;
            }
            row += direction;
        }

        std::string encryptedText;
        for (int i = 0; i < rails; i++) {
            for (int j = 0; j < plaintext.size(); j++) {
                if (fence[i][j] != '\0') {
                    encryptedText += fence[i][j];
                }
            }
        }
        return encryptedText;
    }

private:
    std::string key;
};