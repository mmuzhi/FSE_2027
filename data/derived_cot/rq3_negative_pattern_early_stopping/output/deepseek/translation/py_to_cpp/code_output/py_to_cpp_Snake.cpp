#include <deque>
#include <utility>
#include <random>
#include <cmath>
#include <algorithm>

class Snake {
public:
    Snake(int SCREEN_WIDTH, int SCREEN_HEIGHT, int BLOCK_SIZE, std::pair<int, int> food_position)
        : length(1), SCREEN_WIDTH(SCREEN_WIDTH), SCREEN_HEIGHT(SCREEN_HEIGHT),
          BLOCK_SIZE(BLOCK_SIZE), score(0) {
        // initial head position: (SCREEN_WIDTH/2, SCREEN_HEIGHT/2) -> double
        positions.push_back({static_cast<double>(SCREEN_WIDTH) / 2.0,
                             static_cast<double>(SCREEN_HEIGHT) / 2.0});
        // store food position as double (exact conversion for int)
        this->food_position = {static_cast<double>(food_position.first),
                               static_cast<double>(food_position.second)};
        // seed random generator
        std::random_device rd;
        rng.seed(rd());
    }

    void move(std::pair<int, int> direction) {
        auto cur = positions.front();

        // Python‑style modulo: always non‑negative result
        double new_x = cur.first + direction.first * BLOCK_SIZE;
        new_x = std::fmod(new_x, SCREEN_WIDTH);
        if (new_x < 0) new_x += SCREEN_WIDTH;

        double new_y = cur.second + direction.second * BLOCK_SIZE;
        new_y = std::fmod(new_y, SCREEN_HEIGHT);
        if (new_y < 0) new_y += SCREEN_HEIGHT;

        auto new_pos = std::make_pair(new_x, new_y);

        // check if food was eaten
        if (new_pos == food_position) {
            eat_food();
        }

        // check collision with body (positions[2:])
        bool hit_body = false;
        if (positions.size() > 2) {
            auto it = positions.begin();
            std::advance(it, 2); // start at index 2
            for (; it != positions.end(); ++it) {
                if (it->first == new_pos.first && it->second == new_pos.second) {
                    hit_body = true;
                    break;
                }
            }
        }

        if (hit_body) {
            reset();
        } else {
            positions.push_front(new_pos);
            if (positions.size() > static_cast<size_t>(length)) {
                positions.pop_back();
            }
        }
    }

    void random_food_position() {
        // generate random integer grid coordinates, then multiply by BLOCK_SIZE
        int max_x = SCREEN_WIDTH / BLOCK_SIZE - 1;
        int max_y = SCREEN_HEIGHT / BLOCK_SIZE - 1;
        // assume valid input: max_x >= 0, max_y >= 0
        std::uniform_int_distribution<int> dist_x(0, max_x);
        std::uniform_int_distribution<int> dist_y(0, max_y);

        do {
            int x = dist_x(rng) * BLOCK_SIZE;
            int y = dist_y(rng) * BLOCK_SIZE;
            food_position = {static_cast<double>(x), static_cast<double>(y)};
        } while (is_food_on_snake());
    }

    void reset() {
        length = 1;
        positions.clear();
        positions.push_back({static_cast<double>(SCREEN_WIDTH) / 2.0,
                             static_cast<double>(SCREEN_HEIGHT) / 2.0});
        score = 0;
        random_food_position();
    }

    void eat_food() {
        length += 1;
        score += 100;
        random_food_position();
    }

private:
    int length;
    int SCREEN_WIDTH;
    int SCREEN_HEIGHT;
    int BLOCK_SIZE;
    std::deque<std::pair<double, double>> positions;
    int score;
    std::pair<double, double> food_position;
    std::mt19937 rng;

    bool is_food_on_snake() const {
        // check if food_position is equal to any element in positions
        auto it = std::find(positions.begin(), positions.end(), food_position);
        return it != positions.end();
    }
};