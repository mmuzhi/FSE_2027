#include <string>
#include <vector>
#include <cctype>
#include <stdexcept>

class DecryptionUtils {
public:
    DecryptionUtils(const std::string& key) : key(key) {}

    std::string caesar_decipher(const std::string& ciphertext, int shift) {
        std::string plaintext;
        for (char ch : ciphertext) {
            unsigned char c = static_cast<unsigned char>(ch);
            if (std::isalpha(c)) {
                int ascii_offset = std::isupper(c) ? 65 : 97;
                int shifted = ((static_cast<int>(c) - ascii_offset - shift) % 26 + 26) % 26 + ascii_offset;
                plaintext += static_cast<char>(shifted);
            } else {
                plaintext += ch;
            }
        }
        return plaintext;
    }

    std::string vigenere_decipher(const std::string& ciphertext) {
        std::string decrypted_text;
        std::size_t key_index = 0;
        for (char ch : ciphertext) {
            unsigned char c = static_cast<unsigned char>(ch);
            if (std::isalpha(c)) {
                if (key.empty())
                    throw std::runtime_error("integer division or modulo by zero");
                int shift = std::tolower(static_cast<unsigned char>(key[key_index % key.size()])) - 'a';
                int dec = ((std::tolower(c) - 'a' - shift) % 26 + 26) % 26 + 'a';
                char decrypted_char = static_cast<char>(dec);
                decrypted_text += std::isupper(c)
                                      ? static_cast<char>(std::toupper(static_cast<unsigned char>(decrypted_char)))
                                      : decrypted_char;
                ++key_index;
            } else {
                decrypted_text += ch;
            }
        }
        return decrypted_text;
    }

    std::string rail_fence_decipher(const std::string& encrypted_text, int rails) {
        std::vector<std::vector<char>> fence(rails,
                                             std::vector<char>(encrypted_text.size(), '\n'));
        int direction = -1;
        int row = 0, col = 0;

        for (std::size_t i = 0; i < encrypted_text.size(); ++i) {
            if (row == 0 || row == rails - 1) {
                direction = -direction;
            }
            fence[row][col] = '\0';
            ++col;
            row += direction;
        }

        std::size_t index = 0;
        for (int i = 0; i < rails; ++i) {
            for (std::size_t j = 0; j < encrypted_text.size(); ++j) {
                if (fence[i][j] == '\0') {
                    fence[i][j] = encrypted_text[index];
                    ++index;
                }
            }
        }

        std::string plain_text;
        direction = -1;
        row = 0;
        col = 0;
        for (std::size_t i = 0; i < encrypted_text.size(); ++i) {
            if (row == 0 || row == rails - 1) {
                direction = -direction;
            }
            plain_text += fence[row][col];
            ++col;
            row += direction;
        }

        return plain_text;
    }

private:
    std::string key;
};