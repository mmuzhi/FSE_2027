#include <string>
#include <vector>
#include <cctype>
#include <stdexcept>
#include <utility>

class EncryptionUtils {
public:
    explicit EncryptionUtils(std::string key) : key_(std::move(key)) {}

    std::string caesar_cipher(const std::string& plaintext, int shift) const {
        std::string ciphertext;
        ciphertext.reserve(plaintext.size());
        for (unsigned char ch : plaintext) {
            if (std::isalpha(ch)) {
                int ascii_offset = std::isupper(ch) ? 65 : 97;
                // Python's % always yields a non-negative result; emulate that here
                int shifted = mod26(static_cast<int>(ch) - ascii_offset + shift) + ascii_offset;
                ciphertext += static_cast<char>(shifted);
            } else {
                ciphertext += static_cast<char>(ch);
            }
        }
        return ciphertext;
    }

    std::string vigenere_cipher(const std::string& plain_text) const {
        std::string encrypted_text;
        encrypted_text.reserve(plain_text.size());
        std::size_t key_index = 0;
        for (unsigned char ch : plain_text) {
            if (std::isalpha(ch)) {
                if (key_.empty()) {
                    // Python: key_index % len(self.key) raises ZeroDivisionError
                    throw std::runtime_error("ZeroDivisionError: integer modulo by zero");
                }
                unsigned char key_char = static_cast<unsigned char>(
                    std::tolower(static_cast<unsigned char>(key_[key_index % key_.size()])));
                int shift = static_cast<int>(key_char) - 'a'; // may be outside [0,25] for non-alpha key chars
                unsigned char lower = static_cast<unsigned char>(std::tolower(ch));
                char encrypted_char = static_cast<char>(mod26(static_cast<int>(lower) - 'a' + shift) + 'a');
                encrypted_text += std::isupper(ch)
                    ? static_cast<char>(std::toupper(static_cast<unsigned char>(encrypted_char)))
                    : encrypted_char;
                ++key_index;
            } else {
                encrypted_text += static_cast<char>(ch);
            }
        }
        return encrypted_text;
    }

    std::string rail_fence_cipher(const std::string& plain_text, int rails) const {
        std::vector<std::string> fence(rails, std::string(plain_text.size(), '\n'));
        int direction = -1;
        int row = 0;
        std::size_t col = 0;

        for (unsigned char ch : plain_text) {
            if (row == 0 || row == rails - 1) {
                direction = -direction;
            }
            fence[row][col] = static_cast<char>(ch);
            ++col;
            row += direction;
        }

        std::string encrypted_text;
        for (int i = 0; i < rails; ++i) {
            for (std::size_t j = 0; j < plain_text.size(); ++j) {
                if (fence[i][j] != '\n') {
                    encrypted_text += fence[i][j];
                }
            }
        }
        return encrypted_text;
    }

private:
    std::string key_;

    static int mod26(int value) {
        return ((value % 26) + 26) % 26; // Python-style non-negative modulo
    }
};