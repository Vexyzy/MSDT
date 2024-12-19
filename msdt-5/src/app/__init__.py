"""Example work of program."""


from ticket_manager import TicketManager
from train_ticket import TrainTicket

if __name__ == "__main__":
    manager = TicketManager()

    # Добавляем билеты
    manager.add_ticket(TrainTicket(1, "Alice", 100))
    manager.add_ticket(TrainTicket(2, "Bob", 150))
    manager.add_ticket(TrainTicket(3, "Charlie", 200))

    # Выводим все билеты
    print("All tickets:")
    print(manager.list_all_tickets())

    # Обновляем билет
    manager.update_ticket(2, new_passenger_name="Robert", new_price=160)

    # Смотрим обновленный билет
    print("\nUpdated tickets:")
    print(manager.list_all_tickets())

    # Находим билеты по имени пассажира
    print("\nTickets for Alice:")
    print(manager.find_tickets_by_passenger("Alice"))

    # Сортируем билеты по цене
    manager.sort_tickets_by_price()
    print("\nSorted tickets by price:")
    print(manager.list_all_tickets())

    # Получаем общую стоимость всех билетов
    print("\nTotal price of all tickets:")
    print(manager.get_total_price())


    # Получаем общую стоимость всех билетов с учетом скидок
    print("\nTotal value of tickets with discounts:")
    print(manager.total_tickets_value())
