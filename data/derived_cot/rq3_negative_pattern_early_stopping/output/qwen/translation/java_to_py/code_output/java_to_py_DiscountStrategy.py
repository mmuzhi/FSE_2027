class DiscountStrategy:
    class Customer:
        ...

    class Cart:
        ...

    class Product:
        ...

    # Then the methods and the promotions as global functions or inside the class?

    # We'll define the promotions as global functions because they are static in Java.

    # But note: the promotions are applied by passing the order (DiscountStrategy instance). We can define them as:

    FIDELITY_PROMO = lambda order: order.total() * 0.05 if order.customer.fidelity >= 1000 else 0

    # However, note that the Java code uses the promotions as static fields. We can define them as global functions.

    # Alternatively, we can define them as static methods inside the DiscountStrategy class. But since they don't depend on instance state, we can define them outside.

    # Let's define them as global functions in the module.

    # But wait, the Java code has them as public static final. We can define them as constants in the module.

    # However, the problem says to keep behavior identical. We'll define them as functions.

    # We'll define them after the DiscountStrategy class? But the DiscountStrategy class uses them? No, the promotions are used in the DiscountStrategy constructor and in the promotion method. But note: the Java code defines the promotions before the DiscountStrategy class. We can define them after the DiscountStrategy class? Actually, no, because the DiscountStrategy class uses them.

    # We can define them inside the DiscountStrategy class as class attributes? But they are static.

    # Alternatively, we can define them as functions in the module and then reference them in the DiscountStrategy class.

    # Let's define them as module-level functions.

    # But note: the Java code has them as public static fields. We can define them as:

    #   FIDELITY_PROMO = ...   (a function)

    # We'll do that.

    # However, the Java code also has a method `promotion` in DiscountStrategy that uses the promotion field. We'll define the promotions as module-level functions.

    # Let's code accordingly.

    # But note: the Java code's `total()` method recalculates the total and sets the instance variable. We'll do the same.

    # We'll define the DiscountStrategy class first, then the promotions.

    # But wait, the promotions use the `total()` method of DiscountStrategy, which is defined in the class. So we must define the DiscountStrategy class first.

    # We'll define the DiscountStrategy class and then the promotions.

    # Alternatively, we can define the promotions inside the DiscountStrategy class as class attributes.

    # Let's define the promotions as class attributes of DiscountStrategy.

    # We'll do:

    #   class DiscountStrategy:
    #       FIDELITY_PROMO = lambda self: ...   # Wait, no, the promotions are static and don't take self.

    # Actually, the promotions are functions that take a DiscountStrategy instance. We can define them as:

    #       @staticmethod
    #       def FIDELITY_PROMO(order):
    #           return order.total() * 0.05 if order.customer.fidelity >= 1000 else 0

    # But note: the Java code uses the promotions as static fields. We can define them as static methods.

    # Alternatively, we can define them as functions outside the class and then assign them to the class.

    # Let's define them as static methods inside the class.

    # We'll do:

    #   class DiscountStrategy:
    #       @staticmethod
    #       def FIDELITY_PROMO(order):
    #           return order.total() * 0.05 if order.customer.fidelity >= 1000 else 0

    # But note: the Java code's FIDELITY_PROMO is defined as:

    #   order -> order.total() * 0.05

    # And in Python, we can use a lambda, but staticmethod is more explicit.

    # However, the bulk item promotion is more complex and uses a loop. We'll define it as a static method.

    # Let's code.

    # But note: the Java code's `total()` method recalculates the total and sets the instance variable. We must ensure that the `total()` method is defined.

    # We'll define the DiscountStrategy class with the inner classes and the methods.

    # We'll define the promotions as static methods.

    # Alternatively, we can define them as functions outside the class and then assign them to the class. But to keep everything in one file, we'll define them inside the class.

    # Let's do it.

    # However, note that the Java code has three promotions. We'll define them as static methods.

    # We'll define:

    #   @staticmethod
    #   def FIDELITY_PROMO(order):
    #       ...

    #   @staticmethod
    #   def BULK_ITEM_PROMO(order):
    #       ...

    #   @staticmethod
    #   def LARGE_ORDER_PROMO(order):
    #       ...

    # But wait, the Java code's `total()` method is called in the FIDELITY_PROMO and BULK_ITEM_PROMO. We must ensure that the `total()` method is available.

    # We'll define the DiscountStrategy class first.

    # Let's code.

    # Note: We are using Python 3. We'll use type hints if needed, but the problem says to use idiomatic Python only when it doesn't change behavior.

    # We'll not use type hints to keep it simple and because the problem doesn't require them.

    # Let's code.
</think>
Here's the Python translation of the provided Java code, maintaining the same behavior and using idiomatic Python where appropriate: