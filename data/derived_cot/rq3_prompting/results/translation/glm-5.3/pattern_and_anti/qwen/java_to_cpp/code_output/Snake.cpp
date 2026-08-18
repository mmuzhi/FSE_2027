#include <vector>
#include <random>
#include <algorithm>
#include <cstddef>

namespace org {
namespace example {

class Snake {
public:
    class Position {
    public:
        Position(int x, int y) : x(x), y(y) {}

        int getX() const { return x; }
        int getY() const { return y; }

        bool operator==(const Position& o) const {
            return x == o.x && y == o.y;
        }

        bool operator!=(const Position& o) const {
            return !(*this == o);
        }

    private:
        int x;
        int y;
    };

    Snake(int screenWidth, int screenHeight, int blockSize, const Position& food)
        : length(1),
          SCREEN_WIDTH(screenWidth),
          SCREEN_HEIGHT(screenHeight),
          BLOCK_SIZE(blockSize),
          positions(),
          score(0),
          foodPosition(food),
          random(std::random_device{}()) {
        positions.push_back(Position(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2));
    }

    void move(const Position& direction) {
        const Position& cur = positions.front();
        int x = direction.getX();
        int y = direction.getY();

        int newX = (cur.getX() + (x * BLOCK_SIZE)) % SCREEN_WIDTH;
        int newY = (cur.getY() + (y * BLOCK_SIZE)) % SCREEN_HEIGHT;

        Position newPosition(newX, newY);

        if (newPosition == foodPosition) {
            eatFood();
        }

        bool selfCollision =
            positions.size() > 2 &&
            std::find(positions.begin() + 2, positions.end(), newPosition) != positions.end();

        if (selfCollision) {
            reset();
        } else {
            positions.insert(positions.begin(), newPosition);
            if (positions.size() > static_cast<std::size_t>(length)) {
                positions.pop_back();
            }
        }
    }

    void randomFoodPosition() {
        std::uniform_int_distribution<int> xDist(0, SCREEN_WIDTH / BLOCK_SIZE - 1);
        std::uniform_int_distribution<int> yDist(0, SCREEN_HEIGHT / BLOCK_SIZE - 1);
        do {
            int x = xDist(random) * BLOCK_SIZE;
            int y = yDist(random) * BLOCK_SIZE;
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
    std::mt19937 random;
};

} // namespace example
} // namespace org