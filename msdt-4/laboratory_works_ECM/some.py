import uuid
import datetime
import random

class Item:
    def __init__(self, name, price, quantity=1):
        self.item_id = str(uuid.uuid4())
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"ID: {self.item_id}, Name: {self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def total_cost(self):
        return self.price * self.quantity


class Order:
    def __init__(self, customer_name, items):
        self.order_id = str(uuid.uuid4())
        self.customer_name = customer_name
        self.items = items
        self.order_date = datetime.datetime.now()
        self.status = "Pending"
        self.shipping_address = None
        self.payment_method = None

    def __str__(self):
        item_details = "\n".join([str(item) for item in self.items])
        return f"Order ID: {self.order_id}\nCustomer: {self.customer_name}\nItems:\n{item_details}\nDate: {self.order_date}\nStatus: {self.status}\nShipping Address: {self.shipping_address}\nPayment Method: {self.payment_method}"

    def set_shipping_address(self, address):
        self.shipping_address = address

    def set_payment_method(self, method):
        self.payment_method = method

    def update_status(self, new_status):
        self.status = new_status

    def calculate_total(self):
        return sum(item.total_cost() for item in self.items)


class OrderManager:
    def __init__(self):
        self.orders = {}  # Use a dictionary for faster lookup by order ID

    def add_order(self, order):
        self.orders[order.order_id] = order

    def get_order_by_id(self, order_id):
        return self.orders.get(order_id)

    def get_all_orders(self):
        return list(self.orders.values()) #return a list of Order objects

    def update_order_status(self, order_id, new_status):
        order = self.get_order_by_id(order_id)
        if order:
            order.update_status(new_status)
            return True
        return False

    def search_orders_by_customer(self, customer_name):
        return [order for order in self.orders.values() if order.customer_name.lower() == customer_name.lower()]

    def get_order_with_highest_total(self):
        if not self.orders:
            return None
        return max(self.orders.values(), key=lambda order: order.calculate_total())


if __name__ == "__main__":
    manager = OrderManager()

    items1 = [Item("Laptop", 1200), Item("Mouse", 25, 2)]
    order1 = Order("Alice", items1)
    order1.set_shipping_address("123 Main St")
    order1.set_payment_method("Credit Card")
    manager.add_order(order1)

    items2 = [Item("Keyboard", 75), Item("Monitor", 300)]
    order2 = Order("Bob", items2)
    manager.add_order(order2)

    print(order1)
    print("\n",order2)
    print(f"\nTotal for order {order1.order_id}: ${order1.calculate_total()}")

    manager.update_order_status(order1.order_id, "Shipped")
    print(f"\nOrder {order1.order_id} updated:")
    print(order1)


    alice_orders = manager.search_orders_by_customer("alice")
    print(f"\nAlice's orders: {[str(order) for order in alice_orders]}")

    highest_total_order = manager.get_order_with_highest_total()
    if highest_total_order:
        print(f"\nOrder with the highest total: \n{highest_total_order}")

    # Add some more orders to increase the code length.
    for i in range(5):
      num_items = random.randint(1,5)
      items = [Item(f"Item {j+1}", random.randint(10,200)) for j in range(num_items)]
      customer_name = f"Customer {i+3}"
      order = Order(customer_name, items)
      manager.add_order(order)

    #Print all order details
    for order in manager.get_all_orders():
        print(f"\n--- Order Details ---\n{order}")