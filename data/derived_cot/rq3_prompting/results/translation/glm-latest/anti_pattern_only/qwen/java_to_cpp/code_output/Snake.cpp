#include <algorithm>
#include <chrono>
#include <cstdint>
#include <limits>
#include <stdexcept>
#include <vector>

namespace org {
namespace example {

class Snake {
public:
    class Position {
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

        // Mirrors Java's hashCode(): 31 * x + y with 32-bit two's-complement wraparound.
        int hashCode() const {
            return static_cast<int>(31u * static_cast<unsigned int>(x)
                                    + static_cast<unsigned int>(y));
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
          positions(),
          score(0),
          foodPosition(foodPosition),
          random() {
        positions.push_back(Position(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2));
    }

    void move(Position direction) {
        Position cur = positions.at(0);
        int x = direction.getX();
        int y = direction.getY();

        int newX = (cur.getX() + (x * BLOCK_SIZE)) % SCREEN_WIDTH;
        int newY = (cur.getY() + (y * BLOCK_SIZE)) % SCREEN_HEIGHT;

        Position newPosition(newX, newY);

        if (newPosition == foodPosition) {
            eatFood();
        }

        if (positions.size() > 2
            && std::find(positions.begin() + 2, positions.end(), newPosition) != positions.end()) {
            reset();
        } else {
            positions.insert(positions.begin(), newPosition);
            if (positions.size() > static_cast<std::size_t>(length)) {
                positions.pop_back();
            }
        }
    }

    void randomFoodPosition() {
        do {
            int x = random.nextInt(SCREEN_WIDTH / BLOCK_SIZE) * BLOCK_SIZE;
            int y = random.nextInt(SCREEN_HEIGHT / BLOCK_SIZE) * BLOCK_SIZE;
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

    int getLength() const {
        return length;
    }

    std::vector<Position>& getPositions() {
        return positions;
    }

    int getScore() const {
        return score;
    }

    Position getFoodPosition() const {
        return foodPosition;
    }

private:
    // Faithful port of java.util.Random so nextInt(bound) produces the same
    // distribution and rejection logic as the original.
    class JavaRandom {
    public:
        JavaRandom() {
            // java.util.Random's no-arg constructor seeds nondeterministically
            // (nanoTime ^ seedUniquifier); approximate with clock-based seeding.
            uint64_t seed =
                static_cast<uint64_t>(
                    std::chrono::system_clock::now().time_since_epoch().count())
                ^ (static_cast<uint64_t>(
                       std::chrono::steady_clock::now().time_since_epoch().count())
                   * 0x9E3779B97F4A7C15ULL);
            setSeed(seed);
        }

        explicit JavaRandom(uint64_t seed) {
            setSeed(seed);
        }

        void setSeed(uint64_t seed) {
            this->seed = (seed ^ 0x5DEECE66DULL) & ((1ULL << 48) - 1);
        }

        int nextInt(int bound) {
            if (bound <= 0) {
                throw std::invalid_argument("bound must be positive");
            }
            int r = next(31);
            int m = bound - 1;
            if ((bound & m) == 0) {
                // bound is a power of two
                return static_cast<int>((static_cast<int64_t>(bound) * r) >> 31);
            }
            int bits;
            int val;
            do {
                bits = next(31);
                val = bits % bound;
                // Java relies on int32 overflow (wraparound) here; reproduce it
                // exactly with a 64-bit comparison against INT32_MAX.
            } while (static_cast<int64_t>(bits) - val + m
                     > static_cast<int64_t>(std::numeric_limits<int>::max()));
            return val;
        }

    private:
        uint64_t seed;

        int next(int bits) {
            seed = (seed * 0x5DEECE66DULL + 0xBULL) & ((1ULL << 48) - 1);
            return static_cast<int>(static_cast<uint32_t>(seed >> (48 - bits)));
        }
    };

    int length;
    const int SCREEN_WIDTH;
    const int SCREEN_HEIGHT;
    const int BLOCK_SIZE;
    std::vector<Position> positions;
    int score;
    Position foodPosition;
    JavaRandom random;
};

}  // namespace example
}  // namespace org