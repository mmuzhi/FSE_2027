#include <string>
#include <vector>
#include <cctype>

class DecryptionUtils {
private:
    std::string key;

public:
    DecryptionUtils(const std::string& key) : key(key) {}

    std::string caesarDecipher(const std::string& ciphertext, int shift) {
        std::string plaintext;
        shift = shift % 26;
        for (char ch : ciphertext) {
            if (std::isalpha(static_cast<unsigned char>(ch))) {
                int asciiOffset = std::isupper(static_cast<unsigned char>(ch)) ? 'A' : 'a';
                char shiftedChar = static_cast<char>((ch - asciiOffset - shift + 26) % 26 + asciiOffset);
                plaintext.push_back(shiftedChar);
            } else {
                plaintext.push_back(ch);
            }
        }
        return plaintext;
    }

    std::string vigenereDecipher(const std::string& ciphertext) {
        std::string decryptedText;
        int keyIndex = 0;
        for (char ch : ciphertext) {
            if (std::isalpha(static_cast<unsigned char>(ch))) {
                int shift = std::tolower(static_cast<unsigned char>(key[keyIndex % key.length()])) - 'a';
                char base = std::isupper(static_cast<unsigned char>(ch)) ? 'A' : 'a';
                char decryptedChar = static_cast<char>((ch - base - shift + 26) % 26 + base);
                decryptedText.push_back(decryptedChar);
                keyIndex++;
            } else {
                decryptedText.push_back(ch);
            }
        }
        return decryptedText;
    }

    std::string railFenceDecipher(const std::string& encryptedText, int rails) {
        std::vector<std::vector<char>> fence(rails, std::vector<char>(encryptedText.length(), '\0'));

        int direction = -1;
        int row = 0, col = 0;

        for (size_t i = 0; i < encryptedText.length(); ++i) {
            if (row == 0 || row == rails - 1) {
                direction = -direction;
            }
            fence[row][col++] = '*';
            row += direction;
        }

        int index = 0;
        for (int i = 0; i < rails; ++i) {
            for (size_t j = 0; j < encryptedText.length(); ++j) {
                if (fence[i][j] == '*') {
                    fence[i][j] = encryptedText[index++];
                }
            }
        }

        std::string plainText;
        direction = -1;
        row = 0;
        col = 0;

        for (size_t i = 0; i < encryptedText.length(); ++i) {
            if (row == 0 || row == rails - 1) {
                direction = -direction;
            }
            plainText.push_back(fence[row][col++]);
            row += direction;
        }

        return plainText;
    }
};