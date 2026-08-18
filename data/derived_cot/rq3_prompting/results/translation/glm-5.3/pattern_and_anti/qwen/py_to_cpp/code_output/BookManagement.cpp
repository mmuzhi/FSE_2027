#include <map>
#include <string>
#include <stdexcept>

/**
 * This is a class as managing books system, which supports to add and remove
 * books from the inventory dict, view the inventory, and check the quantity
 * of a specific book.
 */
class BookManagement {
public:
    /**
     * Initialize the inventory of Book Manager.
     */
    BookManagement() : inventory() {}

    /**
     * Add one or several books to inventory which is sorted by book title.
     * @param title   the book title
     * @param quantity int, default value is 1.
     */
    void add_book(const std::string& title, int quantity = 1) {
        auto it = inventory.find(title);
        if (it != inventory.end()) {
            it->second += quantity;
        } else {
            inventory[title] = quantity;
        }
    }

    /**
     * Remove one or several books from inventory which is sorted by book title.
     * Raise while getting invalid input.
     * @param title   the book title
     * @param quantity int
     */
    void remove_book(const std::string& title, int quantity) {
        auto it = inventory.find(title);
        if (it == inventory.end() || it->second < quantity) {
            throw std::invalid_argument("False");
        }
        it->second -= quantity;
        if (it->second == 0) {
            inventory.erase(it);
        }
    }

    /**
     * Get the inventory of the Book Management.
     * @return self.inventory: map, {title(str): quantity(int), ...}
     */
    std::map<std::string, int>& view_inventory() {
        return inventory;
    }

    /**
     * Get the quantity of a book.
     * @param title the title of the book.
     * @return the quantity of this book title; return 0 when the title
     *         does not exist in the inventory.
     */
    int view_book_quantity(const std::string& title) const {
        auto it = inventory.find(title);
        if (it == inventory.end()) {
            return 0;
        }
        return it->second;
    }

private:
    std::map<std::string, int> inventory;
};