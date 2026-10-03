#include <string>
#include <vector>
#include <cctype>

class EncryptionUtils {
public:
    std::string key;

    EncryptionUtils(std::string key) : key(std::move(key)) {}

    std::string caesar_cipher(const std::string& plaintext, int shift) {
        std::string ciphertext = "";
        for (char c : plaintext) {
            if (std::isalpha(static_cast<unsigned char>(c))) {
                int ascii_offset = std::isupper(static_cast<unsigned char>(c)) ? 65 : 97;
                // C++ modulo can be negative for negative shifts, so we adjust to match Python's behavior
                int shifted = (c - ascii_offset + shift) % 26;
                if (shifted < 0) {
                    shifted += 26;
                }
                ciphertext += static_cast<char>(shifted + ascii_offset);
            } else {
                ciphertext += c;
            }
        }
        return ciphertext;
    }

    std::string vigenere_cipher(const std::string& plain_text) {
        std::string encrypted_text = "";
        int key_index = 0;
        for (char c : plain_text) {
            if (std::isalpha(static_cast<unsigned char>(c))) {
                char key_char = std::tolower(static_cast<unsigned char>(key[key_index % key.length()]));
                int shift = key_char - 'a';
                char lower_c = std::tolower(static_cast<unsigned char>(c));
                char encrypted_char = (lower_c - 'a' + shift) % 26 + 'a';
                encrypted_text += std::isupper(static_cast<unsigned char>(c)) ? 
                                  static_cast<char>(std::toupper(static_cast<unsigned char>(encrypted_char))) : encrypted_char;
                key_index++;
            } else {
                encrypted_text += c;
            }
        }
        return encrypted_text;
    }

    std::string rail_fence_cipher(const std::string& plain_text, int rails) {
        std::vector<std::vector<char>> fence(rails, std::vector<char>(plain_text.length(), '\n'));
        int direction = -1;
        int row = 0, col = 0;

        for (char c : plain_text) {
            if (row == 0 || row == rails - 1) {
                direction = -direction;
            }
            fence[row][col] = c;
            col++;
            row += direction;
        }

        std::string encrypted_text = "";
        for (int i = 0; i < rails; ++i) {
            for (size_t j = 0; j < plain_text.length(); ++j) {
                if (fence[i][j] != '\n') {
                    encrypted_text += fence[i][j];
                }
            }
        }
        return encrypted_text;
    }
};