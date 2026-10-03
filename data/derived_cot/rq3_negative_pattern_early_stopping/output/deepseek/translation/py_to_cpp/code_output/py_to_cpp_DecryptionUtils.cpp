cpp
#include <string>
#include <vector>
#include <cctype>

class DecryptionUtils {
private:
    std::string key;
public:
    DecryptionUtils(const std::string& key) : key(key) {}

    std::string caesar_decipher(const std::string& ciphertext, int shift) {
        std::string plaintext;
        for (char ch : ciphertext) {
            if (std::isalpha(static_cast<unsigned char>(ch))) {
                int ascii_offset = std::isupper(static_cast<unsigned char>(ch)) ? 'A' : 'a';
                char shifted = static_cast<char>((ch - ascii_offset - shift) % 26 + ascii_offset);
                plaintext.push_back(shifted);
            } else {
                plaintext.push_back(ch);
            }
        }
        return plaintext;
    }

    std::string vigenere_decipher(const std::string& ciphertext) {
        std::string decrypted_text;
        size_t key_index = 0;
        for (char ch : ciphertext) {
            if (std::isalpha(static_cast<unsigned char>(ch))) {
                int shift = std::tolower(static_cast<unsigned char>(key[key_index % key.size()])) - 'a';
                char decrypted_char = static_cast<char>((std::tolower(static_cast<unsigned char>(ch)) - 'a' - shift) % 26 + 'a');
                if (std::isupper(static_cast<unsigned char>(ch))) {
                    decrypted_char = std::toupper(static_cast<unsigned char>(decrypted_char));
                }
                decrypted_text.push_back(decrypted_char);
                key_index++;
            } else {
                decrypted_text.push_back(ch);
            }
        }
        return decrypted_text;
    }

    std::string rail_fence_decipher(const std::string& encrypted_text, int rails) {
        int n = encrypted_text.length();
        std::vector<std::vector<char>> fence(rails, std::vector<char>(n, '\n'));

        int direction = -1;
        int row = 0, col = 0;
        for (int i = 0; i < n; ++i) {
            if (row == 0 || row == rails - 1) {
                direction = -direction;
            }
            // In Python, they set fence[row][col] = '' (empty string)
            // We use a sentinel '\0' to mark positions to fill
            fence[row][col] = '\0';
            col++;
            row += direction;
        }

        int index = 0;
        for (int i = 0; i < rails; ++i) {
            for (int j = 0; j < n; ++j) {
                if (fence[i][j] == '\0') {
                    fence[i][j] = encrypted_text[index];
                    index++;
                }
            }
        }

        std::string plain_text;
        direction = -1;
        row = 0;
        col = 0;
        for (int i = 0; i < n; ++i) {
            if (row == 0 || row == rails - 1) {
                direction = -direction;
            }
            plain_text.push_back(fence[row][col]);
            col++;
            row += direction;
        }
        return plain_text;
    }
};