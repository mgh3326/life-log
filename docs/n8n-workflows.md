# n8n Workflow Designs

## 1. Daily Workout Nudge

**Trigger:** Cron — every day at 21:00 KST

**Logic:**
1. `GET http://localhost:8766/api/workouts/check/{today}` (ISO date)
2. If `exists = false`:
   - Fetch missing dates: `GET http://localhost:8766/api/workouts/missing?date_from={7d_ago}&date_to={today}`
   - Count consecutive missing days
   - Send Discord notification with tone based on gap:

| Gap | Message |
|-----|---------|
| 1 day | "Hey, want to log today's workout? Even 'rest day' counts!" |
| 3 days | "3 days without a log~ Want to drop a quick note?" |
| 7+ days | "A week gone by... You alive? Rest days count too!" |

**Discord:** HTTP Request node → Discord webhook URL

---

## 2. Weekly Workout Report

**Trigger:** Cron — every Sunday at 20:00 KST

**Logic:**
1. Calculate `week_start` = last Monday
2. `GET http://localhost:8766/api/workouts/report/weekly?week_start={monday}`
3. Format report and send to Discord

**Report Format:**
```
Weekly Workout Report (Mar 11 - Mar 17)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Workout days: 5 | Rest days: 2
Total calories: 1,520
Total duration: 285 min

Workout breakdown:
  CrossFit: 3
  Running: 1
  Force: 1
```

---

## Setup Notes

- Both workflows use `localhost:8766` for development.
- For production (Raspberry Pi), use `localhost:8100`.
- Discord webhook URL configured in n8n credentials
- Date format: ISO 8601 (YYYY-MM-DD)
