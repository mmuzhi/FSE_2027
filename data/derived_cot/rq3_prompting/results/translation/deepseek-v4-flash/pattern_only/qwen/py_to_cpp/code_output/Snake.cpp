#include <vector>
#include <utility>
#include <random>
#include <algorithm>
#include <cmath>

class Snake {
public:
    int length;
    int SCREEN_WIDTH;
    int SCREEN_HEIGHT;
    int BLOCK_SIZE;
    std::vector<std::pair<double, double>> positions;
    int score;
    std::pair<double, double> food_position;

    Snake(int SCREEN_WIDTH, int SCREEN_HEIGHT, int BLOCK_SIZE, std::pair<double, double> food_position)
        : length(1),
          SCREEN_WIDTH(SCREEN_WIDTH),
          SCREEN_HEIGHT(SCREEN_HEIGHT),
          BLOCK_SIZE(BLOCK_SIZE),
          positions(1, std::make_pair(SCREEN_WIDTH / 2.0, SCREEN_HEIGHT / 2.0)),
          score(0),
          food_position(food_position) {}

    void move(std::pair<int, int> direction) {
        auto cur = positions[0];
        int x = direction.first;
        int y = direction.second;

        double new_x = mod(cur.first + x * BLOCK_SIZE, SCREEN_WIDTH);
        double new_y = mod(cur.second + y * BLOCK_SIZE, SCREEN_HEIGHT);
        std::pair<double, double> new_pos = {new_x, new_y};

        if (new_pos == food_position) {
            eat_food();
        }

        if (positions.size() > 2) {
            for (size_t i = 2; i < positions.size(); ++i) {
                if (new_pos == positions[i]) {
                    reset();
                    return;
                }
            }
        }

        positions.insert(positions.begin(), new_pos);
        if (positions.size() > static_cast<size_t>(length)) {
            positions.pop_back();
        }
    }

    void random_food_position() {
        static std::mt19937 gen(std::random_device{}());
        int max_x = SCREEN_WIDTH / BLOCK_SIZE - 1;
        int max_y = SCREEN_HEIGHT / BLOCK_SIZE - 1;
        std::uniform_int_distribution<int> dist_x(0, max_x);
        std::uniform_int_distribution<int> dist_y(0, max_y);

        do {
            food_position = {dist_x(gen) * BLOCK_SIZE, dist_y(gen) * BLOCK_SIZE};
        } while (std::find(positions.begin(), positions.end(), food_position) != positions.end());
    }

    void reset() {
        length = 1;
        positions.clear();
        positions.push_back({SCREEN_WIDTH / 2.0, SCREEN_HEIGHT / 2.0});
        score = 0;
        random_food_position();
    }

    void eat_food() {
        length += 1;
        score += 100;
        random_food_position();
    }

private:
    static double mod(double a, double b) {
        double r = std::fmod(a, b);
        if (r < 0) r += b;
        return r;
    }
};