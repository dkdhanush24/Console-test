"""
main.py
-------
Entry point for the IT Support Ticket System (Sprint 1).

Roles
-----
  Employee   – raise tickets only
  IT Support – view / update tickets, view statistics
  Admin      – view users, view tickets, view statistics

Run with:
    python main.py
"""

import getpass
import database
import ticket as ticket_module
import statistics as stats_module
from ticket import STATUS_OPTIONS


# ─────────────────────────────────────────────────────────────────────────────
#  Shared display helpers
# ─────────────────────────────────────────────────────────────────────────────

def banner(title: str):
    print("\n========================================")
    print(f"  {title}")
    print("========================================\n")


def separator():
    print("  " + "-" * 56)


def pause():
    input("\n  Press Enter to continue...")


# ─────────────────────────────────────────────────────────────────────────────
#  Login
# ─────────────────────────────────────────────────────────────────────────────

def login() -> dict:
    """
    Prompt for credentials and return the authenticated user dict.
    Loops until a valid login is provided.
    """
    while True:
        banner("IT SUPPORT TICKET SYSTEM")
        username = input("  Username: ").strip()
        password = getpass.getpass("  Password: ")

        user = database.authenticate_user(username, password)

        if user:
            print(f"\n  Login successful.\n")
            print(f"  Role: {user['role']}")
            pause()
            return user
        else:
            print("\n  Invalid username or password.")
            print("  Please try again.\n")


# ─────────────────────────────────────────────────────────────────────────────
#  Common ticket actions (shared by IT Support and Admin)
# ─────────────────────────────────────────────────────────────────────────────

def handle_view_all_tickets():
    rows = database.get_all_tickets()

    banner("ALL TICKETS")

    if not rows:
        print("  No tickets found.\n")
        return

    header = (
        f"  {'ID':<10} {'Employee':<12} {'Category':<22} {'Priority':<10} {'Status'}"
    )
    print(header)
    print("  " + "-" * 68)

    for row in rows:
        print(
            f"  {row['ticket_id']:<10} "
            f"{row['employee_username']:<12} "
            f"{row['category']:<22} "
            f"{row['priority']:<10} "
            f"{row['status']}"
        )
    print()
    pause()


def handle_view_ticket():
    ticket_id = input("\n  Enter Ticket ID: ").strip()
    t = database.get_ticket_by_id(ticket_id)

    if not t:
        print(f"\n  [!] Ticket '{ticket_id.upper()}' not found.\n")
        pause()
        return

    resolved = t["resolved_at"] if t["resolved_at"] else "Not resolved"

    print("\n  ----------------------------------------")
    print(f"  Ticket ID   : {t['ticket_id']}")
    print(f"  Employee    : {t['employee_username']}")
    print(f"  Description : {t['description']}")
    print(f"  Category    : {t['category']}")
    print(f"  Priority    : {t['priority']}")
    print(f"  Status      : {t['status']}")
    print(f"  Created     : {t['created_at']}")
    print(f"  Resolved    : {resolved}")
    print("  ----------------------------------------\n")
    pause()


def handle_statistics():
    print("\n  View statistics for:")
    print("    1. All categories")
    print("    2. Specific category")
    sub = input("\n  Enter choice: ").strip()

    if sub == "1":
        print(stats_module.display_all_statistics())
        pause()

    elif sub == "2":
        print("\n  Available categories:")
        rows = database.get_all_statistics()
        for i, row in enumerate(rows, start=1):
            print(f"    {i}. {row['category']}")

        cat_choice = input("\n  Enter category number: ").strip()
        if cat_choice.isdigit():
            idx = int(cat_choice) - 1
            if 0 <= idx < len(rows):
                category = rows[idx]["category"]
                print(stats_module.display_category_statistics(category))
                pause()
            else:
                print("  [!] Invalid selection.\n")
        else:
            print("  [!] Invalid input.\n")
    else:
        print("  [!] Invalid choice.\n")


# ─────────────────────────────────────────────────────────────────────────────
#  Employee portal
# ─────────────────────────────────────────────────────────────────────────────

def employee_menu(user: dict):
    """Main loop for Employee role."""
    while True:
        banner("EMPLOYEE PORTAL")
        print(f"  Welcome, {user['username'].capitalize()}\n")
        print("  1. Raise a Ticket")
        print("  2. Exit\n")

        choice = input("  Enter your choice: ").strip()

        if choice == "1":
            _handle_raise_ticket(user)
        elif choice == "2":
            print("\n  Goodbye! Exiting IT Support Ticket System.\n")
            break
        else:
            print("\n  [!] Invalid choice. Please enter 1 or 2.\n")


