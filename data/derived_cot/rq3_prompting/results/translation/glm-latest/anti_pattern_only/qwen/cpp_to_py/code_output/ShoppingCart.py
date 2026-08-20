class ShoppingCart:
    def __init__(self) -> None:
        # Maps item name -> (price, quantity), mirroring
        # std::unordered_map<std::string, std::pair<double, int>>
        self._items: dict[str, tuple[float, int]] = {}

    def add_item(self, item: str, price: float, quantity: int = 1) -> None:
        # Both branches of the original if/else assign the same value,
        # so an existing entry is overwritten (not accumulated).
        self._items[item] = (price, quantity)

    def remove_item(self, item: str, quantity: int = 1) -> None:
        # Missing items are silently ignored, as in the C++ version.
        if item in self._items:
            price, qty = self._items[item]
            qty -= quantity
            if qty <= 0:
                del self._items[item]
            else:
                self._items[item] = (price, qty)

    def view_items(self) -> dict[str, tuple[float, int]]:
        # C++ returns the map by value (a copy); return a copy here too.
        # Tuples are immutable, so a shallow dict copy matches that semantics.
        return dict(self._items)

    def total_price(self) -> float:
        total = 0.0
        for price, quantity in self._items.values():
            total += price * quantity
        return total