#include <vector>
#include <utility>
#include <algorithm>
#include <random>
#include <stdexcept>

class Snake {
private:
    std::random_device rd;
    std::mt19937 gen;

public:
    int length;
    int SCREEN_WIDTH;
    int SCREEN_HEIGHT;
    int BLOCK_SIZE;
    std::vector<std::pair<int, int>> positions;
    int score;
    std::pair<int, int> food_position;

    Snake(int SCREEN_WIDTH, int SCREEN_HEIGHT, int BLOCK_SIZE, std::pair<int, int> food_position)
        : length(1), SCREEN_WIDTH(SCREEN_WIDTH), SCREEN_HEIGHT(SCREEN_HEIGHT), 
          BLOCK_SIZE(BLOCK_SIZE), score(0), food_position(food_position), gen(rd()) {
        if (BLOCK_SIZE == 0) {
            throw std::invalid_argument("BLOCK_SIZE cannot be zero");
        }
        positions.push_back({SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2});
    }

    void move(std::pair<int, int> direction) {
        auto cur = positions[0];
        int x = direction.first;
        int y = direction.second;

        // C++ modulo can yield negative results for negative dividends, 
        // so we add SCREEN_WIDTH/SCREEN_HEIGHT before modulo to mimic Python's always-positive modulo.
        std::pair<int, int> new_pos = {
            ((cur.first + (x * BLOCK_SIZE)) % SCREEN_WIDTH + SCREEN_WIDTH) % SCREEN_WIDTH,
            ((cur.second + (y * BLOCK_SIZE)) % SCREEN_HEIGHT + SCREEN_HEIGHT) % SCREEN_HEIGHT
        };

        if (new_pos == food_position) {
            eat_food();
        }

        bool collision = false;
        if (positions.size() > 2) {
            for (size_t i = 2; i < positions.size(); ++i) {
                if (new_pos == positions[i]) {
                    collision = true;
                    break;
                }
            }
        }

        if (collision) {
            reset();
        } else {
            positions.insert(positions.begin(), new_pos);
            if (positions.size() > static_cast<size_t>(length)) {
                positions.pop_back();
            }
        }
    }

    void random_food_position() {
        int max_x = SCREEN_WIDTH / BLOCK_SIZE - 1;
        int max_y = SCREEN_HEIGHT / BLOCK_SIZE - 1;
        
        // Emulate Python's ValueError for random.randint if the range is empty
        if (max_x < 0 || max_y < 0) {
            throw std::invalid_argument("empty range for randrange()");
        }

        std::uniform_int_distribution<> distrib_x(0, max_x);
        std::uniform_int_distribution<> distrib_y(0, max_y);

        while (std::find(positions.begin(), positions.end(), food_position) != positions.end()) {
            food_position.first = distrib_x(gen) * BLOCK_SIZE;
            food_position.second = distrib_y(gen) * BLOCK_SIZE;
        }
    }

    void reset() {
        length = 1;
        positions.clear();
        positions.push_back({SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2});
        score = 0;
        random_food_position();
    }

    void eat_food() {
        length += 1;
        score += 100;
        random_food_position();
    }
};