def _handle_raise_ticket(user: dict):
    print("\n  Describe your issue:")
    description = input("  > ").strip()

    if not description:
        print("  [!] No description entered. Returning to menu.\n")
        return

    print("\n  Analyzing issue...\n")
    ticket = ticket_module.create_ticket(user["username"], description)

    print(f"  Detected category : {ticket['category']}")
    print(f"  Priority          : {ticket['priority']}")
    print(ticket_module.format_ticket_created(ticket))
    pause()


# ─────────────────────────────────────────────────────────────────────────────
#  IT Support portal
# ─────────────────────────────────────────────────────────────────────────────

def support_menu(user: dict):
    """Main loop for IT Support role."""
    while True:
        banner("IT SUPPORT PORTAL")
        print(f"  Welcome, {user['username']}\n")
        print("  1. View All Tickets")
        print("  2. View Ticket")
        print("  3. Update Ticket")
        print("  4. View Issue Statistics")
        print("  5. Exit\n")

        choice = input("  Enter your choice: ").strip()

        if choice == "1":
            handle_view_all_tickets()
        elif choice == "2":
            handle_view_ticket()
        elif choice == "3":
            _handle_update_ticket()
        elif choice == "4":
            handle_statistics()
        elif choice == "5":
            print("\n  Goodbye! Exiting IT Support Ticket System.\n")
            break
        else:
            print("\n  [!] Invalid choice. Please enter a number between 1 and 5.\n")


def _handle_update_ticket():
    ticket_id = input("\n  Enter Ticket ID: ").strip()
    t = database.get_ticket_by_id(ticket_id)

    if not t:
        print(f"\n  [!] Ticket '{ticket_id.upper()}' not found.\n")
        pause()
        return

    print(f"\n  Current Status: {t['status']}\n")
    print("  Select New Status:\n")
    for key, value in STATUS_OPTIONS.items():
        print(f"    {key}. {value}")

    choice = input("\n  Enter choice: ").strip()

    if choice not in STATUS_OPTIONS:
        print("  [!] Invalid choice. No changes made.\n")
        pause()
        return

    new_status = STATUS_OPTIONS[choice]
    success = database.update_ticket_status(ticket_id, new_status)

    if success:
        print(f"\n  Ticket {ticket_id.upper()} has been marked as {new_status}.\n")
    else:
        print("  [!] Update failed. Please try again.\n")
    pause()


# ─────────────────────────────────────────────────────────────────────────────
#  Admin portal
# ─────────────────────────────────────────────────────────────────────────────

def admin_menu(user: dict):
    """Main loop for Admin role."""
    while True:
        banner("ADMIN PORTAL")
        print(f"  Welcome, {user['username']}\n")
        print("  1. View All Users")
        print("  2. View All Tickets")
        print("  3. View Ticket")
        print("  4. View Issue Statistics")
        print("  5. Exit\n")

        choice = input("  Enter your choice: ").strip()

        if choice == "1":
            _handle_view_users()
        elif choice == "2":
            handle_view_all_tickets()
        elif choice == "3":
            handle_view_ticket()
        elif choice == "4":
            handle_statistics()
        elif choice == "5":
            print("\n  Goodbye! Exiting IT Support Ticket System.\n")
            break
        else:
            print("\n  [!] Invalid choice. Please enter a number between 1 and 5.\n")


def _handle_view_users():
    rows = database.get_all_users()

    banner("USERS")

    if not rows:
        print("  No users found.\n")
        pause()
        return

    print(f"  {'Username':<15} {'Role'}")
    print("  " + "-" * 30)
    for row in rows:
        print(f"  {row['username']:<15} {row['role']}")
    print()
    pause()


# ─────────────────────────────────────────────────────────────────────────────
#  Main entry point
# ─────────────────────────────────────────────────────────────────────────────

ROLE_MENUS = {
    "Employee":   employee_menu,
    "IT Support": support_menu,
    "Admin":      admin_menu,
}


def main():
    database.initialize_database()

    user = login()
    role = user["role"]

    menu_fn = ROLE_MENUS.get(role)
    if menu_fn:
        menu_fn(user)
    else:
        print(f"\n  [!] Unknown role '{role}'. Contact your administrator.\n")


if __name__ == "__main__":
    main()
