#include <vector>
#include <utility>
#include <cmath>
#include <cstdlib>
#include <iostream>

class Snake {
private:
    double SCREEN_WIDTH;
    double SCREEN_HEIGHT;
    double BLOCK_SIZE;
    int length;
    std::vector<std::pair<double, double>> positions;
    double score;
    std::pair<double, double> food_position;

public:
    Snake(double SCREEN_WIDTH, double SCREEN_HEIGHT, double BLOCK_SIZE, std::pair<double, double> food_position) {
        this->SCREEN_WIDTH = SCREEN_WIDTH;
        this->SCREEN_HEIGHT = SCREEN_HEIGHT;
        this->BLOCK_SIZE = BLOCK_SIZE;
        this->length = 1;
        this->positions = [{(SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2)}];
        this->score = 0;
        this->food_position = food_position;
    }

    void move(std::pair<int, int> direction) {
        double cur_x = positions[0].first;
        double cur_y = positions[0].second;
        int dx = direction.first;
        int dy = direction.second;

        double new_x = cur_x + (dx * BLOCK_SIZE);
        double new_y = cur_y + (dy * BLOCK_SIZE);

        new_x = fmod(new_x, SCREEN_WIDTH);
        new_y = fmod(new_y, SCREEN_HEIGHT);

        if (new_x < 0) new_x += SCREEN_WIDTH;
        if (new_y < 0) new_y += SCREEN_HEIGHT;

        if (new_x == food_position.first && new_y == food_position.second) {
            eat_food();
        }

        if (positions.size() > 2 && 
            (std::find(positions.begin() + 2, positions.end(), std::make_pair(new_x, new_y)) != positions.end())) {
            reset();
        } else {
            positions.insert(positions.begin(), {new_x, new_y});
            if (positions.size() > length) {
                positions.pop_back();
            }
        }
    }

    void random_food_position() {
        int num_blocks_x = static_cast<int>(SCREEN_WIDTH / BLOCK_SIZE);
        int num_blocks_y = static_cast<int>(SCREEN_HEIGHT / BLOCK_SIZE);

        while (true) {
            int x = rand() % num_blocks_x;
            int y = rand() % num_blocks_y;
            double new_x = x * BLOCK_SIZE;
            double new_y = y * BLOCK_SIZE;

            bool inSnake = false;
            for (const auto& pos : positions) {
                if (pos.first == new_x && pos.second == new_y) {
                    inSnake = true;
                    break;
                }
            }

            if (!inSnake) {
                food_position = {new_x, new_y};
                break;
            }
        }
    }

    void reset() {
        length = 1;
        positions = [{(SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2)}];
        score = 0;
        random_food_position();
    }

    void eat_food() {
        length++;
        score += 100;
        random_food_position();
    }
};