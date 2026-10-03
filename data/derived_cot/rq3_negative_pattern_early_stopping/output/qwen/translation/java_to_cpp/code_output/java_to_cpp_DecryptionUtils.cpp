#include <string>
#include <vector>
#include <cctype>
#include <cmath>

class DecryptionUtils {
private:
    std::string key;

public:
    DecryptionUtils(const std::string& key) : key(key) {}

    std::string caesarDecipher(const std::string& ciphertext, int shift) {
        std::string plaintext;
        int normalized_shift = shift % 26;
        if (normalized_shift < 0) {
            normalized_shift += 26;
        }
        for (char ch : ciphertext) {
            if (std::isalpha(ch)) {
                bool is_upper = std::isupper(ch);
                char base = is_upper ? 'A' : 'a';
                char shifted_char = static_cast<char>((ch - base - normalized_shift + 26) % 26 + base);
                plaintext += shifted_char;
            } else {
                plaintext += ch;
            }
        }
        return plaintext;
    }

    std::string vigenereDecipher(const std::string& ciphertext) {
        std::string decryptedText;
        int keyIndex = 0;
        for (char ch : ciphertext) {
            if (std::isalpha(ch)) {
                char keyChar = std::tolower(key[keyIndex % key.length()]);
                int shift = keyChar - 'a';
                bool is_upper = std::isupper(ch);
                char base = is_upper ? 'A' : 'a';
                char decryptedChar = static_cast<char>((ch - base - shift + 26) % 26 + base);
                decryptedText += decryptedChar;
                keyIndex++;
            } else {
                decryptedText += ch;
            }
        }
        return decryptedText;
    }

    std::string railFenceDecipher(const std::string& encryptedText, int rails) {
        if (rails <= 0 || encryptedText.empty()) {
            return encryptedText;
        }

        int len = encryptedText.length();
        std::vector<std::vector<char>> fence(rails, std::vector<char>(len, '\0'));
        std::vector<int> direction(rails, 1);
        int row = 0;

        for (int i = 0; i < len; ++i) {
            fence[row][i] = '*';
            if (row == 0 || row == rails - 1) {
                std::reverse(direction.begin(), direction.end());
            }
            row += direction[row];
        }

        int index = 0;
        for (int i = 0; i < rails; ++i) {
            for (int j = 0; j < len; ++j) {
                if (fence[i][j] == '*') {
                    fence[i][j] = encryptedText[index++];
                }
            }
        }

        index = 0;
        row = 0;
        for (int i = 0; i < len; ++i) {
            decryptedText += fence[row][index++];
            if (row == 0 || row == rails - 1) {
                std::reverse(direction.begin(), direction.end());
            }
            row += direction[row];
        }
        return decryptedText;
    }
};