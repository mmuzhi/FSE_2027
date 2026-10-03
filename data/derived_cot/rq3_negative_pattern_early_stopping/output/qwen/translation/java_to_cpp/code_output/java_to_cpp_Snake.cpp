#include <vector>
#include <random>
#include <ctime>
#include <algorithm>
#include <functional>

class Snake {
private:
    int length;
    const int SCREEN_WIDTH;
    const int SCREEN_HEIGHT;
    const int BLOCK_SIZE;
    std::vector<Position> positions;
    int score;
    Position foodPosition;
    std::mt19937 random;

    struct Position {
        int x;
        int y;

        Position(int x, int y) : x(x), y(y) {}

        bool operator==(const Position& other) const {
            return x == other.x && y == other.y;
        }

        // For use with std::find_if
        bool equals(const Position& other) const {
            return x == other.x && y == other.y;
        }
    };

public:
    Snake(int SCREEN_WIDTH, int SCREEN_HEIGHT, int BLOCK_SIZE, Position foodPosition) :
        SCREEN_WIDTH(SCREEN_WIDTH),
        SCREEN_HEIGHT(SCREEN_HEIGHT),
        BLOCK_SIZE(BLOCK_SIZE),
        positions(1, Position(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)),
        score(0),
        foodPosition(foodPosition),
        random(std::mt19937(std::random_device{}())) {}

    void move(Position direction) {
        Position cur = positions[0];
        int x = direction.x;
        int y = direction.y;

        int newX = (cur.x + (x * BLOCK_SIZE)) % SCREEN_WIDTH;
        int newY = (cur.y + (y * BLOCK_SIZE)) % SCREEN_HEIGHT;

        Position newPosition(newX, newY);

        if (newPosition == foodPosition) {
            eatFood();
        }

        if (positions.size() > 2) {
            bool found = false;
            for (const auto& pos : positions) {
                if (pos == newPosition) {
                    found = true;
                    break;
                }
            }
            if (found) {
                reset();
            } else {
                positions.insert(positions.begin(), newPosition);
                if (positions.size() > length) {
                    positions.pop_back();
                }
            }
        } else {
            positions.insert(positions.begin(), newPosition);
            if (positions.size() > length) {
                positions.pop_back();
            }
        }
    }

    void randomFoodPosition() {
        do {
            std::uniform_int_distribution<int> distX(0, (SCREEN_WIDTH / BLOCK_SIZE) - 1);
            std::uniform_int_distribution<int> distY(0, (SCREEN_HEIGHT / BLOCK_SIZE) - 1);
            int x = distX(random) * BLOCK_SIZE;
            int y = distY(random) * BLOCK_SIZE;
            foodPosition = Position(x, y);
        } while (std::find_if(positions.begin(), positions.end(), [&](const Position& pos) {
            return pos.x == foodPosition.x && pos.y == foodPosition.y;
        }) != positions.end());
    }

    void reset() {
        length = 1;
        positions.clear();
        positions.push_back(Position(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2));
        score = 0;
        randomFoodPosition();
    }

    void eatFood() {
        length++;
        score += 100;
        randomFoodPosition();
    }

    int getLength() const {
        return length;
    }

    const std::vector<Position>& getPositions() const {
        return positions;
    }

    int getScore() const {
        return score;
    }

    const Position& getFoodPosition() const {
        return foodPosition;
    }
};