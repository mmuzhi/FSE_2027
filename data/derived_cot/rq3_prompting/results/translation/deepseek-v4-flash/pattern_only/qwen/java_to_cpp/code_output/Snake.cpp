#include <vector>
#include <algorithm>
#include <stdexcept>
#include <chrono>
#include <random>

class Snake {
public:
    struct Position {
        Position(int x, int y) : x(x), y(y) {}

        int getX() const { return x; }
        int getY() const { return y; }

        bool operator==(const Position& other) const {
            return x == other.x && y == other.y;
        }

        bool operator!=(const Position& other) const {
            return !(*this == other);
        }

    private:
        int x;
        int y;
    };

    Snake(int SCREEN_WIDTH, int SCREEN_HEIGHT, int BLOCK_SIZE, Position foodPosition)
        : length(1),
          SCREEN_WIDTH(SCREEN_WIDTH),
          SCREEN_HEIGHT(SCREEN_HEIGHT),
          BLOCK_SIZE(BLOCK_SIZE),
          positions(1, Position(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)),
          score(0),
          foodPosition(foodPosition),
          rng(static_cast<unsigned int>(
              std::chrono::system_clock::now().time_since_epoch().count())) {}

    void move(Position direction) {
        if (positions.empty()) throw std::out_of_range("positions is empty");

        Position cur = positions.front();
        int x = direction.getX();
        int y = direction.getY();

        if (SCREEN_WIDTH == 0) throw std::runtime_error("division by zero");
        int newX = (cur.getX() + (x * BLOCK_SIZE)) % SCREEN_WIDTH;

        if (SCREEN_HEIGHT == 0) throw std::runtime_error("division by zero");
        int newY = (cur.getY() + (y * BLOCK_SIZE)) % SCREEN_HEIGHT;

        Position newPosition(newX, newY);

        if (newPosition == foodPosition) {
            eatFood();
        }

        if (positions.size() > 2 &&
            std::find(positions.begin() + 2, positions.end(), newPosition) != positions.end()) {
            reset();
        } else {
            positions.insert(positions.begin(), newPosition);
            if (positions.size() > length) {
                positions.pop_back();
            }
        }
    }

    void randomFoodPosition() {
        if (BLOCK_SIZE == 0) throw std::runtime_error("division by zero");
        do {
            int x = randomInt(SCREEN_WIDTH / BLOCK_SIZE) * BLOCK_SIZE;
            int y = randomInt(SCREEN_HEIGHT / BLOCK_SIZE) * BLOCK_SIZE;
            foodPosition = Position(x, y);
        } while (std::find(positions.begin(), positions.end(), foodPosition) != positions.end());
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

    int getLength() const { return length; }

    std::vector<Position>& getPositions() { return positions; }
    const std::vector<Position>& getPositions() const { return positions; }

    int getScore() const { return score; }

    const Position& getFoodPosition() const { return foodPosition; }

private:
    int length;
    const int SCREEN_WIDTH;
    const int SCREEN_HEIGHT;
    const int BLOCK_SIZE;
    std::vector<Position> positions;
    int score;
    Position foodPosition;
    std::mt19937 rng;

    int randomInt(int bound) {
        if (bound <= 0) throw std::invalid_argument("bound must be positive");
        std::uniform_int_distribution<int> dist(0, bound - 1);
        return dist(rng);
    }
};