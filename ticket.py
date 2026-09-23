"""
ticket.py
---------
Ticket creation logic and ticket-related helper functions.
"""

import database


def create_ticket(employee_username: str, description: str) -> dict:
    """
    Full ticket creation pipeline:
      1. Classify the issue (category + priority).
      2. Generate a unique ticket ID.
      3. Persist to SQLite (with the employee's username).
      4. Return the ticket data dict.
    """
    from classifier import classify_issue

    result = classify_issue(description)
    category = result["category"]
    priority = result["priority"]
    detected_keywords = result["detected_keywords"]

    ticket_id = database.get_next_ticket_id()
    database.insert_ticket(ticket_id, employee_username, description, category, priority)

    return {
        "ticket_id": ticket_id,
        "employee_username": employee_username,
        "description": description,
        "category": category,
        "priority": priority,
        "status": "Open",
        "detected_keywords": detected_keywords,
    }


def format_ticket_created(ticket: dict) -> str:
    """Return a formatted string for a newly created ticket."""
    return (
        "\n----------------------------------------\n"
        "           TICKET CREATED\n"
        "----------------------------------------\n\n"
        f"  Ticket ID   : {ticket['ticket_id']}\n"
        f"  Employee    : {ticket['employee_username']}\n"
        f"  Issue       : {ticket['description']}\n"
        f"  Category    : {ticket['category']}\n"
        f"  Priority    : {ticket['priority']}\n"
        f"  Status      : {ticket['status']}\n\n"
        "  Your ticket has been submitted.\n"
        "----------------------------------------\n"
    )


STATUS_OPTIONS = {
    "1": "Open",
    "2": "In Progress",
    "3": "Resolved",
    "4": "Closed",
}
