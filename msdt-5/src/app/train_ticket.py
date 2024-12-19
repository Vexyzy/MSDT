"""Class initializing train tickets."""


class TrainTicket:
    """Model of ticket train."""

    def __init__(self, ticket_id: int, passenger_name: str, price: float):
        """Init train ticket.

        Args:
            ticket_id (int): primary if of ticket. Ticket number.
            passenger_name (str): Passenger name who bought the ticket
            price (float): Ticket price

        """
        self.ticket_id = ticket_id
        self.passenger_name = passenger_name
        self.price = price


    def __str__(self):
        """Create some string output and return it, overriding to_str().

        Returns:
            return string

        """
        return  (
            f"Ticket ID: {self.ticket_id}, "
          + f"Passenger: {self.passenger_name}, Price: {self.price}"
        )


