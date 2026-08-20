#include <cctype>
#include <cstddef>
#include <stdexcept>
#include <string>
#include <vector>

class EncryptionUtils {
public:
    EncryptionUtils(std::string key) : key_(std::move(key)) {}

    // Encrypts the plaintext using the Caesar cipher.
    std::string caesar_cipher(const std::string& plaintext, long long shift) const {
        std::string ciphertext;
        ciphertext.reserve(plaintext.size());
        for (char c : plaintext) {
            unsigned char ch = static_cast<unsigned char>(c);
            if (std::isalpha(ch)) {
                int ascii_offset = std::isupper(ch) ? 65 : 97;
                long long pos = (static_cast<long long>(ch) - ascii_offset + shift) % 26;
                if (pos < 0) pos += 26;  // Python's % always yields a non-negative result
                ciphertext += static_cast<char>(pos + ascii_offset);
            } else {
                ciphertext += c;
            }
        }
        return ciphertext;
    }

    // Encrypts the plaintext using the Vigenere cipher.
    std::string vigenere_cipher(const std::string& plain_text) const {
        std::string encrypted_text;
        encrypted_text.reserve(plain_text.size());
        std::size_t key_index = 0;
        for (char c : plain_text) {
            unsigned char ch = static_cast<unsigned char>(c);
            if (std::isalpha(ch)) {
                if (key_.empty()) {
                    // Python raises ZeroDivisionError (integer modulo by zero) here.
                    throw std::runtime_error("integer modulo by zero");
                }
                unsigned char key_char = static_cast<unsigned char>(
                    std::tolower(static_cast<unsigned char>(key_[key_index % key_.size()])));
                int shift = static_cast<int>(key_char) - 'a';
                int base = static_cast<int>(std::tolower(ch)) - 'a';
                int pos = (base + shift) % 26;
                if (pos < 0) pos += 26;  // Python's % always yields a non-negative result
                char encrypted_char = static_cast<char>(pos + 'a');
                if (std::isupper(ch)) {
                    encrypted_char = static_cast<char>(
                        std::toupper(static_cast<unsigned char>(encrypted_char)));
                }
                encrypted_text += encrypted_char;
                ++key_index;
            } else {
                encrypted_text += c;
            }
        }
        return encrypted_text;
    }

    // Encrypts the plaintext using the Rail Fence cipher.
    std::string rail_fence_cipher(const std::string& plain_text, int rails) const {
        const std::size_t cols = plain_text.size();
        std::vector<std::vector<char>> fence;
        if (rails > 0) {
            fence.assign(static_cast<std::size_t>(rails),
                         std::vector<char>(cols, '\n'));
        }
        int direction = -1;
        std::size_t row = 0;
        std::size_t col = 0;

        for (char c : plain_text) {
            if (row == 0 || row == static_cast<std::size_t>(rails) - 1) {
                direction = -direction;
            }
            // .at() mirrors Python's IndexError for degenerate rail counts (e.g. 0, 1, negative).
            fence.at(row).at(col) = c;
            ++col;
            row += static_cast<std::size_t>(direction);
        }

        std::string encrypted_text;
        for (int i = 0; i < rails; ++i) {
            const std::vector<char>& fence_row = fence[static_cast<std::size_t>(i)];
            for (std::size_t j = 0; j < cols; ++j) {
                if (fence_row[j] != '\n') {
                    encrypted_text += fence_row[j];
                }
            }
        }
        return encrypted_text;
    }

private:
    std::string key_;
};