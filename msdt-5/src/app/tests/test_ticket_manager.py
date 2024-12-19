import pytest
from ..train_ticket import TrainTicket
from ..ticket_manager import TicketManager


def test_create_train_ticket():
    ticket = TrainTicket(ticket_id=1, passenger_name="John Doe", price=100.0)
    assert ticket.ticket_id == 1
    assert ticket.passenger_name == "John Doe"
    assert ticket.price == 100.0


def test_ticket_str_method():
    ticket = TrainTicket(ticket_id=2, passenger_name="Jane Doe", price=150.0)
    assert str(ticket) == "Ticket ID: 2, Passenger: Jane Doe, Price: 150.0"


def test_add_ticket():
    manager = TicketManager()
    ticket = TrainTicket(ticket_id=3, passenger_name="Alice", price=200.0)
    manager.add_ticket(ticket)
    assert len(manager.tickets) == 1
    assert manager.tickets[0] == ticket


def test_add_invalid_ticket():
    manager = TicketManager()
    with pytest.raises(ValueError) as error:
        manager.add_ticket("Invalid Ticket")
    assert str(error.value) == "Only TrainTicket instances can be added."


def test_list_all_tickets():
    manager = TicketManager()
    ticket1 = TrainTicket(ticket_id=4, passenger_name="Bob", price=250.0)
    ticket2 = TrainTicket(ticket_id=5, passenger_name="Charlie", price=300.0)
    manager.add_ticket(ticket1)
    manager.add_ticket(ticket2)

    expected_output = [
        "Ticket ID: 4, Passenger: Bob, Price: 250.0",
        "Ticket ID: 5, Passenger: Charlie, Price: 300.0"
    ]

    assert manager.list_all_tickets() == expected_output
