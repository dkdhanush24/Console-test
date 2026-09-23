# IT Support Ticket Recognition System
## Sprint 1 — Console-Based Prototype

A console application built with **Python 3** and **SQLite** that demonstrates the complete IT support ticket lifecycle.

---

## Project Structure

`
Console Based Application/
├── main.py          # Entry point — main menu and user interaction
├── database.py      # SQLite operations (create, read, update tables)
├── ticket.py        # Ticket creation pipeline and formatting helpers
├── classifier.py    # Keyword-based issue categorisation and priority
├── statistics.py    # Historical statistics and recurrence probability
├── tickets.db       # SQLite database (auto-created on first run)
└── README.md        # This file
`

---

## How to Run

`ash
python main.py
`

No external packages required. Python 3 standard library only.

---

## Features (Sprint 1)

| Feature | Details |
|---|---|
| Issue categorisation | Keyword matching across 6 categories |
| Priority assignment | Rule-based (High / Medium / Low) |
| Unique ticket IDs | Auto-generated (TKT1001, TKT1002, …) |
| SQLite storage | Persistent 	ickets.db file |
| View all tickets | Tabular listing with ID, category, priority, status |
| View individual ticket | Full details including timestamps |
| Update ticket status | Open → In Progress → Resolved → Closed |
| Historical statistics | Pre-seeded fake data for 7 categories |
| Recurrence probability | Recurring Cases / Previous Occurrences × 100 |

---

## Issue Categories

| Category | Example Keywords |
|---|---|
| WiFi Connectivity | wifi, internet, network, connection |
| Password/Login | password, login, sign in, credentials |
| Email Problem | email, outlook, mail |
| Printer Problem | printer, printing, print |
| Software Problem | software, application, app, crash |
| Hardware Problem | laptop, keyboard, mouse, screen |
| Unknown | anything that does not match |

---

## Priority Rules

| Priority | Triggered By |
|---|---|
| High | server, system down, critical, security, outage |
| Medium | wifi, email, printer, software, network |
| Low | mouse, keyboard, slow, display, battery |

---

## Example Session

`
========================================
       IT SUPPORT TICKET SYSTEM
========================================

  1. Raise a Ticket
  2. View All Tickets
  3. View Ticket
  4. Update Ticket
  5. View Issue Statistics
  6. Exit

  Enter your choice: 1

Describe your issue:
  > My laptop is not connecting to WiFi

  Analyzing issue...

  Category detected : WiFi Connectivity
  Priority          : Medium

----------------------------------------
           TICKET CREATED
----------------------------------------

Ticket ID   : TKT1001
Description : My laptop is not connecting to WiFi
Category    : WiFi Connectivity
Keywords    : wifi, connecting
Priority    : Medium
Status      : Open

----------------------------------------

  Ticket saved successfully.
`

---

## Sprint Roadmap

| Sprint | Focus |
|---|---|
| Sprint 1 ✅ | Console prototype, keyword matching, SQLite |
| Sprint 2 | Chatbot interface |
| Sprint 3 | NLP / ML-based classification |
| Sprint 4 | Database server + IT support dashboard |
| Sprint 5 | Predictive analytics with real ML model |

---

## Notes

- The recurrence probability shown in Sprint 1 is a **historical frequency ratio**, not a genuine predictive AI model.
- The issue_statistics table is pre-seeded with fake historical data on first run.
- 	ickets.db is created automatically in the same directory as main.py.
