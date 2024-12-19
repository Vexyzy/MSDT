"""Module use to ticket managing."""

from .train_ticket import TrainTicket

class TicketManager:
    """Initialize model of ticket manager."""

    def __init__(self):
        """Initialize list of tickets."""
        self.tickets = []

    def add_ticket(self, ticket: TrainTicket):
        """Добавляет билет в систему."""
        self.tickets.append(ticket)

    def remove_ticket(self, ticket_id):
        """Удаляет билет по ID."""
        self.tickets = [
            ticket for ticket
            in self.tickets
            if ticket.ticket_id != ticket_id
        ]

    def update_ticket(self, ticket_id, new_passenger_name=None, new_price=None):
        """Обновляет информацию о билете по ID."""
        ticket = self.find_ticket_by_id(ticket_id)
        if ticket:
            if new_passenger_name is not None:
                ticket.passenger_name = new_passenger_name
            if new_price is not None:
                ticket.price = new_price
        else:
            raise ValueError("Ticket not found.")

    def get_total_price(self):
        """Возвращает общую стоимость всех билетов."""
        return sum(ticket.price for ticket in self.tickets)

    def find_ticket_by_id(self, ticket_id):
        """Находит билет по ID."""
        for ticket in self.tickets:
            if ticket.ticket_id == ticket_id:
                return ticket
        return None

    def find_tickets_by_passenger(self, passenger_name):
        """Находит все билеты по имени пассажира."""
        return [
            ticket for ticket
            in self.tickets
            if ticket.passenger_name.lower() == passenger_name.lower()
        ]

    def get_ticket_count(self):
        """Возвращает количество билетов в системе."""
        return len(self.tickets)

    def clear_tickets(self):
        """Очищает список билетов."""
        self.tickets.clear()

    def calculate_discounted_price(
        self,
        ticket: TrainTicket,
        discount_percentage: float
        ):
        """Рассчитывает цену со скидкой."""
        if discount_percentage < 0 or discount_percentage > 100:
            raise ValueError("Discount percentage must be between 0 and 100.")
        return ticket.price * (1 - discount_percentage / 100)

    def list_all_tickets(self):
        """Возвращает список всех билетов."""
        return [str(ticket) for ticket in self.tickets]

    def sort_tickets_by_price(self):
        """Сортирует билеты по цене."""
        self.tickets.sort(key=lambda x: x.price)

    def total_tickets_value(self):
        """Возвращает общую стоимость всех билетов с учетом скидок."""
        total_value = 0
        for ticket in self.tickets:
            # Применяем скидку 10%
            total_value += self.calculate_discounted_price(ticket, 10)
        return total_value
