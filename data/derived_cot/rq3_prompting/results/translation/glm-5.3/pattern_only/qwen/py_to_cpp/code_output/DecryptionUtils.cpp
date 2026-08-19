#include <string>
#include <vector>
#include <cctype>
#include <stdexcept>

class DecryptionUtils {
public:
    DecryptionUtils(std::string key) : key_(std::move(key)) {}

    std::string caesar_decipher(const std::string& ciphertext, int shift) const {
        std::string plaintext;
        for (char ch : ciphertext) {
            unsigned char uc = static_cast<unsigned char>(ch);
            if (std::isalpha(uc)) {
                int ascii_offset = std::isupper(uc) ? 65 : 97;
                // Python's % always yields a non-negative result; emulate that.
                int shifted = ((static_cast<int>(uc) - ascii_offset - shift) % 26 + 26) % 26;
                plaintext += static_cast<char>(shifted + ascii_offset);
            } else {
                plaintext += ch;
            }
        }
        return plaintext;
    }

    std::string vigenere_decipher(const std::string& ciphertext) const {
        std::string decrypted_text;
        std::size_t key_index = 0;
        const std::size_t key_len = key_.size();
        for (char ch : ciphertext) {
            unsigned char uc = static_cast<unsigned char>(ch);
            if (std::isalpha(uc)) {
                if (key_len == 0) {
                    // Python would raise ZeroDivisionError (key_index % len(self.key))
                    throw std::runtime_error("integer division or modulo by zero");
                }
                unsigned char key_char = static_cast<unsigned char>(key_[key_index % key_len]);
                int shift = std::tolower(key_char) - 'a';
                int base = std::tolower(uc) - 'a';
                int dec = ((base - shift) % 26 + 26) % 26 + 'a';
                char decrypted_char = static_cast<char>(dec);
                decrypted_text += std::isupper(uc)
                                      ? static_cast<char>(std::toupper(static_cast<unsigned char>(decrypted_char)))
                                      : decrypted_char;
                ++key_index;
            } else {
                decrypted_text += ch;
            }
        }
        return decrypted_text;
    }

    std::string rail_fence_decipher(const std::string& encrypted_text, int rails) const {
        const int n = static_cast<int>(encrypted_text.size());
        // '\n' = untouched cell (Python's initial '\n'), '\0' = marked path cell (Python's '')
        std::vector<std::vector<char>> fence(rails, std::vector<char>(n, '\n'));
        int direction = -1;
        int row = 0, col = 0;

        for (int i = 0; i < n; ++i) {
            if (row == 0 || row == rails - 1) {
                direction = -direction;
            }
            fence.at(row).at(col) = '\0'; // .at() mirrors Python's IndexError on bad rails
            ++col;
            row += direction;
        }

        int index = 0;
        for (int i = 0; i < rails; ++i) {
            for (int j = 0; j < n; ++j) {
                if (fence[i][j] == '\0') {
                    fence[i][j] = encrypted_text[index++];
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
            plain_text += fence.at(row).at(col);
            ++col;
            row += direction;
        }

        return plain_text;
    }

private:
    std::string key_;
};