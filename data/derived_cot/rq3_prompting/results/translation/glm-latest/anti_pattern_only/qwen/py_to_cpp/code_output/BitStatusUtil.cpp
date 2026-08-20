#include <initializer_list>
#include <stdexcept>
#include <string>

/**
 * This is a utility class that provides methods for manipulating and
 * checking status using bitwise operations.
 */
class BitStatusUtil {
public:
    /**
     * Add a status to the current status, and check whether the
     * parameters are legal.
     *
     * @param states Current status, int.
     * @param stat   Status to be added, int.
     * @return The status after adding the status, int.
     */
    static long long add(long long states, long long stat) {
        check({states, stat});
        return states | stat;
    }

    /**
     * Check if the current status contains the specified status, and check
     * whether the parameters are legal.
     *
     * @param states Current status, int.
     * @param stat   Specified status, int.
     * @return True if the current status contains the specified status,
     *         otherwise False.
     */
    static bool has(long long states, long long stat) {
        check({states, stat});
        return (states & stat) == stat;
    }

    /**
     * Remove the specified status from the current status, and check
     * whether the parameters are legal.
     *
     * @param states Current status, int.
     * @param stat   Specified status, int.
     * @return The status after removing the specified status, int.
     */
    static long long remove(long long states, long long stat) {
        check({states, stat});
        if (has(states, stat)) {
            return states ^ stat;
        }
        return states;
    }

    /**
     * Check if the parameters are legal: each must be greater than or equal
     * to 0 and must be even; if not, throw std::invalid_argument
     * (the C++ counterpart of Python's ValueError).
     *
     * @param args Parameters to be checked.
     */
    static void check(std::initializer_list<long long> args) {
        for (long long arg : args) {
            if (arg < 0) {
                throw std::invalid_argument(std::to_string(arg) +
                                            " must be greater than or equal to 0");
            }
            if (arg % 2 != 0) {
                throw std::invalid_argument(std::to_string(arg) + " not even");
            }
        }
    }
};