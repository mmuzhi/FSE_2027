#include <string>
#include <vector>
#include <cctype>

class DecryptionUtils {
public:
    std::string key;

    DecryptionUtils(std::string key) : key(std::move(key)) {}

    std::string caesar_decipher(std::string ciphertext, int shift) {
        std::string plaintext = "";
        for (char c : ciphertext) {
            if (std::isalpha(static_cast<unsigned char>(c))) {
                int ascii_offset = std::isupper(static_cast<unsigned char>(c)) ? 65 : 97;
                char shifted_char = static_cast<char>((c - ascii_offset - (shift % 26) + 26) % 26 + ascii_offset);
                plaintext += shifted_char;
            } else {
                plaintext += c;
            }
        }
        return plaintext;
    }

    std::string vigenere_decipher(std::string ciphertext) {
        std::string decrypted_text = "";
        int key_index = 0;
        for (char c : ciphertext) {
            if (std::isalpha(static_cast<unsigned char>(c))) {
                int shift = std::tolower(static_cast<unsigned char>(key[key_index % key.length()])) - 'a';
                char decrypted_char = static_cast<char>((std::tolower(static_cast<unsigned char>(c)) - 'a' - shift + 26) % 26 + 'a');
                decrypted_text += std::isupper(static_cast<unsigned char>(c)) ? static_cast<char>(std::toupper(static_cast<unsigned char>(decrypted_char))) : decrypted_char;
                key_index++;
            } else {
                decrypted_text += c;
            }
        }
        return decrypted_text;
    }

    std::string rail_fence_decipher(std::string encrypted_text, int rails) {
        int n = encrypted_text.length();
        std::vector<std::vector<char>> fence(rails, std::vector<char>(n, '\n'));
        int direction = -1;
        int row = 0, col = 0;

        for (int i = 0; i < n; ++i) {
            if (row == 0 || row == rails - 1) {
                direction = -direction;
            }
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

        std::string plain_text = "";
        direction = -1;
        row = 0;
        col = 0;
        for (int i = 0; i < n; ++i) {
            if (row == 0 || row == rails - 1) {
                direction = -direction;
            }
            plain_text += fence[row][col];
            col++;
            row += direction;
        }

        return plain_text;
    }
};