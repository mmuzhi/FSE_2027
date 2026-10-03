#include <string>
#include <vector>
#include <cctype>

class EncryptionUtils {
private:
    std::string key;

public:
    // Constructor
    EncryptionUtils(const std::string& key) : key(key) {}

    // Caesar cipher: shifts each alphabetic character by 'shift' positions,
    // preserving case and leaving non-letters unchanged.
    std::string caesar_cipher(const std::string& plaintext, int shift) {
        std::string ciphertext;
        for (char ch : plaintext) {
            if (std::isalpha(static_cast<unsigned char>(ch))) {
                int offset = std::isupper(static_cast<unsigned char>(ch)) ? 'A' : 'a';
                // C++ modulo can be negative for negative shift, adjust
                int shifted = ((ch - offset + shift) % 26 + 26) % 26;
                ciphertext.push_back(static_cast<char>(shifted + offset));
            } else {
                ciphertext.push_back(ch);
            }
        }
        return ciphertext;
    }

    // Vigenère cipher: encrypts using the stored key.
    // Only alphabetic characters are shifted; case is preserved.
    std::string vigenere_cipher(const std::string& plain_text) {
        std::string encrypted_text;
        size_t key_index = 0;
        for (char ch : plain_text) {
            if (std::isalpha(static_cast<unsigned char>(ch))) {
                // Determine shift from current key character (lowercased)
                int shift = std::tolower(static_cast<unsigned char>(key[key_index % key.length()])) - 'a';
                // Perform shift on lower case version, then restore original case
                char base = std::isupper(static_cast<unsigned char>(ch)) ? 'A' : 'a';
                char shifted = static_cast<char>((std::tolower(static_cast<unsigned char>(ch)) - 'a' + shift) % 26 + 'a');
                // If original was upper, result should be upper
                encrypted_text.push_back(std::isupper(static_cast<unsigned char>(ch)) ?
                                         static_cast<char>(std::toupper(static_cast<unsigned char>(shifted))) :
                                         shifted);
                ++key_index;
            } else {
                encrypted_text.push_back(ch);
            }
        }
        return encrypted_text;
    }

    // Rail Fence cipher: writes plaintext in a zigzag pattern of given rails,
    // then reads row-wise to produce ciphertext.
    std::string rail_fence_cipher(const std::string& plain_text, int rails) {
        if (rails <= 0) return plain_text;  // safeness, though rails >=1 in typical use
        int n = static_cast<int>(plain_text.length());
        // Create fence grid initialized with newline character (matching Python)
        std::vector<std::vector<char>> fence(rails, std::vector<char>(n, '\n'));

        int direction = -1;
        int row = 0, col = 0;
        for (char ch : plain_text) {
            if (row == 0 || row == rails - 1) {
                direction = -direction;  // reverse at top/bottom
            }
            fence[row][col] = ch;
            ++col;
            row += direction;
        }

        std::string encrypted_text;
        for (int i = 0; i < rails; ++i) {
            for (int j = 0; j < n; ++j) {
                if (fence[i][j] != '\n') {
                    encrypted_text.push_back(fence[i][j]);
                }
            }
        }
        return encrypted_text;
    }
};