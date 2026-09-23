"""
statistics.py
-------------
Historical statistics display and recurrence probability calculation.
Uses pre-seeded fake data from the issue_statistics table (Sprint 1).
This is NOT a machine-learning prediction.
"""

import database


def calculate_recurrence_probability(previous_occurrences: int, recurring_cases: int) -> float:
    """Return recurrence probability as a percentage (0.0 if no data)."""
    if previous_occurrences == 0:
        return 0.0
    return round((recurring_cases / previous_occurrences) * 100, 2)


def display_all_statistics() -> str:
    """Return a formatted string of statistics for all categories."""
    rows = database.get_all_statistics()
    if not rows:
        return "No statistics data available."

    lines = [
        "\n========================================",
        "          ISSUE STATISTICS",
        "========================================\n",
    ]

    for row in rows:
        prob = calculate_recurrence_probability(
            row["previous_occurrences"], row["recurring_cases"]
        )
        lines += [
            f"  Category             : {row['category']}",
            f"  Previous Occurrences : {row['previous_occurrences']}",
            f"  Recurring Cases      : {row['recurring_cases']}",
            f"  Recurrence Probability: {prob}%",
            "  ----------------------------------------",
        ]

    lines.append("")
    return "\n".join(lines)


def display_category_statistics(category: str) -> str:
    """Return a formatted string of statistics for a single category."""
    row = database.get_statistics_by_category(category)
    if not row:
        return f"No statistics found for category: {category}"

    prob = calculate_recurrence_probability(
        row["previous_occurrences"], row["recurring_cases"]
    )

    return (
        "\n========================================\n"
        "          ISSUE STATISTICS\n"
        "========================================\n\n"
        f"  Category              : {row['category']}\n"
        f"  Previous Occurrences  : {row['previous_occurrences']}\n"
        f"  Recurring Cases       : {row['recurring_cases']}\n"
        f"  Recurrence Probability: {prob}%\n\n"
        "========================================\n"
    )
