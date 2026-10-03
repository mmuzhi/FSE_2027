#include <string>
#include <vector>
#include <cctype>
#include <algorithm>
#include <iostream>

class DecryptionUtils {
private:
    std::string key;

public:
    explicit DecryptionUtils(const std::string& key) : key(key) {}

    std::string caesar_decipher(const std::string& ciphertext, int shift) {
        std::string plaintext;
        for (char c : ciphertext) {
            if (std::isalpha(c)) {
                int base = std::isupper(c) ? 'A' : 'a';
                char shifted_char = static_cast<char>((static_cast<int>(c) - base - shift + 26) % 26 + base);
                plaintext += shifted_char;
            } else {
                plaintext += c;
            }
        }
        return plaintext;
    }

    std::string vigenere_decipher(const std::string& ciphertext) {
        std::string decrypted_text;
        int key_index = 0;
        for (char c : ciphertext) {
            if (std::isalpha(c)) {
                int shift = std::tolower(key[key_index % key.size()]) - 'a';
                int base = std::isupper(c) ? 'A' : 'a';
                char decrypted_char = static_cast<char>((static_cast<int>(c) - base - shift + 26) % 26 + base);
                decrypted_text += std::isupper(c) ? std::toupper(decrypted_char) : decrypted_char;
                key_index++;
            } else {
                decrypted_text += c;
            }
        }
        return decrypted_text;
    }

    std::string rail_fence_decipher(const std::string& encrypted_text, int rails) {
        if (rails <= 0) {
            throw std::invalid_argument("Number of rails must be positive");
        }

        int len = encrypted_text.length();
        std::vector<std::vector<char>> fence(rails, std::vector<char>(len, '\0'));
        int row = 0, col = 0;
        int direction = -1;

        for (int i = 0; i < len; ++i) {
            if (row == 0 || row == rails - 1) {
                direction *= -1;
            }
            fence[row][col++] = '\0';
            row += direction;
        }

        int index = 0;
        for (int i = 0; i < rails; ++i) {
            for (int j = 0; j < len; ++j) {
                if (fence[i][j] == '\0') {
                    fence[i][j] = encrypted_text[index++];
                }
            }
        }

        row = 0, col = 0, direction = -1;
        std::string plaintext;
        for (int i = 0; i < len; ++i) {
            if (row == 0 || row == rails - 1) {
                direction *= -1;
            }
            plaintext += fence[row][col++];
            row += direction;
        }

        return plaintext;
    }
};