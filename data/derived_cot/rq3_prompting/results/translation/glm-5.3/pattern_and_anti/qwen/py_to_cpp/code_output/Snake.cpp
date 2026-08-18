#include <cstdlib>
#include <utility>
#include <vector>

class Snake {
public:
    int length;
    int SCREEN_WIDTH;
    int SCREEN_HEIGHT;
    int BLOCK_SIZE;
    std::vector<std::pair<int, int>> positions;
    int score;
    std::pair<int, int> food_position;

    Snake(int screen_width, int screen_height, int block_size,
          std::pair<int, int> food_pos)
        : length(1),
          SCREEN_WIDTH(screen_width),
          SCREEN_HEIGHT(screen_height),
          BLOCK_SIZE(block_size),
          positions(1, std::make_pair(screen_width / 2, screen_height / 2)),
          score(0),
          food_position(food_pos) {}

    // Python-style modulo: result is always non-negative for positive modulus
    static int mod(int a, int m) {
        int r = a % m;
        return r < 0 ? r + m : r;
    }

    void move(std::pair<int, int> direction) {
        std::pair<int, int> cur = positions[0];
        int x = direction.first;
        int y = direction.second;

        std::pair<int, int> new_pos(
            mod(cur.first + x * BLOCK_SIZE, SCREEN_WIDTH),
            mod(cur.second + y * BLOCK_SIZE, SCREEN_HEIGHT)
        );

        if (new_pos == food_position) {
            eat_food();
        }

        bool collide = false;
        if (positions.size() > 2) {
            // equivalent of: new in self.positions[2:]
            for (std::size_t i = 2; i < positions.size(); ++i) {
                if (positions[i] == new_pos) {
                    collide = true;
                    break;
                }
            }
        }

        if (collide) {
            reset();
        } else {
            positions.insert(positions.begin(), new_pos);
            if (static_cast<int>(positions.size()) > length) {
                positions.pop_back();
            }
        }
    }

    void random_food_position() {
        while (food_on_snake()) {
            int width_blocks = SCREEN_WIDTH / BLOCK_SIZE;
            int height_blocks = SCREEN_HEIGHT / BLOCK_SIZE;
            food_position.first = (std::rand() % width_blocks) * BLOCK_SIZE;
            food_position.second = (std::rand() % height_blocks) * BLOCK_SIZE;
        }
    }

    void reset() {
        length = 1;
        positions.assign(1, std::make_pair(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2));
        score = 0;
        random_food_position();
    }

    void eat_food() {
        length += 1;
        score += 100;
        random_food_position();
    }

private:
    bool food_on_snake() const {
        for (const auto& pos : positions) {
            if (pos == food_position) {
                return true;
            }
        }
        return false;
    }
};