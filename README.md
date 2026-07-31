# Smart Attendance System

A Python program I built to track student attendance for my programming class, extended with a few rule-based analytics features.

## Features

- Add and remove students
- Mark present or absent by date
- View individual attendance records
- Class-wide attendance summary
- Cancelled class dates are recorded and protected (no attendance is marked on those days)
- Absence pattern detection — identifies which weekday each student tends to miss most often
- Risk scoring — a simple rule-based score (0–100) estimating how likely a student is to be absent next session, based on their overall attendance rate and their attendance rate over the last 5 sessions (recent sessions are weighted more heavily)
- Attendance alerts — automatically flags students at Medium or High absence risk
- Text-based attendance chart — a bar chart in the terminal showing each student's attendance rate

## How It Works

The risk score is not a machine learning model — it's a transparent, rule-based calculation:
risk_score = (0.3 × overall_absence_rate + 0.7 × recent_absence_rate) × 100
Recent absences (last 5 sessions) count for more than the full history, so a student who has recently started missing more classes shows up as higher risk even if their long-term record is still fine. I chose this approach because it's simple, explainable, and doesn't require training data — while still going a step beyond a plain present/absent counter.

## How To Run
python smart_attendance_system.py
## Notes

This started as a basic attendance tracker and was gradually extended with the analytics features above as I learned more. The logic is intentionally kept simple (comparisons, weighted averages, dictionaries) rather than using any ML library.
