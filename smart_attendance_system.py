def mark_attendance(student_id, date, status):
    if student_id not in students:
        print(f"Student ID '{student_id}' not found.")
        return
    if date in CLASS_CANCELLED_DATES:
        print(f"Class was cancelled on {date} ({CLASS_CANCELLED_DATES[date]}). No attendance recorded.")
        return
    status = status.lower()
    if status not in ["present", "absent"]:
        print("Status must be 'present' or 'absent'.")
        return
    attendance[student_id][date] = status
    print(f"Marked {students[student_id]['name']} as {status} on {date}.")


def get_summary(student_id):
    if student_id not in students:
        print(f"Student ID '{student_id}' not found.")
        return None
    records = attendance[student_id]
    total = len(records)
    present = sum(1 for s in records.values() if s == "present")
    absent = total - present
    return {"name": students[student_id]["name"], "present": present, "absent": absent, "total": total}


def print_all_summaries():
    print(f"\n{'Student':<22}{'Present':<10}{'Absent':<10}{'Total':<10}")
    print("-" * 52)
    for sid in students:
        summary = get_summary(sid)
        print(f"{summary['name']:<22}{summary['present']:<10}{summary['absent']:<10}{summary['total']:<10}")


def print_student_detail(student_id):
    if student_id not in students:
        print(f"Student ID '{student_id}' not found.")
        return
    name = students[student_id]["name"]
    print(f"\nAttendance detail for {name} (ID: {student_id}):")
    for date in sorted(attendance[student_id].keys()):
        status = attendance[student_id][date]
        marker = "✓" if status == "present" else "✗"
        print(f"  {date}: {marker} {status}")


def list_cancelled_classes():
    print("\nCancelled class sessions:")
    for date, reason in sorted(CLASS_CANCELLED_DATES.items()):
        print(f"  {date}: {reason}")


# ─────────────────────────────────────────────────────────────
# NEW: ABSENCE PATTERN ANALYSIS
# ─────────────────────────────────────────────────────────────

def get_weekday_absence_pattern(student_id):
    """
    Returns a dict {weekday_name: absence_count} showing which days
    of the week a student tends to miss class on.
    """
    if student_id not in attendance:
        return {}
    pattern = {}
    for date_str, status in attendance[student_id].items():
        if status != "absent":
            continue
        weekday = datetime.strptime(date_str, "%Y-%m-%d").strftime("%A")
        pattern[weekday] = pattern.get(weekday, 0) + 1
    return pattern


def most_missed_weekday(student_id):
    pattern = get_weekday_absence_pattern(student_id)
    if not pattern:
        return None
    return max(pattern, key=pattern.get)


def print_absence_patterns():
    print("\n=== Absence Pattern by Weekday ===")
    for sid in students:
        missed_day = most_missed_weekday(sid)
        name = students[sid]["name"]
        if missed_day:
            print(f"  {name:<22} tends to miss {missed_day}s")
        else:
            print(f"  {name:<22} no absences recorded")


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
    print_absence_patterns()

    print_student_detail("1001")
    list_cancelled_classes()

    # demonstrate adding a new attendance record
    print()
    mark_attendance("1003", "2026-07-27", "present")

    # demonstrate that cancelled days are protected
    print()
    mark_attendance("1001", "2026-07-16", "present")


if ــnameــ" ==  ــmainــ":
    main()
