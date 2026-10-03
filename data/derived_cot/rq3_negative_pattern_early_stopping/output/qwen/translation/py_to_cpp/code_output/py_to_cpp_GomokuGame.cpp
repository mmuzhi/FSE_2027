#include <vector>
#include <utility> // for std::pair

class GomokuGame {
private:
    int board_size;
    std::vector<std::vector<char>> board;
    char current_player;

    bool _check_five_in_a_row(int row, int col, int dx, int dy) {
        char symbol = board[row][col];
        int count = 1;

        for (int i = 1; i < 5; ++i) {
            int new_row = row + dx * i;
            int new_col = col + dy * i;

            if (new_row < 0 || new_row >= board_size || new_col < 0 || new_col >= board_size) {
                return false;
            }

            if (board[new_row][new_col] != symbol) {
                return false;
            }

            count++;
        }

        return count == 5;
    }

public:
    GomokuGame(int board_size) : board_size(board_size) {
        board = std::vector<std::vector<char>>(board_size, std::vector<char>(board_size, ' '));
        current_player = 'X';
    }

    bool make_move(int row, int col) {
        if (row < 0 || row >= board_size || col < 0 || col >= board_size) {
            return false;
        }

        if (board[row][col] == ' ') {
            board[row][col] = current_player;
            current_player = (current_player == 'X') ? 'O' : 'X';
            return true;
        }

        return false;
    }

    char check_winner() {
        static const std::vector<std::pair<int, int>> directions = {{0, 1}, {1, 0}, {1, 1}, {1, -1}};

        for (int row = 0; row < board_size; ++row) {
            for (int col = 0; col < board_size; ++col) {
                if (board[row][col] != ' ') {
                    for (const auto& dir : directions) {
                        if (_check_five_in_a_row(row, col, dir.first, dir.second)) {
                            return board[row][col];
                        }
                    }
                }
            }
        }

        return 0;
    }
};