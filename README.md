# IT Support Ticket System

A console-based IT support ticket management system built with Python and SQLite.

## Features

- **Employee** – raise support tickets; issues are auto-categorised and prioritised
- **IT Support** – view, update, and manage all tickets; view issue statistics
- **Admin** – view all users, tickets, and statistics

## Requirements

- Python 3.8 or higher
- No third-party packages needed (uses stdlib only)

## Installation & Running

```bash
# 1. Clone the repository
git clone <repo-url>
cd "Console Based Application"

# 2. (Optional but recommended) Create a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies (none required, but good habit)
pip install -r requirements.txt

# 4. Run the app
python main.py
```

## Default Login Credentials

| Username  | Password      | Role       |
|-----------|---------------|------------|
| john      | employee123   | Employee   |
| alice     | employee123   | Employee   |
| support1  | support123    | IT Support |
| support2  | support123    | IT Support |
| admin     | admin123      | Admin      |

## Project Structure

```
.
├── main.py          # Entry point & role-based menus
├── database.py      # SQLite persistence layer
├── ticket.py        # Ticket creation & formatting
├── classifier.py    # Keyword-based issue categorisation & priority detection
├── statistics.py    # Historical statistics & recurrence probability
├── requirements.txt # Dependencies (stdlib only)
└── .gitignore
```

> **Note:** `tickets.db` is excluded from version control. It is created automatically on first run.
