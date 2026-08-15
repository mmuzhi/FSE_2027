#include <string>
#include <vector>
#include <cctype>

class EncryptionUtils {
private:
    std::string key;

public:
    EncryptionUtils(const std::string& key) : key(key) {}

    std::string caesar_cipher(const std::string& plaintext, int shift) const {
        std::string ciphertext;
        for (char c : plaintext) {
            if (std::isalpha(static_cast<unsigned char>(c))) {
                int offset = std::isupper(static_cast<unsigned char>(c)) ? 65 : 97;
                long long total = static_cast<long long>(c) - offset + shift;
                int shifted = static_cast<int>((total % 26 + 26) % 26);
                ciphertext += static_cast<char>(shifted + offset);
            } else {
                ciphertext += c;
            }
        }
        return ciphertext;
    }

    std::string vigenere_cipher(const std::string& plain_text) const {
        std::string encrypted_text;
        std::size_t key_index = 0;

        for (char c : plain_text) {
            if (std::isalpha(static_cast<unsigned char>(c))) {
                int shift = std::tolower(static_cast<unsigned char>(key[key_index % key.size()])) - 'a';
                int base = std::tolower(static_cast<unsigned char>(c)) - 'a';
                int encrypted = (base + shift) % 26;
                if (encrypted < 0) encrypted += 26;

                char encrypted_char = static_cast<char>('a' + encrypted);
                if (std::isupper(static_cast<unsigned char>(c))) {
                    encrypted_char = static_cast<char>(std::toupper(static_cast<unsigned char>(encrypted_char)));
                }

                encrypted_text += encrypted_char;
                ++key_index;
            } else {
                encrypted_text += c;
            }
        }

        return encrypted_text;
    }

    std::string rail_fence_cipher(const std::string& plain_text, int rails) const {
        std::vector<std::vector<char>> fence(rails, std::vector<char>(plain_text.size(), '\n'));
        int direction = -1;
        int row = 0;
        int col = 0;

        for (char c : plain_text) {
            if (row == 0 || row == rails - 1) {
                direction = -direction;
            }

            fence[row][col] = c;
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
};