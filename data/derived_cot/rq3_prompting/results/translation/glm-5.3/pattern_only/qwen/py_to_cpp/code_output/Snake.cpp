#include <cmath>
#include <cstddef>
#include <ctime>
#include <list>
#include <random>
#include <stdexcept>
#include <utility>

class Snake {
public:
    using Position = std::pair<double, double>;

    Snake(int screenWidth, int screenHeight, int blockSize,
          const Position &foodPosition)
        : SCREEN_WIDTH(screenWidth),
          SCREEN_HEIGHT(screenHeight),
          BLOCK_SIZE(blockSize),
          food_position(foodPosition),
          length(1),
          score(0) {
        // Python's SCREEN_WIDTH / 2 is true (float) division.
        positions.push_back(Position(SCREEN_WIDTH / 2.0, SCREEN_HEIGHT / 2.0));
    }

    void move(const Position &direction) {
        const Position &cur = positions.front();
        const double x = direction.first;
        const double y = direction.second;

        const Position newPosition(
            pythonMod(cur.first + x * BLOCK_SIZE, SCREEN_WIDTH),
            pythonMod(cur.second + y * BLOCK_SIZE, SCREEN_HEIGHT));

        if (newPosition == food_position) {
            eat_food();
        }

        // Python: new in self.positions[2:] (head and neck cells don't count)
        if (positions.size() > 2 && containsFrom(newPosition, 2)) {
            reset();
        } else {
            positions.push_front(newPosition);
            if (positions.size() > static_cast<std::size_t>(length)) {
                positions.pop_back();
            }
        }
    }

    void random_food_position() {
        while (containsFrom(food_position, 0)) {
            const int rx = randint(0, floorDiv(SCREEN_WIDTH, BLOCK_SIZE) - 1);
            const int ry = randint(0, floorDiv(SCREEN_HEIGHT, BLOCK_SIZE) - 1);
            food_position = Position(rx * BLOCK_SIZE, ry * BLOCK_SIZE);
        }
    }

    void reset() {
        length = 1;
        positions.clear();
        positions.push_back(Position(SCREEN_WIDTH / 2.0, SCREEN_HEIGHT / 2.0));
        score = 0;
        random_food_position();
    }

    void eat_food() {
        length += 1;
        score += 100;
        random_food_position();
    }

    // State kept public to mirror Python attribute access.
    const int SCREEN_WIDTH;
    const int SCREEN_HEIGHT;
    const int BLOCK_SIZE;
    Position food_position;
    int length;
    std::list<Position> positions;  // head at front, mirrors Python list
    int score;

private:
    // Python's % yields a result with the sign of the divisor
    // (wrap-around), unlike std::fmod which takes the dividend's sign.
    static double pythonMod(double value, double modulus) {
        double r = std::fmod(value, modulus);
        if (r < 0.0) {
            r += modulus;
        }
        return r;
    }

    // Python's // is floor division; C++ / truncates.
    static int floorDiv(int a, int b) {
        int q = a / b;
        if ((a % b != 0) && ((a < 0) != (b < 0))) {
            --q;
        }
        return q;
    }

    // Equivalent of random.randint(lo, hi): inclusive on both ends;
    // raises (like ValueError) when the range is empty.
    static int randint(int lo, int hi) {
        if (hi < lo) {
            throw std::invalid_argument("empty range for randint()");
        }
        static std::mt19937 rng(static_cast<std::mt19937::result_type>(std::time(nullptr)));
        std::uniform_int_distribution<int> dist(lo, hi);
        return dist(rng);
    }

    // True if `target` equals any stored position at index >= fromIndex.
    bool containsFrom(const Position &target, std::size_t fromIndex) const {
        std::size_t i = 0;
        for (const Position &p : positions) {
            if (i >= fromIndex && p == target) {
                return true;
            }
            ++i;
        }
        return false;
    }
};