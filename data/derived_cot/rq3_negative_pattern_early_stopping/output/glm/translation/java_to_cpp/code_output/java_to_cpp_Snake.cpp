#ifndef SNAKE_H
#define SNAKE_H

#include <vector>
#include <random>
#include <algorithm>

class Snake {
public:
    class Position {
    private:
        int x;
        int y;

    public:
        Position(int x, int y) : x(x), y(y) {}

        int getX() const { return x; }
        int getY() const { return y; }

        bool operator==(const Position& other) const {
            return x == other.x && y == other.y;
        }

        bool operator!=(const Position& other) const {
            return !(*this == other);
        }

        int hashCode() const {
            return 31 * x + y;
        }
    };

private:
    int length;
    const int SCREEN_WIDTH;
    const int SCREEN_HEIGHT;
    const int BLOCK_SIZE;
    std::vector<Position> positions;
    int score;
    Position foodPosition;
    std::mt19937 random;

public:
    Snake(int SCREEN_WIDTH, int SCREEN_HEIGHT, int BLOCK_SIZE, Position foodPosition)
        : length(1),
          SCREEN_WIDTH(SCREEN_WIDTH),
          SCREEN_HEIGHT(SCREEN_HEIGHT),
          BLOCK_SIZE(BLOCK_SIZE),
          score(0),
          foodPosition(foodPosition),
          random(std::random_device{}())
    {
        positions.push_back(Position(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2));
    }

    void move(Position direction) {
        Position cur = positions[0];
        int x = direction.getX();
        int y = direction.getY();

        int newX = (cur.getX() + (x * BLOCK_SIZE)) % SCREEN_WIDTH;
        int newY = (cur.getY() + (y * BLOCK_SIZE)) % SCREEN_HEIGHT;

        Position newPosition(newX, newY);

        if (newPosition == foodPosition) {
            eatFood();
        }

        if (positions.size() > 2) {
            bool contains = false;
            for (size_t i = 2; i < positions.size(); i++) {
                if (positions[i] == newPosition) {
                    contains = true;
                    break;
                }
            }
            if (contains) {
                reset();
                return;
            }
        }

        positions.insert(positions.begin(), newPosition);
        if (positions.size() > static_cast<size_t>(length)) {
            positions.pop_back();
        }
    }

    void randomFoodPosition() {
        std::uniform_int_distribution<int> distX(0, SCREEN_WIDTH / BLOCK_SIZE - 1);
        std::uniform_int_distribution<int> distY(0, SCREEN_HEIGHT / BLOCK_SIZE - 1);
        do {
            int x = distX(random) * BLOCK_SIZE;
            int y = distY(random) * BLOCK_SIZE;
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
    int getScore() const { return score; }
    Position getFoodPosition() const { return foodPosition; }
};

#endif