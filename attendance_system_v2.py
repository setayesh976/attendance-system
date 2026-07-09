students = {
    "1001": {"name": "Aria Rostami", "gender": "Male"},
    "1002": {"name": "Parsa Mohammadi", "gender": "Male"},
    "1003": {"name": "Ava Naderi", "gender": "Female"},
    "1004": {"name": "Yasna Hosseini", "gender": "Female"},
    "1005": {"name": "Tarannom Rahimi", "gender": "Female"},
}

# Attendance records: student_id -> {date: status}
# Status: "present" or "absent"
attendance = {
    "1001": {
        "2026-06-30": "present", "2026-07-01": "absent", "2026-07-03": "present",
        "2026-07-05": "present", "2026-07-07": "present", "2026-07-09": "present",
        "2026-07-11": "present", "2026-07-13": "present", "2026-07-15": "present",
        "2026-07-17": "present", "2026-07-19": "absent", "2026-07-21": "present",
        "2026-07-23": "present", "2026-07-25": "present",
    },
    "1002": {
        "2026-06-30": "present", "2026-07-01": "present", "2026-07-03": "present",
        "2026-07-05": "present", "2026-07-07": "absent", "2026-07-09": "present",
        "2026-07-11": "present", "2026-07-13": "absent", "2026-07-15": "present",
        "2026-07-17": "present", "2026-07-19": "present", "2026-07-21": "present",
        "2026-07-23": "absent", "2026-07-25": "present",
    },
    "1003": {
        "2026-06-30": "present", "2026-07-01": "present", "2026-07-03": "present",
        "2026-07-05": "present", "2026-07-07": "present", "2026-07-09": "present",
        "2026-07-11": "present", "2026-07-13": "present", "2026-07-15": "present",
        "2026-07-17": "present", "2026-07-19": "present", "2026-07-21": "present",
        "2026-07-23": "present", "2026-07-25": "present",
    },
    "1004": {
        "2026-06-30": "absent", "2026-07-01": "present", "2026-07-03": "present",
        "2026-07-05": "present", "2026-07-07": "present", "2026-07-09": "present",
        "2026-07-11": "present", "2026-07-13": "present", "2026-07-15": "present",
        "2026-07-17": "present", "2026-07-19": "present", "2026-07-21": "absent",
        "2026-07-23": "present", "2026-07-25": "present",
    },
    "1005": {
        "2026-06-30": "present", "2026-07-01": "present", "2026-07-03": "absent",
        "2026-07-05": "present", "2026-07-07": "present", "2026-07-09": "present",
        "2026-07-11": "present", "2026-07-13": "present", "2026-07-15": "present",
        "2026-07-17": "present", "2026-07-19": "present", "2026-07-21": "present",
        "2026-07-23": "present", "2026-07-25": "absent",
    },
}

# Days the class itself was cancelled (no attendance counted for anyone)
CLASS_CANCELLED_DATES = {
    "2026-07-16": "System maintenance",
    "2026-07-24": "Computer equipment upgrade",
    "2026-08-07": "Network maintenance",
    "2026-08-13": "Building power outage",
    "2026-08-27": "Classroom disinfection",
}


def add_student(student_id, name, gender):
    if student_id in students:
        print(f"Student ID '{student_id}' already exists.")
        return
    students[student_id] = {"name": name, "gender": gender}
    attendance[student_id] = {}
    print(f"Student '{name}' added with ID {student_id}.")


def remove_student(student_id):
    if student_id not in students:
        print(f"Student ID '{student_id}' not found.")
        return
    name = students[student_id]["name"]
    del students[student_id]
    del attendance[student_id]
    print(f"Student '{name}' removed.")


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


def main():
    print("=== Python Intro Class — Attendance System ===")
    print("Class schedule: Saturday to Thursday, 10:00–12:00\n")

    print("Registered students:")
    for sid, info in students.items():
        print(f"  {sid}: {info['name']} ({info['gender']})")

    print_all_summaries()

    print_student_detail("1001")

    list_cancelled_classes()

    # demonstrate adding a new attendance record
    print()
    mark_attendance("1003", "2026-07-27", "present")

    # demonstrate that cancelled days are protected
    print()
    mark_attendance("1001", "2026-07-16", "present")


if __name__ == "__main__":
    main()
