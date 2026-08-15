#include <string>
#include <vector>
#include <cctype>
#include <stdexcept>

class DecryptionUtils {
public:
    std::string key;

    DecryptionUtils(const std::string& key) : key(key) {}

    std::string caesar_decipher(const std::string& ciphertext, int shift) const {
        std::string plaintext;
        for (char c : ciphertext) {
            if (std::isalpha(static_cast<unsigned char>(c))) {
                int ascii_offset = std::isupper(static_cast<unsigned char>(c)) ? 65 : 97;
                int shifted = ((c - ascii_offset - shift) % 26 + 26) % 26 + ascii_offset;
                plaintext += static_cast<char>(shifted);
            } else {
                plaintext += c;
            }
        }
        return plaintext;
    }

    std::string vigenere_decipher(const std::string& ciphertext) const {
        std::string decrypted_text;
        std::size_t key_index = 0;

        for (char c : ciphertext) {
            if (std::isalpha(static_cast<unsigned char>(c))) {
                if (key.empty()) {
                    throw std::domain_error("division by zero");
                }
                char key_char = key[key_index % key.length()];
                int shift = std::tolower(static_cast<unsigned char>(key_char)) - 'a';
                int decrypted = ((std::tolower(static_cast<unsigned char>(c)) - 'a' - shift) % 26 + 26) % 26 + 'a';
                char decrypted_char = static_cast<char>(decrypted);

                if (std::isupper(static_cast<unsigned char>(c))) {
                    decrypted_text += static_cast<char>(std::toupper(static_cast<unsigned char>(decrypted_char)));
                } else {
                    decrypted_text += decrypted_char;
                }
                ++key_index;
            } else {
                decrypted_text += c;
            }
        }
        return decrypted_text;
    }

    std::string rail_fence_decipher(const std::string& encrypted_text, int rails) const {
        int n = static_cast<int>(encrypted_text.size());
        std::vector<std::vector<char>> fence;
        if (rails > 0) {
            fence.assign(rails, std::vector<char>(n, '\n'));
        }

        int direction = -1;
        int row = 0, col = 0;

        for (int i = 0; i < n; ++i) {
            if (row == 0 || row == rails - 1) {
                direction = -direction;
            }
            fence.at(row).at(col) = '\0';
            ++col;
            row += direction;
        }

        int index = 0;
        for (int i = 0; i < rails; ++i) {
            for (int j = 0; j < n; ++j) {
                if (fence.at(i).at(j) == '\0') {
                    fence.at(i).at(j) = encrypted_text[index];
                    ++index;
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
};