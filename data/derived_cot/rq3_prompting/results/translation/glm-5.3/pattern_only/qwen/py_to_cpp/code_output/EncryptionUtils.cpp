#include <cctype>
#include <stdexcept>
#include <string>
#include <vector>

class EncryptionUtils {
public:
    std::string key;

    explicit EncryptionUtils(std::string key) : key(std::move(key)) {}

    std::string caesar_cipher(const std::string& plaintext, int shift) const {
        std::string ciphertext;
        ciphertext.reserve(plaintext.size());
        for (char ch : plaintext) {
            unsigned char c = static_cast<unsigned char>(ch);
            if (std::isalpha(c)) {
                int ascii_offset = std::isupper(c) ? 65 : 97;
                int shifted = (static_cast<int>(c) - ascii_offset + shift) % 26;
                if (shifted < 0) shifted += 26;  // Python's % is always non-negative
                ciphertext += static_cast<char>(shifted + ascii_offset);
            } else {
                ciphertext += ch;
            }
        }
        return ciphertext;
    }

    std::string vigenere_cipher(const std::string& plain_text) const {
        std::string encrypted_text;
        encrypted_text.reserve(plain_text.size());
        std::size_t key_index = 0;
        for (char ch : plain_text) {
            unsigned char c = static_cast<unsigned char>(ch);
            if (std::isalpha(c)) {
                if (key.empty()) {
                    // Python raises ZeroDivisionError on key_index % len(self.key)
                    throw std::runtime_error("integer division or modulo by zero");
                }
                unsigned char kc = static_cast<unsigned char>(key[key_index % key.size()]);
                int shift = std::tolower(kc) - 'a';
                int shifted = (((std::tolower(c) - 'a') + shift) % 26 + 26) % 26;
                char encrypted_char = static_cast<char>(shifted + 'a');
                if (std::isupper(c)) {
                    encrypted_char = static_cast<char>(
                        std::toupper(static_cast<unsigned char>(encrypted_char)));
                }
                encrypted_text += encrypted_char;
                ++key_index;
            } else {
                encrypted_text += ch;
            }
        }
        return encrypted_text;
    }

    std::string rail_fence_cipher(const std::string& plain_text, int rails) const {
        std::size_t nrows = rails > 0 ? static_cast<std::size_t>(rails) : 0;
        std::vector<std::vector<char>> fence(
            nrows, std::vector<char>(plain_text.size(), '\n'));
        int direction = -1;
        int row = 0;
        std::size_t col = 0;

        for (char ch : plain_text) {
            if (row == 0 || row == rails - 1) {
                direction = -direction;
            }
            if (row < 0 || static_cast<std::size_t>(row) >= fence.size()) {
                // Mirrors Python IndexError (e.g. rails == 1 with input longer than 1)
                throw std::out_of_range("list index out of range");
            }
            fence[static_cast<std::size_t>(row)][col] = ch;
            ++col;
            row += direction;
        }

        std::string encrypted_text;
        for (std::size_t i = 0; i < fence.size(); ++i) {
            for (std::size_t j = 0; j < plain_text.size(); ++j) {
                if (fence[i][j] != '\n') {
                    encrypted_text += fence[i][j];
                }
            }
        }
        return encrypted_text;
    }
};