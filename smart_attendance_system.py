def calculate_risk_score(student_id):
    """
    Produces a 0-100 'absence risk' score for a student using two signals:
      1. overall_absence_rate  - absences over the whole recorded history
      2. recent_absence_rate   - absences over just the last RECENT_WINDOW sessions

    recent_absence_rate is weighted more heavily (70%) than the overall
    rate (30%) so a student who is slipping lately scores higher than
    their long-term average would suggest. This is a transparent,
    explainable heuristic — not a trained statistical model.
    """
    if student_id not in attendance:
        return None

    records = attendance[student_id]
    if not records:
        return 0

    dates_sorted = sorted(records.keys())
    total = len(dates_sorted)
    total_absences = sum(1 for d in dates_sorted if records[d] == "absent")
    overall_rate = total_absences / total

    recent_dates = dates_sorted[-RECENT_WINDOW:]
    recent_absences = sum(1 for d in recent_dates if records[d] == "absent")
    recent_rate = recent_absences / len(recent_dates)

    score = (0.3 * overall_rate + 0.7 * recent_rate) * 100
    return round(score, 1)


def risk_level(score):
    if score is None:
        return "Unknown"
    if score >= RISK_HIGH:
        return "High"
    if score >= RISK_MEDIUM:
        return "Medium"
    return "Low"


def get_at_risk_students():
    """Returns list of (student_id, name, score, level) sorted by score descending."""
    results = []
    for sid in students:
        score = calculate_risk_score(sid)
        level = risk_level(score)
        results.append((sid, students[sid]["name"], score, level))
    results.sort(key=lambda x: x[2], reverse=True)
    return results


def print_risk_report():
    print(f"\n{'Student':<22}{'Risk Score':<14}{'Level':<10}{'Most Missed Day':<18}")
    print("-" * 64)
    for sid, name, score, level in get_at_risk_students():
        missed_day = most_missed_weekday(sid) or "-"
        marker = " ⚠" if level == "High" else ""
        print(f"{name:<22}{score:<14}{level:<10}{missed_day:<18}{marker}")


def print_alerts():
    """Prints one-line alerts for students at Medium or High risk."""
    at_risk = [r for r in get_at_risk_students() if r[3] in ("Medium", "High")]
    print("\n=== Attendance Alerts ===")
    if not at_risk:
        print("  No students currently at risk. ✓")
        return
    for sid, name, score, level in at_risk:
        missed_day = most_missed_weekday(sid)
        tip = f" — tends to miss {missed_day}s." if missed_day else ""
        icon = "🔴" if level == "High" else "🟡"
        print(f"  {icon} {name}: {level} risk ({score}/100).{tip}")


# ─────────────────────────────────────────────────────────────
# NEW: SIMPLE TEXT-BASED ATTENDANCE CHART
# ─────────────────────────────────────────────────────────────

def print_attendance_chart():
    """
    Prints a simple horizontal bar chart (using block characters) showing
    each student's attendance rate. Kept as plain text so it works in
    any terminal, without needing a plotting library.
    """
    print("\n=== Attendance Rate Chart ===")
    bar_width = 40
    for sid in students:
        summary = get_summary(sid)
        rate = summary["present"] / summary["total"] if summary["total"] else 0
        filled = round(rate * bar_width)
        bar = "█" * filled + "░" * (bar_width - filled)
        print(f"  {summary['name']:<18} [{bar}] {rate*100:5.1f}%")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    print("=== Smart Attendance System ===")
    print("Class schedule: Saturday to Thursday, 10:00–12:00\n")

    print("Registered students:")
    for sid, info in students.items():
        print(f"  {sid}: {info['name']} ({info['gender']})")

    print_all_summaries()
    print_attendance_chart()
    print_absence_patterns()
    print_risk_report()
    print_alerts()

    print_student_detail("1001")
    list_cancelled_classes()


# demonstrate adding a new attendance record
    print()
    mark_attendance("1003", "2026-07-27", "present")

    # demonstrate that cancelled days are protected
    print()
    mark_attendance("1001", "2026-07-16", "present")


if ــname__ == "__main__":
    main()
